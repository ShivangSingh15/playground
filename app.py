from flask import Flask, request, render_template, jsonify
import openai
import os
import json


app = Flask(__name__)
api_key = os.environ.get('OPENAI_API_KEY1')
model_id = 'whisper-1'



# @app.route('/')
# def home():
#     return render_template('transcribe.html')

    #return 'Welcome to the home page'



# @app.route('/transcribe.html', methods=['GET'])
# def transcribe_html():
#     return render_template('transcribe.html')



@app.route('/transcribe', methods=['POST'])
def transcribe():

   # Get the uploaded audio file from the request

    audio_file = request.files['audio']
    audio_path = 'audio.wav'
    audio_file.save(audio_path)



    # Perform transcription using OpenAI API

    with open(audio_path, 'rb') as file:
        response = openai.Audio.transcribe(
            api_key=api_key,
            model=model_id,
            file=file
        )

    transcript = response['text']
    # Create a JSON response
    json_response = {'transcript': transcript}
    return jsonify(json_response)



    #  print('POST request received')

    

    # # # Process the uploaded audio file and obtain the transcript

    # #  transcript = 'Example transcript'  # Replace with your actual transcript

    

    # # # Create a JSON response

    # #  response = {'transcript': transcript}

    

    # Return the JSON response

    #  return jsonify(response)



    



# @app.route('/')

# def upload_form():

#     return render_template('upload.html')

#   try:

#         # Get the uploaded audio file from the request

#         audio_file = request.files['audio']

#         audio_path = 'audio.wav'

#         audio_file.save(audio_path)



#         # Perform transcription using OpenAI API

#         with open(audio_path, 'rb') as file:

#             response = openai.Audio.transcribe(

#                 api_key=api_key,

#                 model=model_id,

#                 file=file

#             )



#         # Extract the transcript from the response

#         transcript = response['text']



#         # Create a JSON response

#         json_response = {'transcript': transcript}



#         # Return the JSON response

#         return jsonify(json_response)



#   except Exception as e:

#         print("Error during transcription:", str(e))

#         # Return an error JSON response

#         error_response = {'error': 'Transcription failed'}

#         return jsonify(error_response), 500



if __name__ == '__main__':

    app.run(debug=True)
