import sys
sys.path.append('..')
import argparse
try:
  import perceplearn
except:
  print("Cannot find perceplearn module. Please check directory structure.\n Exiting... ")
  sys.exit()


def createposFile(inFileName,outFileName):
  infile=open(inFileName,'r')
  outfile=open(outFileName,"w")
  for line in infile:
    tokens=line.split()
    prep=["BOS/BOS"]
    app=["EOS/EOS"]
    tokens=prep+prep+tokens+app+app
    for i in range(2,len(tokens)-2):
      line=""
      curr=tokens[i].split("/")
      currW=curr[0]
      tagCurrent=curr[1]
#      pprevW=tokens[i-2].split("/")[0]
      prevW=tokens[i-1].split("/")[0]
      nextW=tokens[i+1].split("/")[0]
#      nnextW=tokens[i+2].split("/")[0]
      line=line+tagCurrent
   #   pprevF="pprev:"+pprevW
      if prevW!="BOS":
        prevW=prevW.lower()
      if nextW!="EOS":
        nextW=nextW.lower()
      prevF="prev:"+prevW
      currF="curr:"+currW.lower()
      nextF="next:"+nextW
#      nnextF="nnext:"+nnextW
      prefixF="pref:"+currW[:2]
      suffixF="suff:"+currW[-3:]
      line=line+" "+ prevF + " "+ currF +" "+ nextF  + " "+ prefixF + " " + suffixF +"\n"
      outfile.write(line)
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
  devfname=args.devFile


  ptrfname = trfname+".pre.percepTrain"
  pdevfname = devfname+"pre.percepDev"
  createposFile(trfname,ptrfname)
  createposFile(devfname,pdevfname)
  pargs=[ptrfname,mdfname,"-h",pdevfname]
  perceplearn.perceptMain(pargs)

if __name__=="__main__":
  postrainMain(sys.argv[1:])
