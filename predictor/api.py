from fastapi import FastAPI
from pydantic import BaseModel
from pickle import load
import json
import re
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

app = FastAPI()

class model_input(BaseModel):

    News_Title : str
    News_Body : str

news_model = load(open("model.pkl", "rb"))

@app.post('/news_validator') #In point
def news_valid(input_parameters : model_input):

    input_data = input_parameters.json()
    input_dictionary = json.loads(input_data)

    title = input_dictionary["News_Title"]
    body = input_dictionary["News_Body"]

    input_list = [title, body]

    input_string = "".join(input_list)

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

    processed_input = [stemming(input_string)]

    vectorizer = load(open('vectorizer.pkl', "rb"))

    processed_input = vectorizer.transform(processed_input)

    predictor = load(open("model.pkl", "rb"))

    if predictor.predict(processed_input) == 1:
        return "The news is most certainly TRUE."
    else:
        return "The news is probably FAKE or has been manipulated. Fact checking is recommended."