import streamlit as st
from deepface import DeepFace
import cv2
import numpy as np
from PIL import Image
import io

def detect_emotion_and_faces(frame):
    """
    Detecta emoções e rostos em um frame usando a biblioteca DeepFace.
    
    Args:
        frame (numpy.ndarray): Frame no formato OpenCV.
    
    Returns:
        list: Lista de tuplas contendo a emoção detectada, a confiança e as coordenadas do rosto.
    """
    try:
        # Analisa as emoções no frame
        results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        
        faces = []
        # Verificar se o resultado é uma lista de dicionários
        if isinstance(results, list) and len(results) > 0:
            for result in results:
                # Obter a emoção dominante do rosto detectado e a confiança
                emotion = result.get('dominant_emotion', 'Unknown')
                confidence = result.get('emotion', {}).get(emotion, 0)
                
                # Obter as coordenadas do rosto
                face_coords = result.get('region', {})
                faces.append((emotion, confidence, face_coords))
        return faces
    except Exception as e:
        st.error(f"Erro na detecção de emoções: {str(e)}. Verifique a câmera ou tente novamente.")
        return []

# Inicializa uma variável de estado para controlar a exibição da câmera e captura de imagem
if 'camera_open' not in st.session_state:
    st.session_state['camera_open'] = False
if 'captured_image' not in st.session_state:
    st.session_state['captured_image'] = None
if 'capture_image' not in st.session_state:
    st.session_state['capture_image'] = False

st.sidebar.title('Projeto de Visão Computacional')
st.sidebar.subheader('Detector de Emoções em Tempo Real')
st.sidebar.write('Prof.Dr.Giovanni Lucca')
st.sidebar.write('Grupo: Lucas Fonseca, Luis Rodrigo, Diogo Soares, Pedro Arthur, Osvaldo Saboia')

# Botão para abrir a câmera
if st.sidebar.button('Abrir câmera'):
    st.session_state['camera_open'] = True

# Botão para capturar uma imagem e fechar a câmera após a captura
if st.sidebar.button('Capturar imagem'):
    st.session_state['capture_image'] = True

# Exibe a câmera se a variável de estado estiver ativada
if st.session_state['camera_open']:
    # Captura o vídeo da câmera em tempo real
    cap = cv2.VideoCapture(0)
    stframe = st.empty()

    try:
        while st.session_state['camera_open']:
            ret, frame = cap.read()
            if not ret:
                st.write("Falha ao capturar imagem da câmera")
                break

            # Detecta emoções e rostos na imagem capturada
            faces = detect_emotion_and_faces(frame)

            # Desenha caixas ao redor dos rostos detectados e exibe a confiança da emoção
            for emotion, confidence, face_coords in faces:
                if face_coords:
                    x, y, w, h = face_coords['x'], face_coords['y'], face_coords['w'], face_coords['h']
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    label = f"{emotion} ({confidence:.2f})"
                    cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Converte a imagem de volta para o formato que o Streamlit possa exibir
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            stframe.image(frame_rgb, caption="Emoções detectadas", channels="RGB")

            # Captura a imagem quando o botão é clicado e fecha a câmera automaticamente
            if st.session_state.get('capture_image', False):
                st.session_state['captured_image'] = frame_rgb
                st.session_state['camera_open'] = False  # Fecha a câmera
                st.session_state['capture_image'] = False
                break  # Sai do loop para garantir que a câmera seja fechada

            # Adiciona um pequeno atraso para reduzir a carga de processamento
            cv2.waitKey(1)

    finally:
        # Garante que a câmera seja fechada mesmo em caso de exceção
        cap.release()

# Exibe a imagem capturada, se disponível
if st.session_state['captured_image'] is not None:
    #st.image(st.session_state['captured_image'], caption="Imagem capturada", channels="RGB")

    # Botão para fazer o download da imagem capturada
    img = Image.fromarray(st.session_state['captured_image'])
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    byte_im = buf.getvalue()
    st.sidebar.download_button(label="Baixar imagem", data=byte_im, file_name="captured_image.jpg", mime="image/jpeg")
else:
    st.sidebar.write("Câmera fechada")
