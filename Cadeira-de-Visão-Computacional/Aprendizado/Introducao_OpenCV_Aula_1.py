#========================================================================Bibliotecas=======================================================================#

import numpy as np
import cv2
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt

#==========================================================================Funções=========================================================================#

# Função para exibir imagens no Streamlit
def display_image(img, title):
    st.image(img, caption=title, use_column_width=True)

# Função de amostragem
def amostragem(img, n):
    # Reduz a resolução da imagem, selecionando apenas alguns pixels com base no fator n
    amostra = [lin[::n] for lin in img[::n]]
    return np.array(amostra)

# Função de quantização
def quantizacao_uniforme(img, K):
    # Reduz o número de níveis de cinza na imagem, agrupando os valores de pixel em K níveis
    a = np.float32(img)
    bucket = 256 / K
    quantizado = np.floor(a / bucket)
    return np.uint8(quantizado * bucket)

# Função para conversão de BGR para CMY
def bgr_to_cmy(image):
    # Converte a imagem de BGR para RGB
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Converte a imagem de RGB para CMY
    cmy = 255 - rgb
    return cmy

# Função para criar máscara de acordo com a forma selecionada
def create_mask(img_shape, shape, **kwargs):
    mask = np.zeros(img_shape[:2], dtype="uint8")
    if shape == 'Círculo':
        cv2.circle(mask, (kwargs['cx'], kwargs['cy']), kwargs['radius'], 255, -1)
    elif shape == 'Quadrado':
        cv2.rectangle(mask, (kwargs['x'], kwargs['y']), (kwargs['x'] + kwargs['side'], kwargs['y'] + kwargs['side']), 255, -1)
    elif shape == 'Retângulo':
        cv2.rectangle(mask, (kwargs['x'], kwargs['y']), (kwargs['x'] + kwargs['width'], kwargs['y'] + kwargs['height']), 255, -1)
    elif shape == 'Triângulo':
        pts = np.array([[kwargs['x1'], kwargs['y1']], [kwargs['x2'], kwargs['y2']], [kwargs['x3'], kwargs['y3']]], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.fillPoly(mask, [pts], 255)
    return mask

#======================================================================Função Principal=====================================================================#

# Função principal do Streamlit
def main():
    # Título da barra lateral
    st.sidebar.title('Processamento de Imagens com OpenCV')
    st.sidebar.subheader('Introdução')

    # Carregamento do arquivo de imagem
    uploaded_file = st.file_uploader("Escolha uma imagem", type=["jpg", "png"])

    if uploaded_file is not None:
        # Carregar imagem usando PIL e converter para array numpy
        img = Image.open(uploaded_file)
        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        # Criar colunas para input e output
        col1, col2 = st.columns(2)

        # Exibir a imagem original na primeira coluna
        with col1:
            st.image(img, caption='Imagem Original', use_column_width=True)
            cb_img = img
        
        # Exibir informações da imagem
            st.sidebar.subheader('Informações da Imagem Original')
            st.sidebar.text(f'Tamanho da imagem: {cb_img.shape[0]}x{cb_img.shape[1]}')
            st.sidebar.text(f'Quantidade de canais: {cb_img.shape[2] if len(cb_img.shape) > 2 else 1}')
            st.sidebar.text(f'Número de pixels: {cb_img.shape[0] * cb_img.shape[1]}')
            st.sidebar.text(f'Tipo de dado da imagem: {cb_img.dtype}')

#=========================================================================Amostragem========================================================================#

        # Seção de amostragem
        st.sidebar.subheader('Amostragem')
        fator = st.sidebar.slider('Escolha o fator de amostragem', min_value=2, max_value=1024, step=2, value=2)
        if st.sidebar.button('Aplicar Amostragem'):
            sampled_img = amostragem(img, fator)
            with col2:
                display_image(sampled_img, f'Imagem Amostrada com fator {fator}')

#====================================================================Quantização Uniforme===================================================================#

        # Seção de quantização uniforme
        st.sidebar.subheader('Quantização Uniforme')
        K = st.sidebar.slider('Escolha o número de cores', min_value=2, max_value=1024, step=2, value=2)
        if st.sidebar.button('Aplicar Quantização'):
            quantized_img = quantizacao_uniforme(cv2.cvtColor(img, cv2.COLOR_RGB2GRAY), K)
            with col2:
                display_image(quantized_img, f'Imagem Quantizada com {K} cores')

#=================================================================Separação dos Canais RGB=================================================================#

        # Seção de separação e junção dos canais RGB
        st.sidebar.subheader('Separação dos Canais RGB')

        # Selectbox para escolher qual canal exibir
        canal_selecionado = st.sidebar.selectbox(
            'Escolha o canal de cor para exibir',
            ('R', 'G', 'B')
        )

        if st.sidebar.button('Aplicar Separação'):
            R, G, B = cv2.split(img)
            merged_img = cv2.merge([R, G, B])
            
            with col2:
                if canal_selecionado == 'R':
                    display_image(R, 'Canal R')
                elif canal_selecionado == 'G':
                    display_image(G, 'Canal G')
                elif canal_selecionado == 'B':
                    display_image(B, 'Canal B')

#===========================================================================Escala==========================================================================#

        # Seção de escala
        st.sidebar.subheader('Ajuste de Escala')
        escala = st.sidebar.slider('Escolha o fator de escala', min_value=0.1, max_value=3.0, value=1.0, step=0.1)

        if st.sidebar.button('Aplicar Escala'):
            # Redimensionar a imagem com base na escala
            new_size = (int(img.shape[1] * escala), int(img.shape[0] * escala))
            resized_img = cv2.resize(img, new_size, interpolation=cv2.INTER_LINEAR)
            with col2:
                display_image(resized_img, f'Imagem Redimensionada (Escala: {escala})')

#=================================================================Transformações Geométricas================================================================#

        # Seção de transformações geométricas
        st.sidebar.subheader('Transformações Geométricas')
        tx = st.sidebar.slider('Translação X', -200, 200, 100)
        ty = st.sidebar.slider('Translação Y', -200, 200, 50)
        if st.sidebar.button('Aplicar Translação'):
            translation_matrix = np.float32([[1, 0, tx], [0, 1, ty]])
            translated_img = cv2.warpAffine(img, translation_matrix, (img.shape[1], img.shape[0]))
            with col2:
                display_image(translated_img, 'Imagem Transladada')

        angle = st.sidebar.slider('Ângulo de Rotação', 0, 360, 45)
        if st.sidebar.button('Aplicar Rotação'):
            rotation_matrix = cv2.getRotationMatrix2D((img.shape[1] // 2, img.shape[0] // 2), angle, 1.0)
            rotated_img = cv2.warpAffine(img, rotation_matrix, (img.shape[1], img.shape[0]))
            with col2:
                display_image(rotated_img, 'Imagem Rotacionada')

#=========================================================================Espelhamento=====================================================================#

        # Seção de espelhamento
        st.sidebar.subheader('Espelhamento')
        espelhamento = st.sidebar.selectbox(
            'Escolha o tipo de espelhamento',
            ('Nenhum', 'Horizontal', 'Vertical', 'Ambos')
        )

        if st.sidebar.button('Aplicar Espelhamento'):
            # Aplicar espelhamento
            if espelhamento == 'Nenhum':
                mirrored_img = img  # Usar a imagem original se nenhum espelhamento for selecionado
            elif espelhamento == 'Horizontal':
                mirrored_img = cv2.flip(img, 1)
            elif espelhamento == 'Vertical':
                mirrored_img = cv2.flip(img, 0)
            elif espelhamento == 'Ambos':
                mirrored_img = cv2.flip(img, -1)
            with col2:
                display_image(mirrored_img, f'Imagem Espelhada (Espelhamento: {espelhamento})')

#================================================================Operações Aritméticas e Lógicas============================================================#

        # Seção de operações aritméticas e lógicas
        st.sidebar.subheader('Operações Aritméticas e Lógicas')

        # Carregamento do primeiro arquivo de imagem
        uploaded_file1 = st.sidebar.file_uploader("Escolha a primeira imagem", type=["jpg", "png"])

        # Carregamento do segundo arquivo de imagem
        uploaded_file2 = st.sidebar.file_uploader("Escolha a segunda imagem", type=["jpg", "png"])

        if uploaded_file1 is not None:
            img1 = Image.open(uploaded_file1)
            img1 = np.array(img1)

            if uploaded_file2 is not None:
                img2 = Image.open(uploaded_file2)
                img2 = np.array(img2)

                # Garantir que as duas imagens têm o mesmo tamanho
                img1 = cv2.resize(img1, (img2.shape[1], img2.shape[0]))
                
                # Criar colunas para input e output
                #col1, col2 = st.columns(2)

                # Exibir a primeira imagem na primeira coluna
                #with col1:
                #    st.image(img1, caption='Imagem Original 1', use_column_width=True)

                # Exibir a segunda imagem na segunda coluna
                #with col2:
                #    st.image(img2, caption='Imagem Original 2', use_column_width=True)
                
                # Seção de operações aritméticas e lógicas
                st.sidebar.subheader('Operações Aritméticas e Lógicas')

                # Selectbox para escolher a operação
                operacao_selecionada = st.sidebar.selectbox(
                    'Escolha a operação a ser aplicada',
                    ('Adição', 'Subtração', 'Multiplicação', 'Divisão', 'AND', 'OR', 'XOR', 'NOT')
                )

                if st.sidebar.button('Aplicar Operação'):
                    if operacao_selecionada in ['Adição', 'Subtração', 'Multiplicação', 'Divisão']:
                        # Operações aritméticas
                        if operacao_selecionada == 'Adição':
                            resultado = cv2.add(img1, img2)
                        elif operacao_selecionada == 'Subtração':
                            resultado = cv2.subtract(img1, img2)
                        elif operacao_selecionada == 'Multiplicação':
                            resultado = cv2.multiply(img1, img2)
                        elif operacao_selecionada == 'Divisão':
                            resultado = cv2.divide(img1, img2 + 1)

                    elif operacao_selecionada in ['AND', 'OR', 'XOR', 'NOT']:
                        # Operações lógicas
                        if operacao_selecionada == 'AND':
                            resultado = cv2.bitwise_and(img1, img2)
                        elif operacao_selecionada == 'OR':
                            resultado = cv2.bitwise_or(img1, img2)
                        elif operacao_selecionada == 'XOR':
                            resultado = cv2.bitwise_xor(img1, img2)
                        elif operacao_selecionada == 'NOT':
                            resultado = cv2.bitwise_not(img1)

                    with col2:
                        display_image(resultado, f'Imagem após {operacao_selecionada}')

#==========================================================================Máscara==========================================================================#

        # Seção de máscaras        
        st.sidebar.subheader('Máscaras')
        shape = st.sidebar.selectbox('Escolha a forma da máscara', ['Círculo', 'Quadrado', 'Retângulo', 'Triângulo'])

        # Parâmetros para diferentes formas
        if shape == 'Círculo':
            cx = st.sidebar.slider('Centro X', 0, img.shape[1], img.shape[1] // 2)
            cy = st.sidebar.slider('Centro Y', 0, img.shape[0], img.shape[0] // 2)
            radius = st.sidebar.slider('Raio', 0, min(img.shape[:2]) // 2, 50)
            params = {'cx': cx, 'cy': cy, 'radius': radius}
        
        elif shape == 'Quadrado':
            x = st.sidebar.slider('X', 0, img.shape[1], img.shape[1] // 4)
            y = st.sidebar.slider('Y', 0, img.shape[0], img.shape[0] // 4)
            side = st.sidebar.slider('Lado', 0, min(img.shape[:2]), 100)
            params = {'x': x, 'y': y, 'side': side}

        elif shape == 'Retângulo':
            x = st.sidebar.slider('X', 0, img.shape[1], img.shape[1] // 4)
            y = st.sidebar.slider('Y', 0, img.shape[0], img.shape[0] // 4)
            width = st.sidebar.slider('Largura', 0, img.shape[1], 150)
            height = st.sidebar.slider('Altura', 0, img.shape[0], 100)
            params = {'x': x, 'y': y, 'width': width, 'height': height}
        
        elif shape == 'Triângulo':
            x1 = st.sidebar.slider('X1', 0, img.shape[1], img.shape[1] // 4)
            y1 = st.sidebar.slider('Y1', 0, img.shape[0], img.shape[0] // 4)
            x2 = st.sidebar.slider('X2', 0, img.shape[1], img.shape[1] // 2)
            y2 = st.sidebar.slider('Y2', 0, img.shape[0], img.shape[0] // 4)
            x3 = st.sidebar.slider('X3', 0, img.shape[1], img.shape[1] // 2)
            y3 = st.sidebar.slider('Y3', 0, img.shape[0], img.shape[0] // 2)
            params = {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'x3': x3, 'y3': y3}

        if st.sidebar.button('Aplicar Máscara'):
            mask = create_mask(img.shape, shape, **params)
            masked_img = cv2.bitwise_and(img, img, mask=mask)
            with col2:
                display_image(masked_img, f'Imagem com Máscara - {shape}')

#===============================================================Conversões de Modelos de Cores==============================================================#

        # Seção de conversões de modelos de cores
        st.sidebar.subheader('Conversões de Modelos de Cores')
        color_model = st.sidebar.selectbox('Escolha o modelo de cor', ['RGB', 'HSV', 'LAB', 'Grayscale', 'CMY'])
        
        if st.sidebar.button('Aplicar Conversão'):
            if color_model == 'RGB':
                converted_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            elif color_model == 'HSV':
                converted_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            elif color_model == 'LAB':
                converted_img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
            elif color_model == 'Grayscale':
                converted_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            elif color_model == 'CMY':
                converted_img = bgr_to_cmy(img)
                
            with col2:
                display_image(converted_img, f'Imagem em {color_model}')

#=========================================================================Executar========================================================================#

# Executar a função principal
if __name__ == "__main__":
    main()