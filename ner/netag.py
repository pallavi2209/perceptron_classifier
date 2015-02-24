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

def processToken(token):
  indexes = [found.start() for found in re.finditer('/',token)]
  if len(indexes)<1:
    return -1
  iSecLast = indexes[-1]
  word=token[:iSecLast]
  pbTag=token[iSecLast+1:]
  posTag=pbTag.split("/")[0]
  return [word, posTag]

def createneFile(inLine):
  listPre=[]
  tokens=inLine.split()
  prep=["BOS/BOS"]
  app=["EOS/EOS"]
  tokens=prep+tokens+app

  resPrev=processToken(tokens[0])
  resCurr=processToken(tokens[1])
  for i in range(2,len(tokens)):
    line=""

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

    resNext=processToken(tokens[i])
    if resNext==-1:
      continue;
    else:
      nextW=resNext[0]
      nextTag=resNext[1]

    prevWF="prevW:"+prevW
    prevTF="prevT:"+prevTag
    currWF="currW:"+currW
    currTF="currT:"+currTag
    nextWF="nextW:"+nextW
    nextTF="nextT:"+nextTag
    suffixFx="suff:"+currW[-4:]
    suffixFy="suff:"+currW[-3:]

    wshape = "wshape:" + getWShape(currW)
    line = prevWF+ " " + prevTF + " "+ currWF+" "+ currTF + " "+ nextWF + " " + nextTF + " "  + suffixFx + " " + suffixFy+ " " +  wshape +"\n"
    resPrev=resCurr
    resCurr=resNext  
    listPre.append(line)
  return listPre

def netagMain(argv):
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
    listToTag=createneFile(doc)
    result=""
    for line in listToTag:  
      tokens=line.split()
      currW=tokens[2].split(":")[1]
      currT=tokens[3].split(":")[1]
      maxwtcls = max( setcls , key = lambda cls: sum( [ dictClsWts[cls][token] for token in tokens[0:] if token in dictClsWts[cls]]) )
      result += currW + "/" + currT + "/" + maxwtcls + " "
    print(result)
    sys.stdout.flush()


if __name__=="__main__":
  netagMain(sys.argv[1:])
