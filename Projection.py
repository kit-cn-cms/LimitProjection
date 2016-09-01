import os
from subprocess import call

import scaleDataCards
import scaleHistograms

class Projection:
  def __init__(self,name,factorLuminosity,factorTheorySyst,theoSysts,scaleStatSyst,statSysts,inputDir,outputDir,dataCards,dataCardNames,omittedSysts,histograms,isCombined=False,isScaled=False):
    
    self.name = name
    
    self.factorLuminosity = factorLuminosity
    
    self.factorTheorySyst = factorTheorySyst
    self.theoSysts = theoSysts
    self.scaleStatSyst = scaleStatSyst
    self.statSysts = statSysts
    
    self.inputDir = inputDir
    self.outputDir = outputDir
    
    self.dataCards = dataCards
    self.dataCardNames = dataCardNames
    
    self.omittedSysts = omittedSysts
    
    self.histograms = histograms
    
    self.isCombined = isCombined
    self.isScaled = isScaled
    
    
  def CombineDataCards(self):
    
    datacardCombineString = [ name+'='+self.inputDir+datacard for datacard,name in zip(self.dataCards,self.dataCardNames)]
    
    dummyname=self.outputDir+'dummydatacard.txt'

    dummyfile=open(dummyname,'w')

    call(['combineCards.py']+datacardCombineString, stdout=dummyfile)

    dummyfile.close()

    dummyfile=open(dummyname,'r')

    datacardname=self.outputDir+'datacard_'+self.name+'.txt'
    datacardfile=open(datacardname,'w')

    for line in dummyfile:
      if line.split()[0] in self.omittedSysts:
        continue

      if line.split()[0] == 'kmax':
        splitline=line.split()
        splitline[1]=str(int(splitline[1])-len(self.omittedSysts))

        newline=''
        for word in splitline:
          newline+=word

          if word != splitline[-1]:
            newline+=' '
          else:
            newline+='\n'

        datacardfile.write(newline)
        continue          

      datacardfile.write(line)

    datacardfile.close() 
    dummyfile.close()
    
    self.isCombined = True
  
  def ScaleToProjection(self):
  
    datacardname = ''
    if os.path.isfile(self.outputDir+'datacard_'+self.name+'.txt'):
      datacardname='datacard_'+self.name+'.txt'
    else:
      print 'Error! No valid datacard found! Terminating!'
      return
    
    outputhistogram = self.histograms.rsplit('.',1)[0]+'_'+self.name+'.'+self.histograms.rsplit('.',1)[1]
    scaleDataCards.scaleDataCard(datacardname,self.histograms,self.inputDir,self.outputDir,'datacard_'+self.name+'_scaled.txt',outputhistogram,self.factorLuminosity,self.factorTheorySyst,self.theoSysts,self.scaleStatSyst,self.statSysts)
    scaleHistograms.scaleHistograms(self.inputDir+self.histograms,self.outputDir+outputhistogram,self.factorLuminosity,self.factorTheorySyst,self.scaleStatSyst)
    
    self.isScaled = True
    
  def CalulateLimit(self):
    
    datacardname = ''
    if self.isScaled:
      datacardname=self.outputDir+'datacard_'+self.name+'_scaled.txt'
    elif self.isCombined :
      datacardname=self.outputDir+'datacard_'+self.name+'.txt'
    elif os.path.isfile(self.outputDir+'datacard_'+self.name+'_scaled.txt'):
      datacardname=self.outputDir+'datacard_'+self.name+'_scaled.txt'
    elif os.path.isfile(self.outputDir+'datacard_'+self.name+'.txt'):
      datacardname=self.outputDir+'datacard_'+self.name+'.txt'
    else:
      print 'Error! No valid datacard found! Terminating!'
      return
    
    resultslimitname=self.outputDir+'results_limit_'+self.name+'.txt'
    resultslimitsfile=open(resultslimitname,'w')
       
    print 'Start Limit Calculation with Datacard',datacardname
    print 'Output File',resultslimitname
    call(['combine','-M','Asymptotic','--minosAlgo','stepping','-m','125','--run=blind',datacardname], stdout=resultslimitsfile)
    print 'Done with Limit Calulation'
    
    
  def Run(self,doCombineDataCards,doScaleToProjection,doCalulation):
  
    if doCombineDataCards:
      self.CombineDataCards()
    if doScaleToProjection:
      self.ScaleToProjection()
    if doCalulation:
      self.CalulateLimit()
    
