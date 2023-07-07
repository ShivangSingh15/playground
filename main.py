import streamlit as st

from streamlit_chat import message

import requests
import json
import os

import openai,os
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv

from dotenv import load_dotenv

load_dotenv()

# openai.log=None

# openai.api_type = "azure"

# openai.api_version = "2023-03-15-preview"

# openai.api_base = os.getenv("OPENAI_ENDPOINT")

openai.api_key = os.getenv("OPENAI_API_KEY1")

# openai.api_key=os.getenv("ES_API_KEY")

# openai.api_type = "azure"

# openai.api_base = os.getenv("OPENAI_API_BASE")

# openai.api_version = "2023-03-15-preview"

# openai.api_key = os.getenv("AZURE_API_KEY")

st.title("Azure GPT4 playground")

def api_endpoint(audio_file_input):

    # Add your code logic here

    print('GET request received')

    url = 'http://127.0.0.1:5000/transcribe'  # Replace with the URL of the endpoint you want to send the file to

    file_path = audio_file_input

    with open(file_path, 'rb') as audio_file:
        # Create a dictionary to hold the file data
        files = {'audio': audio_file}
    
    # Set the appropriate headers
        headers = {'Content-Type': 'audio/mpeg'}
        response = requests.post(url, files=files) 

    # Check the response

        if response.status_code == 200:

            

            try:
                json_data = response.json()
                aud = json_data['transcript']
                print(aud)
            except json.decoder.JSONDecodeError as e:
                print('Invalid JSON response:', response.content)
        else:
            print('Error uploading the file:', response.text)
        return aud
            # Return a response

def get_chat_response(messages):

   chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",

                 messages=messages,temperature=0.1)

   return chat_completion.choices[0].message.content




if 'send_button' not in st.session_state:

        st.session_state['send_button'] = False

 

init_prompt=st.sidebar.text_area("Enter your System (Initiation) prompt here")

send_button=st.sidebar.button("Send")



if send_button and init_prompt:

    st.session_state.send_button=True

 

if st.session_state.send_button==True:

    if "messages" not in st.session_state:

        st.session_state.messages=[

            {"role": "system", "content":init_prompt}

            ]

    if 'generated' not in st.session_state:

        st.session_state['generated'] = []

        chat_response = get_chat_response(st.session_state.messages)

        st.session_state.messages.append({"role":"assistant","content":chat_response})

        st.session_state['generated'].append(chat_response)





    if 'past' not in st.session_state:

        st.session_state['past'] = []

        st.session_state['past'].append(" ")






    response_container = st.container()

    container = st.container()

 
 

    with container:

        placeholder = st.empty()

        with placeholder.form(key='my_form', clear_on_submit=True):

                user_input = st.text_input("You:", key='input')

                submit_button = st.form_submit_button(label='Send')

                freq = 44100
 
                # Recording duration
                duration = 10
                record_button = st.form_submit_button(label='Record')

                # record_button=st.form_submit_button(label="record")


                if submit_button and user_input:
                    with st.spinner("Loading"):
                        st.session_state.messages.append({"role":"user","content":user_input})

                        print("messages dict-----",st.session_state.messages)

                        

                        message_bot = get_chat_response(st.session_state.messages)

                        # message_bot = azure_gpt_call_davinci()

                        st.session_state.messages.append({"role":"assistant","content":message_bot},)

                        st.sidebar.write(st.session_state.messages)

                        st.session_state['past'].append(user_input)

                        st.session_state['generated'].append(message_bot)

                if record_button:
                    with st.spinner("Recording"):
                        recording = sd.rec(int(duration * freq),
                                        samplerate=freq, channels=1)
                    
                    # Record audio for the given number of seconds
                        sd.wait()
                    
                    # This will convert the NumPy array to an audio
                    # file with the given sampling frequency
                        write("recording0.wav", freq, recording)

                        audio_file = "recording0.wav"
                        user_input_audio = api_endpoint(audio_file)
                        #st.write(user_input_audio)
                    with st.spinner("Loading"):    
                        st.session_state.messages.append({"role":"user","content":user_input_audio})

                        print("messages dict-----",st.session_state.messages)

                        

                        message_bot = get_chat_response(st.session_state.messages)

                        # message_bot = azure_gpt_call_davinci()

                        st.session_state.messages.append({"role":"assistant","content":message_bot},)

                        st.sidebar.write(st.session_state.messages)

                        st.session_state['past'].append(user_input_audio)
                        st.session_state['generated'].append(message_bot)
                    






    with response_container:

        if st.session_state['generated']:

            for i in range(len(st.session_state['generated'])):

                if st.session_state["past"][i]!=" ":

                    message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')

                    message(st.session_state["generated"][i], key=str(i))

 

                else:

                    message(st.session_state["generated"][i], key=str(i))