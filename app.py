import streamlit as st
from streamlit_chat import message
import requests
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

data=pd.read_csv('data.csv')

sentence_list= data['Question'].to_list()

def greeting_response(text):
    text = text.lower()
    
    bot_greetings = ['howdy', 'hi', 'hey', 'hello', 'hola']
    
    user_greetings = ['hi', 'hey', 'hello', 'hola', 'greetings', 'wassup']
    
    for word in text.split():
        if word in user_greetings:
            return random.choice(bot_greetings)

def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(0,length))
    
    x = list_var
    
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp
    return list_index

def bot_response(user_input):
    user_input = user_input.lower()
    sentence_list.append(user_input)
    bot_response = ''
    cm = CountVectorizer().fit_transform(sentence_list)
    similarity_scores = cosine_similarity(cm[-1], cm)
    similarity_scores_list = similarity_scores.flatten()
    index = index_sort(similarity_scores_list)

    
    
    if similarity_scores_list[[index[0]]] == similarity_scores_list[[index[1]]]:
        if similarity_scores_list[[index[0]]] > 0.3:
            bot_response = bot_response+' '+data['Answer'][index[0]]
    
        else:
            bot_response = bot_response+' '+"I apologize, I don't understand."
    else:
        if similarity_scores_list[[index[1]]] > 0.3:
            bot_response = bot_response+' '+data['Answer'][index[1]]
    
        else:
            bot_response = bot_response+' '+"I apologize, I don't understand."
        
    sentence_list.remove(user_input)
    
    return bot_response

st.header("Psychologist Chatbot demo")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def get_text():
    input_text = st.text_input('Your question: ', key="input")
    return input_text 


user_input = get_text()

if user_input:
    if greeting_response(user_input) != None:
        output = greeting_response(user_input)
    else:
        output = bot_response(user_input)

    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')


message('I am Psychologist Bot or Psy Bot for short. I will answer your queries about mental health.')
