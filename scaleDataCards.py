import sys
import math

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def scaleDataCard(indatacardname,histogramsname,inputdir,outputdir,outdatacardname,outhistogramsname,scale,scaleFactorTheoSysts=1.0,theoSysts=[],scaleStatSysts=False,statSysts=[]):
  
  print 'Scaling datacard by factor',scale
  print 'input file',inputdir+indatacardname
  print 'output file',outputdir+outdatacardname

  infile=open(outputdir+indatacardname,"r")
  inlist=list(infile)
  newlines=[]

  for line in inlist:
    if ("observation" in line or "rate" in line):
      splitline=line.replace("\n","").replace("\t"," ").split(" ")
      futureline=""
      
      for word in splitline:
	      if (is_number(word) and word!="-1"):
	        fl=float(word)
	        nfl=fl*scale
	        nw=str(nfl)
	        futureline+=nw+" "
	      else:
	        futureline+=word+" "
          
      futureline=futureline.rstrip(" ")+"\n"
      newlines.append(futureline)
    
    elif (scaleStatSysts==True and line.replace("\n","").replace("\t"," ").split(" ")[0] in statSysts):
      print "stat syst"
      splitline=line.replace("\n","").replace("\t"," ").split(" ")
      futureline=""
      
      for word in splitline:
        if (is_number(word) and word!="-1"):
	        fl=float(word)
	        nfl=fl/math.sqrt(float(scale))
	        nw=str(nfl)
	        futureline+=nw+" "
	        #print word, nw
        else:
	        futureline+=word+" "
          
      futureline=futureline.rstrip(" ")+"\n"
      newlines.append(futureline)
            
    elif (scaleFactorTheoSysts!=1.0 and line.replace("\n","").replace("\t"," ").split(" ")[0] in theoSysts):
      print "theo syst"
      splitline=line.replace("\n","").replace("\t"," ").split(" ")
      futureline=""
      
      for word in splitline:
        if (is_number(word) and word!="-1"):
	        fl=float(word)
	        nfl=(fl-1.0)*float(scaleFactorTheoSysts)+1.0
	        nw=str(nfl)
	        futureline+=nw+" "
        elif ("/" in word):
	        if (is_number(word.split("/")[0]) and is_number(word.split("/")[1]) ):
	          fl1=float(word.split("/")[0])
	          nfl1=1.0-(1.0-fl1)*float(scaleFactorTheoSysts)
	          nw1=str(nfl1)
	          futureline+=nw1+"/"
	          fl2=float(word.split("/")[1])
	          nfl2=(fl2-1.0)*float(scaleFactorTheoSysts)+1.0
	          nw2=str(nfl2)
	          futureline+=nw2+" "
        else:
	        futureline+=word+" "

      futureline=futureline.rstrip(" ")+"\n"
      newlines.append(futureline)

    elif histogramsname in line:
      futureline=line.replace(inputdir,outputdir).replace(histogramsname,outhistogramsname)
      newlines.append(futureline)
      
    else:
      newlines.append(line)
    
  outfile=open(outputdir+outdatacardname,"w")
  for line in newlines:
    outfile.write(line)
  outfile.close()
  
  print 'Done scaling datacard'
