from browser import document, ajax
import json

def get_input_answer():
### Input gets passed through this funciton ###
    Ticker = document['Ticker'].value
    Year = document['Year'].value
    Quarter = document['Quarter'].value

    return {'Ticker': str(Ticker),
            'Year': int(Year),
            'Quarter': int(Quarter)}


def display_text(req):
    result = json.loads(req.text)
    # note the syntax for setting the child text of an element
    document['text'].html = f"{result['answer']}"

def send_answer_json(answer):
    req = ajax.Ajax()
    req.bind('complete', display_text)
    req.open('POST',
                '/solve',
                True)
    req.set_header('Content-Type', 'application/json')
    req.send(json.dumps(answer))

def click(event):
    ### Runs get_input_answer
    
    answer = get_input_answer()
    send_answer_json(answer)
    del document['hidden_layer'].attrs['hidden']

def question_json(event):
    question = document['question'].value
    EC = document['text'].html
    return {'Question': question, 'EarningsCall': EC}

def ask(answer):
    answer = get_input_answer()
    send_answer_json(answer)

document['solve'].bind('click', click)
document['ask'].bind('click', ask)
