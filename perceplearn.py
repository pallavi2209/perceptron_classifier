import sys
import argparse
from decimal import Decimal
import copy
import random
import pickle
def perceptMain(argv):
  parser = argparse.ArgumentParser(add_help=False)
  parser.add_argument("trainFile")
  parser.add_argument("modelFile")
  parser.add_argument('-h', dest='devFile')
  args = parser.parse_args(argv)
  trfname=args.trainFile
  mdfname=args.modelFile
  if args.devFile:
    devfname=args.devFile
  setcls=set()
  dictuw={}
  trfile=open(trfname,'r')
  lineList = trfile.readlines()
  trfile.close()
  for line in lineList:
    tokens=line.split()
    strClass=tokens[0]
    setcls.add(strClass)
    for i in range(1,len(tokens)):
      token=tokens[i]
      if token not in dictuw:
        dictuw[token]=0
  dictClsWts={}
  dictClsBias={}
  dictClsAvg={}
  for item in setcls:
    dictClsWts[item]=copy.deepcopy(dictuw)
    dictClsBias[item]=copy.deepcopy(dictuw)
    dictClsAvg[item]=copy.deepcopy(dictuw)
  maxAcc=0
  maxModel=dictClsAvg
  for N in range(0,20):
    totDocs=0
    random.shuffle(lineList)
    for line in lineList:
      totDocs+=1
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
        docLength = sum( dictLine.values())
        #update the weights for truecls and maxwtcls
        for k,v in dictLine.items():
          dictClsWts[trueCls][k] = dictClsWts[trueCls][k] + v
          dictClsWts[maxwtcls][k]=dictClsWts[maxwtcls][k] - v
          dictClsBias[trueCls][k]+=N*v
          dictClsBias[maxwtcls][k]-=N*v
    #print(dictClsWts)
    for c,d in dictClsWts.items():
      for t,val in d.items():
        avgVal=val-(dictClsBias[c][t]/totDocs)
        dictClsAvg[c][t]=avgVal
    if args.devFile:
      devFile=open(devfname,'r')
      correctPred=0
      totFiles=0
      accuracy=0
      for line in devFile:
        totFiles+=1
        tokens=line.split()
        truecls=tokens[0]
        # compute class, wt tuple
        maxwtcls = max( setcls , key = lambda cls: sum( [ dictClsAvg[cls][token] for token in tokens[1:] if token in dictClsAvg[cls]]))
   #     print("True class: %s, Predicted class: %s"%(truecls,maxwtcls))
        if truecls==maxwtcls:
          correctPred+=1
      accuracy=correctPred/totFiles
      if accuracy>maxAcc:
        maxAcc=accuracy
        maxModel=dictClsAvg
      print("Iteration %d with Accuracy:%f"%(N,accuracy))
    else:
      print("Iteration %d complete.."%(N))
      maxModel=dictClsAvg
  if args.devFile:
    print("Model with Accuracy:%f is stored as %s"%(maxAcc,mdfname))
  else:
    print("Model with last iteration written as %s"%(mdfname))
  dictModel=dict(wDict=maxModel,setcls=setcls)
  with open(mdfname,"wb") as handle:
    pickle.dump(dictModel,handle)
  trfile.close()
  if args.devFile:
    devFile.close()
  handle.close()
 
if __name__=="__main__":
  perceptMain(sys.argv[1:])
