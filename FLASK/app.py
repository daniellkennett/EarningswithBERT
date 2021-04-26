from math import sqrt
from flask import Flask, render_template, request, jsonify
import requests
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('BERT.html')

def call_pull(ticker, year, quarter,key = 'e46f1a303dafb62460de104424a00084'):
    try:
        transcript = requests.get(f'https://financialmodelingprep.com/api/v3/earning_call_transcript/{ticker}?quarter={quarter}&year={year}&apikey={key}').json()
        tran = transcript[0]['content']
        date = transcript[0]['date']
        return tran
    except:
        pass
    
def clean_text(ticker, year, quarter):
    tran= call_pull(ticker, year, quarter)
    dialogue = tran.split('Operator:')[2:-1]
    
    dialogue = 'operator:'.join(dialogue)
    if "\n" in dialogue:
        dialogue = dialogue.split('\n')
        for dia in dialogue:
            # if dia.endswith('?'):
            #     dialogue.remove(dia)
            if 'Operator' or 'operator:' in dia:
                dialogue.remove(dia)
        return dialogue
    else:
        dialogue = dialogue.split('.')
        print(dialogue)
        for dia in dialogue:
            if dia.endswith('?'):
                dialogue.remove(dia)
            if 'Operator' or 'operator:' in dia:
                dialogue.remove(dia)
        dialogue = '.'.join(dialogue)
        return dialogue

def get_answer_long(answer_text_list, question):
  
  answer_list=[]
  start=[]
  end= []
  for text in answer_text_list:
    try:

      input_ids = tokenizer.encode(question, text)
      tokens = tokenizer.convert_ids_to_tokens(input_ids)

      sep_index = input_ids.index(tokenizer.sep_token_id)
      num_seg_a = sep_index + 1
      num_seg_b = len(input_ids) - num_seg_a
      segment_ids = [0]*num_seg_a + [1]*num_seg_b
      assert len(segment_ids) == len(input_ids)

      outputs = model(torch.tensor([input_ids]), # The tokens representing our input text.
                                  token_type_ids=torch.tensor([segment_ids]), # The segment IDs to differentiate question from answer_text
                                  return_dict=True) 

      start_scores = outputs.start_logits
      end_scores = outputs.end_logits

      answer_start = torch.argmax(start_scores)
      answer_end = torch.argmax(end_scores)

      answer = ' '.join(tokens[answer_start:answer_end+1])

      answer_list.append(answer)
      start.append(start_scores[0][answer_start])
      end.append(end_scores[0][answer_end])
      print(answer)
    except:
      continue

  return answer_list[torch.argmax(torch.tensor(start))]

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
    answer = get_answer_long(EC,ask)
    return jsonify({'answer': answer})

def find_answer(Ticker, Year, Quarter):
    answer_text = clean_text(Ticker, Year, Quarter)
    return answer_text


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
