import sys, os, glob, re, copy

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

def extractEntitiesFromFile(fileName):
  iFile=open(fileName,'r',errors='ignore')
  #iFile=open(fileName,'r',errors='ignore')
  data=iFile.read()
  iFile.close()
  tokens=data.split()  ## this takes care of all the \n and whitespaces.

  ## represent entity as [ list_of_all_words_in_entity, start_token_idx, end_token_idx, entityType]
  ## entList = list of all entity in the file
  entList=[]  

  currEntityTokenList = []
  currStartIdx= 0
  currEndIdx = 0
  currEntityType = None
  isEntityRunning = False

  for i in range(0, len(tokens)):
    tok = tokens[i]
    word, posTag, nerTag = processToken(tok)

    ## Firstly ignore the O
    if nerTag == 'O':
      continue

    if nerTag[:2] == 'B-':
      ## Begin a new entity
      isEntityRunning = True
      currEntityType = nerTag[2:]
      currEndIdx = i
      currStartIdx = i
      currEntityTokenList = [ tok ]
    
    if nerTag[:2] == 'I-':
      ### Entity is continued only when isEntityRunning is set True
      if isEntityRunning:
        currEndIdx = i
        currEntityTokenList.append( tok )

    #### Now look at the next tok and just to see whether you need to end this entity or not.
    #### If you need to end it then end it and add to the entityList and reset everything.
    toEnd = False
    if i == len(tokens):
      toEnd = True
    else:
      nextTok = tokens[i+1]
      n_word, n_posTag, n_nerTag = processToken(nextTok)
      if n_nerTag != 'I-' + str(currEntityType):
        toEnd = True
    if toEnd and isEntityRunning:
      isEntityRunning = False
      entity = (copy.deepcopy(currEntityTokenList), currStartIdx, currEndIdx, currEntityType)
      entList.append(entity)
      currEntityTokenList = []
      ## These are not required  but doing it for sanity
      currEntityType = None
      currStartIdx = -1
      currEndIdx = -1
      
  #print(entList)
  return entList

def matchEntitiesInFile(entityList, fileName):
  """
    This function takes preExtracted entities and a new file. 
    Its task is to find the entities in the list in file. If they are found it updates the entities last bit from 0 to 1.
  """

  iFile=open(fileName,'r', errors='ignore')
  #iFile=open(fileName,'r',errors='ignore')
  data=iFile.read()
  iFile.close()
  tokens=data.split()  ## this takes care of all the \n and whitespaces.
  entMatch = []
  for entity in entityList:
    entityTokenList, startIdx, endIdx, entityType = entity
    same = True
    for i in range(startIdx, endIdx+1): #endIdx is inclusive
      if tokens[i] != entityTokenList[ i - startIdx]:
        same = False
        break
    if not same:
      entMatch.append( (entityTokenList, startIdx, endIdx, entityType, 0) )
    else:
      entMatch.append( ( entityTokenList, startIdx, endIdx, entityType, 1 ))

 # print entMatch
  return entMatch
  

def main():
  trueFile=sys.argv[1]
  guessedFile=sys.argv[2]
  #call above func on true and guess files and get matching numbers    
  entityList = extractEntitiesFromFile(guessedFile)
  mList=matchEntitiesInFile(entityList, trueFile)
  labelLOC="LOC"
  labelORG="ORG"
  labelPER="PER"
  labelMISC="MISC"

  tLOC= list(filter(lambda x: x[3]=='LOC',mList))
  tORG=list(filter(lambda x: x[3]=='ORG',mList))
  tPER=list(filter(lambda x: x[3]=='PER',mList))
  tMISC=list(filter(lambda x: x[3]=='MISC',mList))
  tALL= len(tLOC) + len(tORG) + len(tPER) + len(tMISC)

  mLOC = list(filter(lambda x: x[3]=='LOC' and x[4]==1,mList))
  mORG = list(filter(lambda x: x[3]=='ORG' and x[4]==1,mList))
  mPER = list(filter(lambda x: x[3]=='PER' and x[4]==1,mList))
  mMISC = list(filter(lambda x: x[3]=='MISC' and x[4]==1,mList))
  mALL = list(filter(lambda x: x[4]==1,mList))

  precLOC = len(mLOC)/len(tLOC)
  precORG = len(mORG)/len(tORG)
  precPER = len(mPER)/len(tPER)
  precMISC = len(mMISC)/len(tMISC)
  precALL = len(mALL)/tALL

  rentityList = extractEntitiesFromFile(trueFile)
  rmList=matchEntitiesInFile(rentityList, guessedFile)

  rtLOC= list(filter(lambda x: x[3]=='LOC',rmList))
  rtORG=list(filter(lambda x: x[3]=='ORG',rmList))
  rtPER=list(filter(lambda x: x[3]=='PER',rmList))
  rtMISC=list(filter(lambda x: x[3]=='MISC',rmList))
  rtALL = len(rtLOC) + len(rtORG) + len(rtPER) + len(rtMISC)

  rmLOC = list(filter(lambda x: x[3]=='LOC' and x[4]==1,rmList))
  rmORG = list(filter(lambda x: x[3]=='ORG' and x[4]==1,rmList))
  rmPER = list(filter(lambda x: x[3]=='PER' and x[4]==1,rmList))
  rmMISC = list(filter(lambda x: x[3]=='MISC' and x[4]==1,rmList))
  rmALL = list(filter(lambda x: x[4]==1,rmList))

  recLOC = len(rmLOC)/len(rtLOC)
  recORG = len(rmORG)/len(rtORG)
  recPER = len(rmPER)/len(rtPER)
  recMISC = len(rmMISC)/len(rtMISC)
  recALL =len(rmALL)/rtALL

  fLOC= (2*precLOC*recLOC)/(precLOC+recLOC)
  fORG = (2*precORG*recORG)/(precORG+recORG)
  fPER= (2*precPER*recPER)/(precPER+recPER)
  fMISC= (2*precMISC*recMISC)/(precMISC+recMISC)
  fALL = (2*precALL*recALL)/(precALL+recALL)

  print("prec of LOC:" + str(precLOC))
  print("prec of ORG:" + str(precORG))
  print("prec of PER:" + str(precPER))
  print("prec of MISC:" + str(precMISC))
  print("prec of ALL:" + str(precALL))

  print("rec of LOC:" + str(recLOC))
  print("rec of ORG:" + str(recORG))
  print("rec of PER:" + str(recPER))
  print("rec of MISC:" + str(recMISC))
  print("rec of ALL:" + str(recALL))


  print("f score of LOC:"+ str(fLOC))
  print("f score of MISC:"+ str(fMISC))
  print("f score of ORG:"+ str(fORG))
  print("f score of PER:"+ str(fPER))
  print("f score of ALL:"+ str(fALL))
if __name__=="__main__":
  main()
