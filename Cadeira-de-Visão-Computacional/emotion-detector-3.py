import streamlit as st
import cv2
import numpy as np
from deepface import DeepFace
from PIL import Image

# Dicionário de tradução de emoções
emotion_translation = {
    'angry': 'Raiva',
    'disgust': 'Nojo',
    'fear': 'Medo',
    'happy': 'Felicidade',
    'sad': 'Tristeza',
    'surprise': 'Surpresa',
    'neutral': 'Neutro'
}

def detect_emotion(image):
    """
    Detecta emoções em uma imagem usando a biblioteca DeepFace.
    
    Args:
        image (PIL.Image): Imagem no formato Pillow.
    
    Returns:
        None
    """
    # Converter a imagem do Pillow para o formato do OpenCV
    image = np.array(image.convert('RGB'))
    image = image[:, :, ::-1].copy() 
    
    try:
        # Exibir mensagem de carregamento
        with st.spinner('Detectando emoções...'):
            # Analisa as emoções na imagem
            results = DeepFace.analyze(image, actions=['emotion'], enforce_detection=False)
        
        # Verificar se o resultado é uma lista de dicionários
        if isinstance(results, list):
            # Verificar se há pelo menos um rosto detectado
            if len(results) > 0:
                # Iterar sobre todos os rostos detectados
                for result in results:
                    # Obter a emoção dominante
                    emotion = result.get('dominant_emotion', 'Desconhecida')
                    
                    # Traduzir a emoção para português
                    emotion_pt = emotion_translation.get(emotion, 'Desconhecida')
                    
                    # Adicionar texto à imagem
                    image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                    #st.image(image_pil)
                    st.subheader(f"Emoção detectada: {emotion_pt}")
            else:
                raise ValueError("Nenhum rosto detectado na imagem.")
        else:
            raise ValueError("Formato de resultado inesperado.")

    except Exception as e:
        st.error(f"Erro ao detectar emoções: {e}")

def main():
    """
    Função principal que define a interface do usuário usando Streamlit.
    
    Returns:
        None
    """
    st.title("Detector de Emoções")
    
    uploaded_file = st.file_uploader("Escolha uma imagem", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Imagem carregada", use_column_width=True)
        
        if st.button("Detectar Emoção"):
            detect_emotion(image)

if __name__ == "__main__":
    main()