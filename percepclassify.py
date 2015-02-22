import sys
import argparse
from decimal import Decimal
import copy
import random
import pickle
def perceptClassifyMain(argv):
  parser = argparse.ArgumentParser(add_help=False)
  parser.add_argument("modelFile")
  args = parser.parse_args(argv)
  mdfname=args.modelFile
  
  with open(mdfname,"rb") as handle:
    data=pickle.load(handle)

  dictClsWts=data["wDict"]
  setcls = data["setcls"]
  for line in sys.stdin:
    tokens=line.split()
    maxwtcls = max( setcls , key = lambda cls: sum( [ dictClsWts[cls][token] for token in tokens[1:] if token in dictClsWts[cls]]) )
    print(maxwtcls)
    sys.stdout.flush()    
  
 
if __name__=="__main__":
  perceptClassifyMain(sys.argv[1:])
