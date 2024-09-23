import streamlit as st
from deepface import DeepFace
import cv2
import numpy as np
from PIL import Image
import io

def detect_emotion_and_faces(frame):
    try:
        results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        faces = []
        if isinstance(results, list) and len(results) > 0:
            for result in results:
                emotion = result.get('dominant_emotion', 'Unknown')
                confidence = result.get('emotion', {}).get(emotion, 0)
                face_coords = result.get('region', {})
                faces.append((emotion, confidence, face_coords))
        return faces
    except Exception as e:
        st.error(f"Erro na detecção de emoções: {str(e)}. Verifique a câmera ou tente novamente.")
        return []

if 'camera_open' not in st.session_state:
    st.session_state['camera_open'] = False
if 'captured_image' not in st.session_state:
    st.session_state['captured_image'] = None
if 'capture_image' not in st.session_state:
    st.session_state['capture_image'] = False

st.sidebar.title('Projeto de Visão Computacional')
st.sidebar.subheader('Detector de Emoções em Tempo Real')
st.sidebar.write('Giovanni Lucca, PhD, Professor')
st.sidebar.write('Grupo: Lucas Fonseca, Luis Rodrigo, Diogo Soares, Pedro Arthur, Osvaldo Saboia')

if st.sidebar.button('Abrir câmera'):
    st.session_state['camera_open'] = True

if st.sidebar.button('Capturar imagem'):
    st.session_state['capture_image'] = True

if st.session_state['camera_open']:
    cap = cv2.VideoCapture(0)
    stframe = st.empty()

    try:
        while st.session_state['camera_open']:
            ret, frame = cap.read()
            if not ret:
                st.write("Falha ao capturar imagem da câmera")
                break

            faces = detect_emotion_and_faces(frame)

            for emotion, confidence, face_coords in faces:
                if face_coords:
                    x, y, w, h = face_coords['x'], face_coords['y'], face_coords['w'], face_coords['h']
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    label = f"{emotion} ({confidence:.2f})"
                    cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            stframe.image(frame_rgb, caption="Emoções detectadas", channels="RGB")

            if st.session_state.get('capture_image', False):
                st.session_state['captured_image'] = frame_rgb
                st.session_state['camera_open'] = False
                st.session_state['capture_image'] = False
                break

    finally:
        cap.release()

if st.session_state['captured_image'] is not None:
    img = Image.fromarray(st.session_state['captured_image'])
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    byte_im = buf.getvalue()
    st.sidebar.download_button(label="Baixar imagem", data=byte_im, file_name="captured_image.jpg", mime="image/jpeg")
else:
    st.sidebar.write("Câmera fechada")
