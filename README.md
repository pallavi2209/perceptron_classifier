# README #
The assignment consists of three parts:
1. Average Perceptron Classifier:
The code contains two files: perceplearn.py and percepclassify.py
perceplearn.py takes in the training file and model file name (as output). There is an optional argument also, -h to give dev file as an input. The syntax to run the code is:
python3 perceplearn.py [TRAINING FILE] [MODEL FILE] [-h DEV FILE]
Example: python3 perceplearn.py spam_train spam.model
Example: python3 perceplearn.py spam_train spam.model -h spam_dev

percepclassify.py takes in model file and test file (using STDIN) and gives output tagged file.The syntax to run the code is:
python3 percepclassify.py [MODEL FILE] < [TEST FILE] > [OUTPUT FILE]
Example: python3 percepclassify.py spam.model < spam.test > spam.out

2. Part of Speech Tagging
The code contains two files: postrain.py and postag.py
postrain.py takes in the training file and model file name (as output). There is an optional argument also, -h to give dev file as an input. The syntax to run the code is:
python3 postrain.py [TRAINING FILE] [MODEL FILE] [-h DEV FILE]
Example: python3 postrain.py pos.train pos.model
Example: python3 postrain.py pos.train pos.model -h pos.dev

postag.py takes in model file and test file (using STDIN) and gives output tagged file.The syntax to run the code is:
python3 postag.py [MODEL FILE] < [TEST FILE] > [OUTPUT FILE]
Example: python3 postag.py pos.model < pos.test > pos.test.out

2. Named Entity Recognition
The code contains two files: nelearn.py and netag.py
nelearn.py.py takes in the training file and model file name (as output). There is an optional argument also, -h to give dev file as an input. The syntax to run the code is:
python3 nelearn.py [TRAINING FILE] [MODEL FILE] [-h DEV FILE]
Example: python3 nelearn.py ner.esp.train ner.model
Example: python3 nelearn.py ner.esp.train ner.model -h ner.esp.dev

netag.py takes in model file and test file (using STDIN) and gives output tagged file.The syntax to run the code is:
python3 netag.py [MODEL FILE] < [TEST FILE] > [OUTPUT FILE]
Example: python3 netag.py ner.model < ner.esp.test > ner.esp.test.out


ANSWER 1:
Accuracy of your part-of-speech tagger: I did 20 iterations and got the results as follows for dev data:
Iteration 0 with Accuracy:0.941720
Iteration 1 with Accuracy:0.945185
Iteration 2 with Accuracy:0.949872
Iteration 3 with Accuracy:0.947080
Iteration 4 with Accuracy:0.954259
Iteration 5 with Accuracy:0.954234
Iteration 6 with Accuracy:0.953536
Iteration 7 with Accuracy:0.954483
Iteration 8 with Accuracy:0.953611
Iteration 9 with Accuracy:0.954159
Iteration 10 with Accuracy:0.956427
Iteration 11 with Accuracy:0.954658
Iteration 12 with Accuracy:0.953661
Iteration 13 with Accuracy:0.955854
Iteration 14 with Accuracy:0.956951
Iteration 15 with Accuracy:0.955729
Iteration 16 with Accuracy:0.955306
Iteration 17 with Accuracy:0.955356
Iteration 18 with Accuracy:0.955929
Iteration 19 with Accuracy:0.950869
Model with Accuracy:0.956951 is stored as pos.model

Maximum accuracy: 0.956951


ANSWER 2:
Fscore for LOC: 0.5645
Fscore for ORG: 0.4967
FScore for PER: 0.5678
FScore for MISC: 0.5234
Overall FScore: 0.5564 

ANSWER3:
In case of POS tagging, Naive Bayes Classifier gives an accuracy : 0.9373 as compared to the accuracy of 0.95695 in case of perceptron. (DECREASED)
Reason:
I believe the the decrease in accuracy is because Naive Bayes considers the features as bag of words. It assumes the words are independent and hence it does not considers the context of a word in regard to surrounding words. Perceptron handles this case very well, since it taken in the features corresponding to surrounding words also. This enable perceptron to increase the accuracy in case of POS tagging and NER tagging.

