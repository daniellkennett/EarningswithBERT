import json
import os
import re
import string
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow import keras
from tensorflow.keras import layers
from tokenizers import BertWordPieceTokenizer
from data_gather import *

max_seq_length = 384
bert_layer = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/2", trainable=True)
vocab_file = bert_layer.resolved_object.vocab_file.asset_path.numpy().decode("utf-8")
tokenizer = BertWordPieceTokenizer(vocab=vocab_file, lowercase=True)
# model = keras.models.load_model('../model')



def preprocess(context, question):
  start_token_idx = -1
  end_token_idx = -1
  context = " ".join(str(context).split())
  question = " ".join(str(question).split())
  # tokenize context and question
  tokenized_context = tokenizer.encode(context)
  tokenized_question = tokenizer.encode(question)


  input_ids = tokenized_context.ids + tokenized_question.ids[1:]
  token_type_ids = [0] * len(tokenized_context.ids) + [1] * len(tokenized_question.ids[1:])
  attention_mask = [1] * len(input_ids)
  padding_length = max_seq_length - len(input_ids)
        # add padding if necessary
  if padding_length > 0:
    input_ids = input_ids + ([0] * padding_length)
    attention_mask = attention_mask + ([0] * padding_length)
    token_type_ids = token_type_ids + ([0] * padding_length)
  return input_ids, token_type_ids, attention_mask, start_token_idx, end_token_idx, tokenized_context.offsets

def create_inputs(squad_examples):
    dataset_dict = {
        "input_word_ids": [],
        "input_type_ids": [],
        "input_mask": [],
        "start_token_idx": [],
        "end_token_idx": [],
    }
    dataset_dict['input_word_ids'] = squad_examples[0]
    dataset_dict['input_type_ids'] = squad_examples[1]
    dataset_dict['input_mask'] = squad_examples[2]
    dataset_dict['start_token_idx'] = squad_examples[3]
    dataset_dict['end_token_idx'] = squad_examples[4]

    for key in dataset_dict:
        dataset_dict[key] = np.array([dataset_dict[key]])
    x = [dataset_dict["input_word_ids"],
         dataset_dict["input_mask"],
         dataset_dict["input_type_ids"]]
    y = [dataset_dict["start_token_idx"], dataset_dict["end_token_idx"]]
    return x, y


def question_answer(ticker, year, quarter, question):
  # transcript = get_split(ticker, year, quarter)
  # answers = []
  # scores = []

  # for dialogue in transcript:

  #   test_samples = preprocess(dialogue, question)[:5]
  #   x, _ = create_inputs(test_samples)
  #   pred_start, pred_end = model.predict(x)
  #   for idx, (start, end) in enumerate(zip(pred_start, pred_end)):
  #     test_sample = test_samples[idx]
  #     offsets = preprocess(dialogue, question)[-1]
  #     ### Use largest start to determine right answer ###
  #     score = max(start)
  #     start = np.argmax(start)
  #     end = np.argmax(end)
  #     pred_ans = None
  #     if start >= len(offsets):
  #         continue
  #     pred_char_start = offsets[start][0]
  #     if end < len(offsets):
  #         pred_ans = dialogue[pred_char_start:offsets[end][1]]
  #     else:
  #         pred_ans = dialogue[pred_char_start:]
  #     answers.append(pred_ans)
  #     scores.append(score)

  #     # print("Q: " + question)
  #     # print("A: " + pred_ans)



  # return answers[np.argmax(scores)]
  return "Galvanize is awesome"


if __name__ == "__main__":
  trigger = True
  print('Welcome to Earnings With BERT!')
  company = input('Enter company ticker: ')
  year = input("Enter year: ")
  qtr = input("Enter quarterly report: ")
  question = input("What is your question? ")
  print(question_answer(company, year, qtr, question))
  while trigger == True:
    done = input('Any other questions? ')
    if done == 'yes' or done =='Yes':
      question = input("What is your question? ")
      print(question_answer(company, year, qtr, question))
    else:
      trigger = False