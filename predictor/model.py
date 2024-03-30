import numpy as np
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score
from pickle import dump, load

# Download stopwords like []'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd"]

nltk.download('stopwords')

# print(stopwords.words('english'))

# Loading the data from news database made by scraper

news_dataset = pd.read_excel('news.xlsx')

# print(news_dataset)

# Replacing empty spaces with nulls

news_dataset = news_dataset.fillna('')

# Creating content by joining news "Title" and "Text" columns

news_dataset['content'] = news_dataset["Title"] + ' ' + news_dataset["Text"]

# print(news_dataset['content'])

# Separating data and labels

X = news_dataset.drop(columns='TorF', axis=1)
Y = news_dataset['TorF']

# print(X)
# print(Y)

port_stem = PorterStemmer()


def stemming(content):

    # Function to stem the content (make the data uniform and convert all the words to the words they stem from)
    # Driver, Driving -> Drive
    # Typist, Typer, Typing -> Type

    stemmed_content = re.sub('[^0-9a-zA-Z]', ' ', content)
    stemmed_content = stemmed_content.lower()
    stemmed_content = stemmed_content.split()
    stemmed_content = [
        port_stem.stem(word)
        for word in stemmed_content
        if word not in stopwords.words('english')
    ]
    stemmed_content = ' '.join(stemmed_content)
    return stemmed_content


# Applying stemming to the content

news_dataset['content'] = news_dataset['content'].apply(stemming)

# print(news_dataset['content'])

# Assigning data and lables to spearate variables

X = news_dataset['content'].values
Y = news_dataset['TorF'].values

# print(X)
# print(Y)

# Converting text into numerical values

vectorizer = TfidfVectorizer()
vectorizer.fit(X)

# Transforming text to numeric values

X = vectorizer.transform(X)

# print(X)

# Splitting database into testing and training data

X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, stratify=Y, random_state=5)

# Training the model SGDClassifier

# loss="hinge" gives a linear SVM.
# penalty="l2" is default value and is a regulization term. ()"Try l1 in future").
# fit_intercept="True" is whether the intercept should be estimated or not.
# shuffle="True" is whether or not the training data should be shuffled after each epoch.

model = SGDClassifier(loss='hinge', penalty='l2',
                      fit_intercept=True, shuffle=True)

# Fitting the data in the model

# Using fit will overwrite the previous weights on each epoch
# Partial fit enables fitting new data to the previously trained model

model.partial_fit(X_train, Y_train, classes=np.unique(Y))

# Training the model with training data and printing it's accuracy on training data

X_train_prediction = model.predict(X_train)
training_data_accuracy = accuracy_score(X_train_prediction, Y_train)

print('Accuracy score of the training data : ', training_data_accuracy)

# Testing the model with testing data and printing it's accuracy on test data

X_test_prediction = model.predict(X_test)
test_data_accuracy = accuracy_score(X_test_prediction, Y_test)

print('Accuracy score of the test data : ', test_data_accuracy)

# Saving the model (Pickling) so that it can be used to predict data or trained with new data

dump(model, open("model.pkl", "wb"))

# Saving the transformer (text to numeric) method so that new data for training or prediction could have the same attributes as previous data

dump(vectorizer, open('vectorizer.pkl', "wb"))
