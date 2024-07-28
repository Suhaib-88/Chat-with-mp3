import streamlit as st
from audio_recorder_streamlit import audio_recorder
from groq import Groq

def audio_to_text(filepath,client,model):
    with open(filepath, "rb") as file:
        transcriptions = client.audio.translations.create(
            file=(filepath, file.read()),
            model=model,
        )
    return transcriptions.text



def transcript_chat_completion(client, transcript):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": transcript,
            }
        ],
        model="llama3-8b-8192",
    )

    return chat_completion.choices[0].message.content


def main():
    st.sidebar.title("API key config")
    api_key= st.sidebar.text_input("Enter your Api key",type='password')
    st.title("AI Voice assistant")
    st.write("This is a simple voice assistant that can perform various tasks")


    if api_key:
        try:
            client = Groq(api_key = api_key)
            whisper_model = 'whisper-large-v3'
            recorded_audio= audio_recorder()
            if recorded_audio:
                audiofile='audio_file.mp3'
                with open(audiofile,'wb') as f:
                    f.write(recorded_audio)

                translation_text = audio_to_text(audiofile, client=client,model=whisper_model)
                with st.chat_message('user'):
                    st.write("Transcription: ", translation_text)
                
                with st.chat_message('assistant'):
                    ai_response=transcript_chat_completion(client, translation_text)
                    st.write(ai_response)
        except Exception as e:
            st.error("Error: ", e)

    else:
        st.error("Set your API token first 🚩")


if __name__=="__main__":
    main()