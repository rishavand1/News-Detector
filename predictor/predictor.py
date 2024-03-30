import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from pickle import load

X = str(input("Enter the news article text here: "))

port_stem = PorterStemmer()


def stemming(content):
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


X_new = [stemming(X)]

vectorizer = load(open('vectorizer.pkl', "rb"))

X_new = vectorizer.transform(X_new)

predictor = load(open("model.pkl", "rb"))

if predictor.predict(X_new) == 1:
    print("The news is most certainly TRUE.")
else:
    print("The news is probably FAKE or has been manipulated. Fact checking is recommended.")
