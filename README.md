# News-Validator

A news validation bot that tries to predict if a news is real or fake.

## Content:

### Scraper

Scrapes the news from various websites.

### Predictor

Learns from the collected articles and predicts the validity of input.

## Workflow:

### Scraper

The scraper/scraper.py file is the first file that runs. It's objective is to collect database for the model to learn.
It has a dictionary that contains different scraping info from different sites to basically extract Title, Text and Date of the news.
User can select what kind of news and from which website to choose and the category of the news as well (wrold-news, india-news etc).
Once the selections are made, based on the number of articles to fetch from, it'll generate/append this data to an excel file.

The updater.py is supposed to be an automated version of the scraper.py file but is not implimented as of now.

### Predictor

Moving on to predictor/model.py file. It has an SDGClassifier which takes the title and text from data base and then combines them and processes them using nltk library and then finally tranforms the text data into numeric data using TfidfVectorizer from scikit-learn library.
The model is trianed and and then both vectorizer and model are dumped into pickle files.

The predictor.py takes the input string from user, processes them using the saved vectorizer (so that there is no issue of different arguments passed to the TfidfVectorizer) and then loads the saved model and predicts an outcome and prints it.
(side note: Other vectorizers can be used for transformation which won't have the arguments issue, but they could be less efficient/accurate then TfidfVectorizer.)

The api.py uses FastAPI to take inputs from user and give outputs.
