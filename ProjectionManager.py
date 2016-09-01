import sys
import os
import stat
from subprocess import call
from subprocess import check_output
import ROOT
import copy
import time as timer

from QueHelper import QueHelper

import Configuration
import Projection

import CMS_lumi, tdrstyle

class ProjectionManager:
  def __init__(self,currentPath):
    self.Path = currentPath
    self.Verbose = True
    
    self.doParallel = Configuration.doParallel
    
    self.doProjection = Configuration.doProjection
    
    self.doCombineDataCards = Configuration.doCombineDataCards
    self.doScaleToProjection = Configuration.doScaleToProjection
    self.doCalulation = Configuration.doCalulation
    
    self.doOutputParsing = Configuration.doOutputParsing
    self.doPlotLimits = Configuration.doPlotLimits
    
    self.outputDir=Configuration.outputDir
    if self.outputDir[-1] != '/':
        self.outputDir+='/'
    
    self.projectionLuminosity = Configuration.projectionLuminosity
    
    self.Projections = []
    for name,lumi,theofactor in zip(Configuration.projectionName,Configuration.projectionLuminosity,Configuration.projectionFactorTheorySyst):
      lumifactor = lumi/self.projectionLuminosity[0]
      self.Projections.append(Projection.Projection(name,lumifactor,theofactor,Configuration.theoSysts,Configuration.scaleStatSyst,Configuration.statSysts,Configuration.inputDir,self.outputDir,Configuration.dataCards,Configuration.dataCardNames,Configuration.omittedSysts,Configuration.histograms))
    
    self.JobIDList=[]
    self.JobScriptList=[]
    self.QueHelper=""

    
  def CreateOutputPaths(self):
    if not os.path.exists(self.outputDir):
      os.makedirs(self.outputDir)
        
    print "output directory created"


  def SetQueHelper(self,quesystem):
    self.QueHelper=QueHelper(quesystem)


  def RunProjection(self,i):
    
    self.Projections[i].Run(self.doCombineDataCards,self.doScaleToProjection,self.doCalulation)


  def OutputParsing(self):
    
    calulatedLimitsObs=[]
    calulatedLimitsExp=[]
    
    for iproj,projection in enumerate(self.Projections):#for name,cats,systs in self.Scenarios:
      
      resultslimitname=self.outputDir+'results_limit_'+projection.name+'.txt'

      resultslimitname=open(resultslimitname,'r')
      for line in resultslimitname:
        if 'Expected 50' in line:
          calulatedLimitsExp.append(float(line.split(' < ')[-1]))
      resultslimitname.close()

    finallimitresults=self.outputDir+'finalresults_limit.txt'
    finallimitfile=open(finallimitresults,'w')

    for iproj,projection in enumerate(self.Projections): #for isc,(name,cats,systs) in enumerate(self.Scenarios):

      outstring=projection.name+' expected: '

      outstring+=str(calulatedLimitsExp[iproj])
      if iproj > 0:
        outstring+='   ratio: {:06.4f}'.format((calulatedLimitsExp[iproj]/calulatedLimitsExp[0])-1)

      outstring+='\n'

      finallimitfile.write(outstring)
    
    finallimitfile.close()
  
  
  def PlotLimits(self):
    
    calulatedLimits=[]
    
    for iproj,projection in enumerate(self.Projections):#for name,cats,systs in self.Scenarios:
      
      resultslimitname=self.outputDir+'results_limit_'+projection.name+'.txt'

      resultslimitname=open(resultslimitname,'r')
      
      limits = []
      
      for line in resultslimitname:
        if 'Expected' in line:
          limits.append(float(line.split(' < ')[-1]))
      
      calulatedLimits.append(limits)
      
      resultslimitname.close()

    medianLimits = ROOT.TGraph()
    oneSigmaBand = ROOT.TGraphAsymmErrors()
    twoSigmaBand = ROOT.TGraphAsymmErrors()

    for ilimit,((down2,down1,median,up1,up2),lumi) in enumerate(zip(calulatedLimits,self.projectionLuminosity)):
      medianLimits.SetPoint(ilimit,lumi,median)
      oneSigmaBand.SetPoint(ilimit,lumi,median)
      twoSigmaBand.SetPoint(ilimit,lumi,median)
      oneSigmaBand.SetPointError(ilimit,0,0,median-down1,up1-median)
      twoSigmaBand.SetPointError(ilimit,0,0,median-down2,up2-median)

    canvas = ROOT.TCanvas('projection','Limit Projection',1000,800)
    canvas.SetMargin(0.14,0.04,0.13,0.07)
    
    medianLimits.GetXaxis().SetTitle('Integrated luminosity [fb^{-1}]')
    medianLimits.GetXaxis().SetTitleSize(0.06)
    medianLimits.GetXaxis().SetTitleOffset(0.95)
    medianLimits.GetXaxis().SetLabelSize(0.05)
    medianLimits.GetYaxis().SetTitle('95% CL #sigma/#sigma_{SM}')
    medianLimits.GetYaxis().SetTitleSize(0.06)
    medianLimits.GetYaxis().SetTitleOffset(1.)
    medianLimits.GetYaxis().SetLabelSize(0.05)
  
    medianLimits.SetLineWidth(3)
    medianLimits.Draw('ALP')
    
    oneSigmaBand.SetFillColor(ROOT.kGreen)
    twoSigmaBand.SetFillColor(ROOT.kYellow)
    
    twoSigmaBand.Draw('E3same')
    oneSigmaBand.Draw('E3same')
    medianLimits.Draw('LPsame')
        
    legend=ROOT.TLegend()
    legend.SetX1NDC(0.65)
    legend.SetX2NDC(1.0)
    legend.SetY1NDC(0.72)
    legend.SetY2NDC(0.9)
    legend.SetBorderSize(0);
    legend.SetLineStyle(0);
    legend.SetTextFont(42);
    legend.SetTextSize(0.06);
    legend.SetFillStyle(0);
    legend.AddEntry(medianLimits,'Median','L')
    legend.AddEntry(oneSigmaBand,'#pm 1 #sigma','F')
    legend.AddEntry(twoSigmaBand,'#pm 2 #sigma','F')
    legend.Draw()
    
