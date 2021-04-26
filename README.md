# Earnings with Bert

1. What is Bert
2. Finetuning dataset
3. In practice - data
4. Problems with BERT
5. Final





### 1. What is Bert

In 2018, Google's research labs introduced a new model with unique techniques called Bert, Bidirectional Encoder Representations from Transformers. This NLP bot was trained on every English Wikipedia page, as well as, a corpus of 10,000 books. This training created a corpus of over 110 million tokens. Google implemented Bert in 2019 to it's search engine to derive context and meaning from longer queries. The model has a great understanding of the English language and can be fine tuned for many different purposes.

#### How does it work?

* Bidirectionally - 
Bert is bidirectionally trained, meaning that language passed through is trained left to right and left to right. This gives the model a deeper understanding of the language. 

* Transformers - 
From the Google research paper that was released with the model:
"As opposed to directional models, which read the text input sequentially (left-to-right or right-to-left), the Transformer encoder reads the entire sequence of words at once. Therefore it is considered bidirectional, though it would be more accurate to say that it’s non-directional. This characteristic allows the model to learn the context of a word based on all of its surroundings (left and right of the word)."

* Masked Language Model - 
To train, Bert is given sentences with 15% of words replaced with the [Mask] tag. The model predicts the words and then compares it to the actual answer. 

* Next Sentence Prediction - 
The model is also trained by providing two sentences of a time. 50% of the time the sentences are sequential. 50% they are random. The model needs to predict the randomness of the secon sentence. This technique holds the largest weight for QA because we will fine-tune Bert by setting the question as sentence 1. It will assign scores to every sentence 2.


### Finetuning with SQuAD
the Stanford Question Answering Dataset is a collection of 100,000 question and answer pairs. Bert takes in the question, a contextual passage and predicts the answer. Bert uses the the logliklihoods to determine start and end postitions of answers.


Softmax logloss to measure performance-
$ log(softmax(CW^T)) $


### In Practice
INSERT SITE HERE

Once trained on the Stanford set, the model can take in any set of question and paragraph and derive 


### Problems with BERT

By design of how BERT was trained, the model can only take up to 512 parameters. To avoid this, I created a system to chop Earning Reports into small sections. These smaller sections will incorporate 25% of the section before to maintain conversational context. Otherwise BERT would lose that and the model would be missing valuable information. 


### In Practice

Final model




