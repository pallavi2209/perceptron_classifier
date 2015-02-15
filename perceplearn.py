import sys
import argparse
from decimal import Decimal
import copy
import random
def perceptMain(argv):
  parser = argparse.ArgumentParser(add_help=False)
  parser.add_argument("trainFile")
  parser.add_argument("modelFile")
  parser.add_argument('-h', dest='devFile')
  args = parser.parse_args(argv)
  trfname=args.trainFile
  mdfname=args.modelFile
  devfname=args.devFile

  setcls=set()
  dictuw={}
  trfile=open(trfname,'r')
  lineList=[]
  for line in trfile:
    lineList.append(line)
  random.shuffle(lineList)
  shTrFile=open("mypercept.shuffled.train",'w+')
  for lineItem in lineList:
    shTrFile.write(lineItem)
  #unique words dictuw={word->0}
  shTrFile.seek(0,0)
  for line in shTrFile:
    tokens=line.split()
    strClass=tokens[0]
    setcls.add(strClass)
    for i in range(1,len(tokens)):
      token=tokens[i]
      if token not in dictuw:
        dictuw[token]=0
  dictClsWts={}
  for item in setcls:
    dictClsWts[item]=copy.deepcopy(dictuw)
 
  for N in range(0,3):
    trfile.seek(0,0)
    for line in trfile:
      maxwtsum = Decimal('-inf')
      maxwtcls = next(iter(setcls))
      wtsum=0
      tokens=line.split()
      trueCls=tokens[0]
      # compute class, wt tuple
      maxwtcls = max( setcls , key = lambda cls: sum( [ dictClsWts[cls][token] for token in tokens[1:] ]) )

      if trueCls != maxwtcls :
      #  print("wrong prediction for line: %s \n True class: %s, Predicted class: %s"% (line, trueCls, maxwtcls))
        dictLine={}
        for token in tokens[1:]:
          if token in dictLine:
            dictLine[token]=1 + (dictLine[token])
          else:
            dictLine[token]=1

        #update the weights for truecls and maxwtcls
        dicttcls=dictClsWts[trueCls]
        dictfcls=dictClsWts[maxwtcls]
        for k,v in dictLine.items():
          dictClsWts[trueCls][k]= dictClsWts[trueCls][k]-v
          dictClsWts[maxwtcls][k]=dictClsWts[maxwtcls][k]+v
    print(dictClsWts)
    devFile=open(devfname,'r')
    correctPred=0
    totFiles=0
    accuracy=0
    for line in devFile:
      totFiles+=1
      tokens=line.split()
      truecls=tokens[0]
      # compute class, wt tuple
      maxwtcls = max( setcls , key = lambda cls: sum( [ dictClsWts[cls][token] for token in tokens[1:] if token in dictuw]) )
 #     print("True class: %s, Predicted class: %s"%(truecls,maxwtcls))
      if truecls==maxwtcls:
        correctPred+=1
    accuracy=correctPred/totFiles
    print("Iteration %d: Accuracy:%f"%(N,accuracy))
  trfile.close()
 
if __name__=="__main__":
  perceptMain(sys.argv[1:])