#    cms = ROOT.TLatex(0.2, 0.94, 'CMS private work'  );
#    cms.SetTextFont(42)
#    cms.SetNDC()
#    cms.Draw()
    
    frame1 = ROOT.TLine(ROOT.gPad.GetUxmin(),ROOT.gPad.GetUymax(),ROOT.gPad.GetUxmax(),ROOT.gPad.GetUymax())
    frame2 = ROOT.TLine(ROOT.gPad.GetUxmax(),ROOT.gPad.GetUymin(),ROOT.gPad.GetUxmax(),ROOT.gPad.GetUymax())
    frame1.Draw("same")
    frame2.Draw("same")

    canvas.RedrawAxis()
    
    line=ROOT.TLine(ROOT.gPad.GetUxmin(),1,ROOT.gPad.GetUxmax(),1)
    line.SetLineWidth(3)
    line.SetLineColor(632)
    line.Draw()
    
    #CMS text
    #CMS_lumi.lumi_13TeV = "2.7 fb^{-1}"
    CMS_lumi.lumi_13TeV = ""
    CMS_lumi.writeExtraText = 1
    CMS_lumi.extraText = "private work"
    CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

    CMS_lumi.cmsTextSize = .9
    CMS_lumi.lumiTextOffset = 0.2
    CMS_lumi.lumiTextSize = 0.7
    CMS_lumi.cmsTextOffset = 0.05
    CMS_lumi.relPosX = 0.17

    #CMS_lumi.relExtraDY = 1.0
    
    #draw the lumi text on the canvas
    iPeriod=4   # 13TeV
    iPos=0     # CMS inside frame
    CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)
    
    minXaxisSTD=0
    maxXaxisSTD=self.projectionLuminosity[-1]
    minYaxisSTD=0.001
    maxYaxisSTD=8.0
    
    medianLimits.GetYaxis().SetRangeUser(minYaxisSTD,maxYaxisSTD)
    medianLimits.GetXaxis().SetRangeUser(minXaxisSTD,maxXaxisSTD)
    
    line.SetX1(minXaxisSTD)
    line.SetX2(maxXaxisSTD)
    
    frame1.SetX1(minXaxisSTD)
    frame1.SetY1(maxYaxisSTD)
    frame1.SetX2(maxXaxisSTD)
    frame1.SetY2(maxYaxisSTD)
    
    frame2.SetX1(maxXaxisSTD)
    frame2.SetY1(minYaxisSTD)
    frame2.SetX2(maxXaxisSTD)
    frame2.SetY2(maxYaxisSTD)
    
    canvas.SaveAs(self.outputDir+'projectionplot.pdf')
    canvas.SaveAs(self.outputDir+'projectionplot.root')

    minXaxisLOG=0
    maxXaxisLOG=self.projectionLuminosity[-1]
    minYaxisLOG=0.001
    maxYaxisLOG=8.0
    
    canvas.SetLogx()
    medianLimits.GetYaxis().SetRangeUser(minYaxisLOG,maxYaxisLOG)
    medianLimits.GetXaxis().SetRangeUser(minXaxisLOG,maxXaxisLOG)
    
    line.SetX1(minXaxisSTD)
    line.SetX2(maxXaxisSTD)
    
    frame1.SetX1(minXaxisLOG)
    frame1.SetY1(maxYaxisLOG)
    frame1.SetX2(maxXaxisLOG)
    frame1.SetY2(maxYaxisLOG)
    
    frame2.SetX1(maxXaxisLOG)
    frame2.SetY1(minYaxisLOG)
    frame2.SetX2(maxXaxisLOG)
    frame2.SetY2(maxYaxisLOG)
    
    canvas.SaveAs(self.outputDir+'projectionplot_log.pdf')
    canvas.SaveAs(self.outputDir+'projectionplot_log.root')
    
    finallimitresults=self.outputDir+'finalresults_limit.txt'
    finallimitfile=open(finallimitresults,'w')    
  

  def Run(self):
  
    self.CreateOutputPaths()
    
    if self.doProjection:
      if self.doParallel:
        if not os.path.exists("PreparationScripts"):
          os.makedirs("PreparationScripts")

        mainrunline=self.QueHelper.GetRunLines()

        for iproj,projection in enumerate(self.Projections):
          joblines=[]
          jj=self.QueHelper.GetExecLines()
          for jjj in jj:
            joblines.append(jjj)
          joblines.append("cd "+self.Path+"\n")
          joblines.append("python "+self.Path+"Parallel.py "+str(iproj))

          outfile=open("PreparationScripts/"+projection.name+".sh","w")
          for line in joblines:
            outfile.write(line)
          outfile.close()
          st = os.stat("PreparationScripts/"+projection.name+".sh")
          os.chmod("PreparationScripts/"+projection.name+".sh", st.st_mode | stat.S_IEXEC)

          runlines=[]
          thisrl=mainrunline[0]
          runlines.append(thisrl)
          runlines[-1]=runlines[-1].replace("INSERTPATHHERE",self.Path)
          runlines[-1]=runlines[-1].replace("INSERTEXECSCRIPTHERE","PreparationScripts/"+projection.name+".sh")
          runfile=open("runPrep.sh","w")
          for rl in runlines:
            runfile.write(rl)
          runfile.close()
          st = os.stat("runPrep.sh")
          os.chmod("runPrep.sh", st.st_mode | stat.S_IEXEC)

          thisID=self.QueHelper.StartJob("./runPrep.sh")
          self.JobIDList.append(thisID)
          print "submitted ", "PreparationScripts/"+projection.name+".sh"

        #now check the que until its finished
        JobsStillRunning=True
        nJobsStillRunning=len(self.JobIDList)
        while(JobsStillRunning):
          timer.sleep(30)
          nJobsStillRunning=0
          for job in self.JobIDList:
            if self.QueHelper.GetIsJobRunning(job):
              nJobsStillRunning+=1
          if nJobsStillRunning>0:
            JobsStillRunning=True
          else:
            JobsStillRunning=False

          print nJobsStillRunning, " jobs still running"

      else:
        print 'Running locally'
        for iproj,projection in enumerate(self.Projections):
          print 'Start Projection',iproj,':', projection.name
          self.RunProjection(iproj)
          print 'Done with Projection',iproj
        
    if self.doOutputParsing:
      self.OutputParsing()
      
    if self.doPlotLimits:
      self.PlotLimits()
