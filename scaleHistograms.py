import sys
import os
import ROOT

def scaleHistograms(infilename,outfilename,scale,scaleFactorTheoSysts=1.0,scaleStatSysts=False):
  
  print 'Scaling histograms by factor',scale
  print 'input file',infilename
  print 'output file',outfilename
  
  outdir = outfilename.rstrip(outfilename.rsplit('/',1)[-1])
  if not os.path.exists(outdir):
    os.makedirs(outdir)
  
  inf=ROOT.TFile(infilename,"READ")
  outf=ROOT.TFile(outfilename,"RECREATE")
  
  histlist=inf.GetListOfKeys()
  
  print len(histlist), " histos in file"

  for ih in range(len(histlist)):
    inf.cd()
    thishist=inf.Get(histlist[ih].GetName())
    thishist.Scale(scale)
    outf.cd()
    thishist.Write()

  inf.Close()
  outf.Close()
  
  print 'Done scaling histograms'
