from browser import document, ajax, console
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



### For BERT answer ###

def question_json():
    Ticker = document['Ticker'].value
    Year = document['Year'].value
    Quarter = document['Quarter'].value
    question = document['question'].value
    return {'question': str(question), 
            'Ticker': str(Ticker),
            'Year': int(Year),
            'Quarter': int(Quarter)}

def display_text_question(req):
    result = json.loads(req.text)
    # note the syntax for setting the child text of an element
    document['solution'].html = f"{result['answer']}"

def send_question_json(answer):
    req = ajax.Ajax()
    req.bind('complete', display_text_question)
    req.open('POST',
                '/ask',
                True)
    req.set_header('Content-Type', 'application/json')
    req.send(json.dumps(answer))


def ask(event):
    question = question_json()
    send_question_json(question)

document['solve'].bind('click', click)
document['ask'].bind('click', ask)
