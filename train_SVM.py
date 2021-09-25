import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, naive_bayes, svm
from sklearn.metrics import accuracy_score
import pickle

Corpus = pd.read_csv("test.csv", encoding='utf-8')

# Step - a : Remove blank rows if any.
Corpus['content'].dropna(inplace=True)

# Step - b : Change all the text to lower case. This is required as python interprets 'dog' and 'DOG' differently
Corpus['content'] = [entry.lower() for entry in Corpus['content']]

# Step - c : Tokenization : In this each entry in the corpus will be broken into set of words
Corpus['content']= [word_tokenize(entry) for entry in Corpus['content']]

for index,entry in enumerate(Corpus['content']):
    Corpus.loc[index,'text_final'] = str(Corpus['content'][index])

Train_X, Test_X, Train_Y, Test_Y = model_selection.train_test_split(Corpus['text_final'],Corpus['label'],test_size=0.3)

Encoder = LabelEncoder()
Train_Y = Encoder.fit_transform(Train_Y)
Test_Y = Encoder.fit_transform(Test_Y)

Tfidf_vect = TfidfVectorizer(max_features=5000)
Tfidf_vect.fit(Corpus['text_final'])
Train_X_Tfidf = Tfidf_vect.transform(Train_X)
Test_X_Tfidf = Tfidf_vect.transform(Test_X)

# print(Tfidf_vect.vocabulary_)

# print(Train_X_Tfidf)

# Classifier - Algorithm - SVM
# fit the training dataset on the classifier
SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
SVM.fit(Train_X_Tfidf,Train_Y)
# predict the labels on validation dataset
predictions_SVM = SVM.predict(Test_X_Tfidf)
# Use accuracy_score function to get the accuracy
print("SVM Accuracy Score -> ",accuracy_score(predictions_SVM, Test_Y)*100)

# saving encoder to disk
filename = 'save/labelencoder_fitted.pkl'
pickle.dump(Encoder, open(filename, 'wb'))

# saving TFIDF Vectorizer to disk
filename = 'save/Tfidf_vect_fitted.pkl'
pickle.dump(Tfidf_vect, open(filename, 'wb'))

# saving the both models to disk
filename = 'save/svm_trained_model.sav'
pickle.dump(SVM, open(filename, 'wb'))

# 97.27