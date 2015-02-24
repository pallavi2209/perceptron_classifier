import tempfile
import re
import sys
import os
sys.path.append('..')
import argparse
try:
  import perceplearn
except:
  print("Cannot find perceplearn module. Please check directory structure.\n Exiting... ")
  sys.exit()

def getWShape(word):
    word = re.sub('[a-z]+','a',word)
    word = re.sub('[A-Z]+','A',word)
    word = re.sub('[0-9]+','9',word)
    word = re.sub('[^0-9a-zA-Z]+','-',word)
    return word


def processToken(token):
  indexes = [found.start() for found in re.finditer('/',token)]
  if len(indexes)<2:
    return -1
  iSecLast = indexes[-2]
  word=token[:iSecLast]
  pbTag=token[iSecLast+1:]
  posTag=pbTag.split("/")[0]
  neTag=pbTag.split("/")[1]
  return [word, posTag, neTag]

def createNeFile(inFileName,outFileName):
  infile=open(inFileName,'r',errors="ignore")
  outfile=open(outFileName,"w")
  for line in infile:
    tokens=line.split()
    prep=["BOS/BOS/BOS"]
    app=["EOS/EOS/EOS"]
    tokens=prep+tokens+app

    resPrev=processToken(tokens[0])
    resCurr=processToken(tokens[1])
    for i in range(2,len(tokens)):
      resLine=""

      if resPrev==-1:
        continue;
      else:
        prevW=resPrev[0]
        prevTag=resPrev[1]

      if resCurr==-1:
        continue;
      else:
        currW=resCurr[0]
        currTag=resCurr[1]
        nertagCurr=resCurr[2]
 
      resNext=processToken(tokens[i])
      if resNext==-1:
        continue;
      else:
        nextW=resNext[0]
        nextTag=resNext[1]
   
      resLine=resLine + nertagCurr
      prevWF="prevW:"+prevW
      prevTF="prevT:"+prevTag
      currWF="currW:"+currW
      currTF="currT:"+currTag
      nextWF="nextW:"+nextW
      nextTF="nextT:"+nextTag
      suffixFx="suff:"+currW[-4:]
      suffixFy="suff:"+currW[-3:]
      
      wshape = "wshape:" + getWShape(currW)
      resLine=resLine+" "+ prevWF+ " " + prevTF + " "+ currWF+" "+ currTF + " "+ nextWF + " " + nextTF + " " + suffixFx + " " +  suffixFy + " " + wshape + "\n"
      outfile.write(resLine)
      resPrev=resCurr
      resCurr=resNext
  infile.close()
  outfile.close()

def netrainMain(argv):
  parser = argparse.ArgumentParser(add_help=False)
  parser.add_argument("trainFile")
  parser.add_argument("modelFile")
  parser.add_argument('-h', dest='devFile')
  args = parser.parse_args(argv)
  trfname=args.trainFile
  mdfname=args.modelFile
  if args.devFile:
    devfname=args.devFile

  ptrfile = tempfile.NamedTemporaryFile(delete=False)
  ptrfname=ptrfile.name
  ptrfile.close()
  createNeFile(trfname,ptrfname)

  if args.devFile:
    pdevFile = tempfile.NamedTemporaryFile(delete=False)
    pdevfname=pdevFile.name
    pdevFile.close()
    createNeFile(devfname,pdevfname)
    pargs=[ptrfname,mdfname,"-h",pdevfname]
  else:
    pargs=[ptrfname,mdfname]
  perceplearn.perceptMain(pargs)
  os.unlink(ptrfname)
  if args.devFile:
    os.unlink(pdevfname)

if __name__=="__main__":
  netrainMain(sys.argv[1:])
