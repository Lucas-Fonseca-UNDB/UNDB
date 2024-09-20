from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Documentação do Código: emotion_detector_6.py', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

pdf = PDF()
pdf.add_page()
pdf.set_font('Arial', 'I', 12)

codigo = '''
Descrição Geral
Este script utiliza a biblioteca DeepFace para detectar emoções e rostos em frames de vídeo. A aplicação é construída com Streamlit para fornecer uma interface de usuário simples e interativa. O código também faz uso das bibliotecas cv2 (OpenCV), numpy, e PIL para manipulação de imagens.

Importações:
import streamlit as st
from deepface import DeepFace
import cv2
import numpy as np
from PIL import Image
import io

Descrição das Importações:
-streamlit: Utilizado para criar a interface de usuário.
-DeepFace: Biblioteca para análise de emoções e reconhecimento facial.
-cv2: Biblioteca OpenCV para manipulação de imagens e vídeos.
-numpy: Biblioteca para operações numéricas.
-PIL: Biblioteca para manipulação de imagens.
-io: Biblioteca para manipulação de fluxos de entrada e saída.

Funções:
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

Descrição da Função:
A função detect_emotion_and_faces recebe um frame de vídeo no formato numpy.ndarray e retorna uma lista de tuplas contendo a emoção detectada, a confiança e as coordenadas do rosto.

Parâmetros:
-frame (numpy.ndarray): Frame no formato OpenCV.
Retorno:
-list: Lista de tuplas contendo a emoção detectada, a confiança e as coordenadas do rosto.
Detalhamento do Processo:
1.Análise de Emoções: Utiliza a função DeepFace.analyze para analisar as emoções no frame.
2.Verificação de Resultados: Verifica se os resultados são uma lista de dicionários.
3.Extração de Informações: Para cada rosto detectado, extrai a emoção dominante, a confiança e as coordenadas do rosto.
4.Tratamento de Exceções: Em caso de erro, exibe uma mensagem de erro no Streamlit e retorna uma lista vazia.

Conclusão:
Este script é uma ferramenta poderosa para detecção de emoções e rostos em frames de vídeo, utilizando a biblioteca DeepFace. A função principal detect_emotion_and_faces é robusta e trata exceções para garantir uma experiência de usuário suave.
'''

pdf.multi_cell(0, 10, codigo)
pdf.output('doc_remotion_detector.pdf')