from flask import Flask, render_template, url_for, request, redirect
from tensorflow import keras
import pandas as pd
import numpy as np
from scrapping import get_comments
from preprocess import clean, tokenize, remove_blanks

app = Flask(__name__)
app.debug = True

model = keras.models.load_model('polarity_class_model')

@app.route('/')
def home():
    """
    Home page route
    """
    return render_template('index.html')

@app.route('/', methods=['POST'])
def scrap():
    """
    POST request
    """
    if request.method == "POST":
        link = request.form.get('url')
        if link:
            #try:
            get_comments(link)
            comments = pd.read_csv('results.csv', sep = ",", encoding='utf-8', quotechar='"', engine='python')
            clean_comments = [clean(t) for t in comments]
            clean_comments = remove_blanks(clean_comments)
            clean_comments = [' '.join(t) for t in clean_comments]
            print("Num. com:", len(clean_comments))
            token = tokenize(clean_comments)[2]
            print("SHAPE:", token.shape)
            prediction = model.predict(token)
            prediction = [np.argmax(c) for c in prediction]
            pd.DataFrame(comments, prediction).to_csv('SCRAPED.csv')
            return render_template('index.html', comments=comments, prediction=prediction)
            # except:
            #     message = "Soemething went wrong with the WebBrowser. Try again."
            #     return render_template('index.html', err_msg=message)
        else:
            message = "Insert the link"
            return render_template('index.html', err_msg=message)

if __name__ == "__main__":
    app.run()