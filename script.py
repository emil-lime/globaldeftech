from flask import Flask, render_template, url_for, request, redirect
from tensorflow import keras
import pandas as pd
import numpy as np
from scraping import get_comments
from preprocess import clean, tokenize, remove_blanks
from visualize import word_cloud, pie_chart
import os

app = Flask(__name__)
app.debug = True

#Попытки разобраться с проблемой кэша.
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'plots')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

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
            try:
                
                #Берёт комментарии
                df = get_comments(link)
                comments = df["Comments"]
                df.to_csv('test.csv')
                
                
                #comments = pd.read_csv('results.csv', sep = ",", encoding='utf-8', quotechar='"', engine='python')
                #df = pd.read_csv('test.csv')
                
                #Очищается текст
                comments = list(df['Comments'])
                clean_comments = [clean(t) for t in comments]
                #print(clean_comments)
                clean_comments = remove_blanks(clean_comments)
                clean_comments = [' '.join(t) for t in clean_comments]
                #print("Num. com:", len(clean_comments))
                
                #Преобразование в векторы
                token = tokenize(clean_comments)[2]
                #print("SHAPE:", token.shape)
                
                #Модель предсказывает
                prediction = model.predict(token)
                prediction = [np.argmax(c) for c in prediction]
                
                #Cоздаётся отдельная таблица для визуализаций
                pred_df = pd.DataFrame(list(zip(clean_comments, prediction)), columns=["clean_comment","label"])
                pred_df.to_csv('SCRAPED.csv')
                
                #Word Cloud
                pos_words =' '.join([text for text in pred_df['clean_comment'][pred_df['label'] == 2]]) 
                neg_words =' '.join([text for text in pred_df['clean_comment'][pred_df['label'] == 0]]) 
                neut_words =' '.join([text for text in pred_df['clean_comment'][pred_df['label'] == 1]]) 
                word_cloud(pos_words, "positive")
                word_cloud(neut_words, "neutral")
                word_cloud(neg_words, "negative")
                
                #Pie Chart
                pie_chart(pred_df)
                #print("CLEAN:", clean_comments[0])
                return render_template('index.html', comments=comments, prediction=prediction)
            except:
                message = "Soemething went wrong with the WebBrowser. Try again."
                return render_template('index.html', err_msg=message)
        else:
            message = "Insert the link"
            return render_template('index.html', err_msg=message)

if __name__ == "__main__":
    app.run()
