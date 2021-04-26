from math import sqrt
from flask import Flask, render_template, request, jsonify
import requests
from model import *
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('BERT.html')


@app.route('/solve', methods=['POST'])
def solve():
    user_data = request.json
    Ticker, Year, Quarter = user_data['Ticker'], user_data['Year'], user_data['Quarter']
    answer = find_answer(Ticker, Year, Quarter)
    return jsonify({'answer': answer})

@app.route('/ask', methods=['POST'])
def ask():
    user_data = request.json
    ask = user_data['Question']
    EC = user_data['EarningsCall']
    answer = question_answer(EC,ask)
    return jsonify({'answer': answer})

def find_answer(Ticker, Year, Quarter):
    answer_text = call_pull(Ticker, Year, Quarter)
    return answer_text


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
