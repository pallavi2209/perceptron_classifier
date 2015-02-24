import sys
sys.path.append('..')
import argparse
import re
import os
import tempfile
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

def createposFile(inFileName,outFileName):
  infile=open(inFileName,'r')
  outfile=open(outFileName,"w")
  for line in infile:
    tokens=line.split()
    prep=["BOS/BOS"]
    app=["EOS/EOS"]
    tokens=prep+tokens+app
    prev=tokens[0].split("/")
    curr=tokens[1].split("/")
    for i in range(2,len(tokens)):
      resLine=""
      currW=curr[0]
      tagCurrent=curr[1]

      prevW=prev[0]
      nxt=tokens[i].split("/")
      nextW=nxt[0]

      resLine=resLine+tagCurrent

      prevF="prev:"+prevW
      currF="curr:"+currW
      nextF="next:"+nextW
      suffixFthree="suff3:"+currW[-3:]
      suffixFtwo="suff2:"+currW[-2:]
      wshape = "wshape:" + getWShape(currW)
      resLine=resLine+" " + prevF + " "+ currF +" "+ nextF + " " + suffixFthree + " " + suffixFtwo + " " +  wshape + "\n"
      outfile.write(resLine)
      prev=curr
      curr=nxt
  infile.close()
  outfile.close()

def postrainMain(argv):
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
  ptrfname = ptrfile.name
  ptrfile.close()
  createposFile(trfname,ptrfname)
  if args.devFile:
    pdevFile = tempfile.NamedTemporaryFile(delete=False)
    pdevfname=pdevFile.name
    pdevFile.close()
    createposFile(devfname,pdevfname)
    pargs=[ptrfname,mdfname,"-h",pdevfname]
  else: 
    pargs=[ptrfname,mdfname]
  perceplearn.perceptMain(pargs)
  os.unlink(ptrfname)
  if args.devFile:
    os.unlink(pdevfname) 

if __name__=="__main__":
  postrainMain(sys.argv[1:])
