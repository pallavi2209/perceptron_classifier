import sys
sys.path.append('..')
import argparse
import pickle
def createposFile(inLine):
  listPre=[]
  tokens=inLine.split()
  prep=["BOS/BOS"]
  app=["EOS/EOS"]
  tokens=prep+prep+tokens+app+app
  
  for i in range(2,len(tokens)-2):
    line=""
    curr=tokens[i].split("/")
    currW=curr[0]

    pPrevW=tokens[i-2].split("/")[0]
    prevW=tokens[i-1].split("/")[0]

    nextW=tokens[i+1].split("/")[0]
    nNextW=tokens[i+2].split("/")[0]

#      line=line+tagCurrent

    if prevW!="BOS":
      prevW=prevW.lower()
    if nextW!="EOS":
      nextW=nextW.lower()
    if pPrevW!="BOS":
      pPrevW=pPrevW.lower()
    if nNextW!="EOS":
      nNextW=nNextW.lower()
      
    pPrevF="pprev:"+pPrevW
    prevF="prev:"+prevW
    currF="curr:"+currW.lower()
    nextF="next:"+nextW
    nNextF="nnext:"+nNextW
    prefixF="pref:"+currW[:2]
    suffixF="suff:"+currW[-3:]
    line += pPrevF + " "+ prevF + " "+ currF +" "+ nextF + " " + nNextF + " "+ prefixF + " " + suffixF +"\n"
    listPre.append(line)
  return listPre

def postagMain(argv):
  parser = argparse.ArgumentParser(add_help=False)
  parser.add_argument("modelFile")
  args = parser.parse_args(argv)
  mdfname=args.modelFile

  with open(mdfname,"rb") as handle:
    data=pickle.load(handle)

  dictClsWts=data["wDict"]
  setcls = data["setcls"]

  for doc in sys.stdin:
    listToTag=createposFile(doc)
    result=""
    for line in listToTag:  
      tokens=line.split()
      currW=tokens[2].split(":")[1]
      maxwtcls = max( setcls , key = lambda cls: sum( [ dictClsWts[cls][token] for token in tokens[0:] if token in dictClsWts[cls]]) )
      result += currW + "/" + maxwtcls + " "
    print(result)
    sys.stdout.flush()


if __name__=="__main__":
  postagMain(sys.argv[1:])
