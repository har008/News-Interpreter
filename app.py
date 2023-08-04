#Importing the Libraries
import numpy as np
from flask import Flask, request,render_template, url_for
from flask_cors import CORS
import pandas as pd
import pickle
import flask
import os
import newspaper
from newspaper import *
import urllib
import nltk
import summ
#Loading Flask and assigning the model variable
app = Flask(__name__)
CORS(app)
app=flask.Flask(__name__,template_folder='templates')

with open('final1.pickle', 'rb') as handle:
	model1 = pickle.load(handle)
with open('final2.pickle', 'rb') as handle:
	model2 = pickle.load(handle)
@app.route('/')
def welcome():
    return render_template('Welcome.html')

@app.route('/Input')
def main():
    return render_template('Input.html')
@app.route('/Result')
def main2():
    return render_template('Result.html')

#Receiving the input url from the user and using Web Scrapping to extract the news content
@app.route('/predict',methods=['GET','POST'])
def predict():
	try:
		url =request.get_data(as_text=True)[5:]
		if url=="":
			return render_template('Input.html',prediction_text='')    
		url = urllib.parse.unquote(url)
		article = Article(str(url))
		article.download()
		article.parse()
		article.nlp()
		news = article.text
		title = article.title
			    #Passing the news article to the model and returing whether it is Fake or Real
		pred1 = model1.predict([news])
		pred2 = model2.predict([news])
		if pred1[0]=='tech':
			pred1[0]='TECHNOLOGY'
		elif pred1[0]=='sport':
			pred1[0]='SPORTS'
		elif pred1[0]=='crime':
			pred1[0]='CRIME'
		elif pred1[0]=='business':
			pred1[0]='BUSINESS'
		elif pred1[0]=='politics':
			pred1[0]='POLITICS'
		elif pred1[0]=='entertainment':
			pred1[0]='ENTERTAINMENT'

		if request.form.get('Number'):
			number=request.form['Number']
			number = int(number)
			body=summ.GetText(title,news,number)
			return render_template('Result.html',prediction_text1='The news is {}'.format(pred2[0]),prediction_text2='{}'.format(pred1[0]),summary_text=body)
		return render_template('Result.html',prediction_text1='The news is {}'.format(pred2[0]),prediction_text2='{}'.format(pred1[0]))
	except:
		return render_template('Input.html',prediction_text='Please Enter a Valid URL')

@app.route('/predict2', methods=['POST'])
def predict2():
    text = request.form['news']
    pred1 = model1.predict([text])
    pred2 = model2.predict([text])
    return render_template('Result.html',prediction_text1='The news is {}'.format(pred2[0]),prediction_text2='{}'.format(pred1[0]))


if __name__=="__main__":
    port=int(os.environ.get('PORT',5000))
    app.run(port=port,debug=True,use_reloader=False)