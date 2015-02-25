import sys
import argparse
import pickle
import re
import codecs
def getWShape(word):
    word = re.sub('[a-z]+','a',word)
    word = re.sub('[A-Z]+','A',word)
    word = re.sub('[0-9]+','9',word)
    word = re.sub('[^0-9a-zA-Z]+','-',word)
    return word

def createposFile(inLine):
  listPre=[]
  tokens=inLine.split()
  prep=["BOS/BOS"]
  app=["EOS/EOS"]
  tokens=prep+tokens+app
  
  prev=tokens[0].split("/")
  curr=tokens[1].split("/")
  for i in range(2,len(tokens)):
    line=""
    currW=curr[0]
    prevW=prev[0]
    nxt=tokens[i].split("/")
    nextW=nxt[0]
    
    prevF="prev:"+prevW
    currF="curr:"+currW
    nextF="next:"+nextW
    suffixFthree="suff3:"+currW[-3:]
    suffixFtwo="suff2:"+currW[-2:]
    wshape = "wshape:" + getWShape(currW)
    
    line += prevF + " "+ currF +" "+ nextF + " "  + suffixFthree + " " + suffixFtwo + " " +  wshape + "\n"
    listPre.append(line)
    prev=curr
    curr=nxt
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
  sys.stdin = codecs.getreader('utf8')(sys.stdin.detach(), errors='ignore')
  for doc in sys.stdin:
    listToTag=createposFile(doc)
    result=""
    for line in listToTag:  
      tokens=line.split()
      currW=tokens[1].split(":")[1]
      maxwtcls = max( setcls , key = lambda cls: sum( [ dictClsWts[cls][token] for token in tokens[0:] if token in dictClsWts[cls]]) )
      result += currW + "/" + maxwtcls + " "
    print(result.rstrip())
    sys.stdout.flush()


if __name__=="__main__":
  postagMain(sys.argv[1:])
