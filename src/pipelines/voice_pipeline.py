from  resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import io
import librosa
import streamlit as st



@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()


def get_voice_embedding(audio_bytes):

    try:
        encoder=load_voice_encoder()
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        wav=preprocess_wav(audio)
        embedding=encoder.embed_utterance(wav)
        return embedding.tolist()
    
    except Exception as e:
        st.error(f"Error processing audio: {e}")
        return None
    




def identify_speaker(new_embedding,candidate_dict,threshold=0.7):
    if new_embedding is None and not candidate_dict:
        return None, None
    
    best_sid=None
    best_score=-1

    for sid,stored_embedding  in candidate_dict.items():
        if stored_embedding:
            similarity=np.dot(new_embedding, stored_embedding)
            if similarity>best_score:
                best_score=similarity
                best_sid=sid

    if best_score>=threshold:
        return best_sid, best_score
    else:
        return None, best_score
    

def process_bulk_audio(audio_bytes,candidate_dict,threshold=0.7):
    try:
        encoder=load_voice_encoder()
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        segments = librosa.effects.split(audio, top_db=20)

        identified_results = {}
        for start,end in segments:
            if (end-start)<sr*0.5:
                continue
            segment_audio=audio[start:end]
            wav=preprocess_wav(segment_audio)
            embedding=encoder.embed_utterance(wav)
            sid,score=identify_speaker(embedding,candidate_dict,threshold)


            if sid:
                if sid not in identified_results or score>identified_results[sid]:
                    identified_results[sid]=score


        return identified_results
    except Exception as e:
        st.error(f"Error processing bulk audio: {e}")
        return {}
                         
    

    