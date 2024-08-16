import streamlit as st
from audio_recorder_streamlit import audio_recorder
from groq import Groq
import os

def audio_to_text(filepath,client,model):
    with open(filepath, "rb") as file:
        transcriptions = client.audio.translations.create(
            file=(filepath, file.read()),
            model=model,
        )
    return transcriptions.text

def save_uploadedfile(uploadedfile,directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(os.path.join(directory,uploadedfile.name),'wb') as f:
        f.write(uploadedfile.getbuffer())

    return st.success(f"Saved File: {uploadedfile.name}")


def transcript_chat_completion(client, transcript, user_query):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": '''
                use this transcript or transcripts to answer any user questions, citing any specific quotes {transcript}
                '''.format(transcript=transcript),
            }
            ,{
                "role": "user",
                "content": user_query,
            }
        ],
        model="llama3-8b-8192",
    )

    return chat_completion.choices[0].message.content


def main():
    st.sidebar.title("API key config")
    api_key= st.sidebar.text_input("Enter your Api key",type='password')
    st.title("Chat with MP3 audio files")
    st.write("This is an streamlit  application that can interact with mp3 audio files")


    if api_key:
        try:
            with st.sidebar:
                st.success(f"API key successfully set ✅")
            client = Groq(api_key = api_key)
            whisper_model = 'whisper-large-v3'
            uploaded_audio= st.file_uploader('upload mp3 files',type=['mp3'])
            if uploaded_audio is not None:
                save_uploadedfile(uploaded_audio,"audio_files")
                translation_text = audio_to_text(filepath=os.path.join("audio_files", uploaded_audio.name), client=client,model=whisper_model)
                prompt= st.chat_input('Chat with audio files')
                with st.chat_message('user'):
                    st.write("Transcription: ", translation_text)
                
                with st.chat_message('assistant'):
                    if prompt is not None:
                        ai_response=transcript_chat_completion(client, translation_text,prompt)
                        st.write(ai_response)
                    else:
                        st.info("We are ready, Please start your conversation")
            
            else:
                 st.info("Please upload the MP3 audio files first 🎵")

        except Exception as e:
            st.error(f"Error: {e}")

    else:
        st.error("Set your API token first 🚩")


if __name__=="__main__":
    main()