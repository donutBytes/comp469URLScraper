"""
Alexander Bickham
Comp 469: Final Project

Project Poposal:

I propose to use Natural Language processing to extract key points from a webpage by url (i.e.
summary, bullets, intro). I will be using python and a python library called Natural Language Toolkit.
(https://www.nltk.org/)

What I have:

Python Flask server bringing up a webpage that allows the user to either a url to scrape text off and create a 
word cloud or to enter text and create a word cloud using that

run 'python main.py'
Click the localhost url  
README.md coming soon
"""

'''Imports'''
import argparse
import requests
from bs4 import BeautifulSoup
import json
import nltk
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
# nltk.download('averaged_perceptron_tagger')


'''Start of Flask server setup'''
import sys

from flask import Flask, render_template, request, redirect, Response, abort, jsonify

app = Flask(__name__, template_folder='template')

@app.route('/')
def output():
	# serve index template
	return render_template('index.html', name='Joe')

def getTokens(paragraphs):
    '''Storing the contents from the page in json'''
    data = {
        'commonWords': {}
    }
    words = []
    # print (paragraphs)
    for a in paragraphs:
        if type(a) is not unicode:
            content = a.text.strip()
        else:
            content = a
        # data['paragraphs'][a] = content
        tokens = tokenizer.tokenize(content)
        words = words + tokens        
        # text = nltk.Text(tokens)

    fdist = FreqDist()
    for word in words:
        # print word
        if word.isalpha:
            fdist[word.lower()] += 1 
    
    for word in fdist:
        # print word
        if word.isalpha and fdist[word] > 1:
            data['commonWords'][str(unicode(word))] = fdist[word]

    return data

@app.route('/tokens', methods = ['GET'])
def tokens():
    paragraphs = request.args.get('paragraphs')
    return jsonify(getTokens([paragraphs]))

'''Function to curl url and parse through the body text to return useful information'''
@app.route('/receiver', methods = ['GET'])
# @app.route('/receiver', methods = ['POST'])
def hitUrl():
    print 'Entering the Matrix...'
    url = request.args.get('url')
    print url
    try:
        print url, '\n'
        response = requests.get(url)
    except:
        print 'This URL is not valid'
        abort(401)
        exit(1)

    '''Parsing through the page's HTML and extracts paragraph tags'''
    raw = response.content
    html = BeautifulSoup(raw,'html.parser')
    paragraphs = html.select('body p')

    print paragraphs[0]
    data = getTokens(paragraphs)
    return jsonify(data)

if __name__ == '__main__':
	# run!
    app.run(debug=True)
'''End of flask server setup'''
