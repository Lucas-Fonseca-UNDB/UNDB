#========================================================================Bibliotecas=======================================================================#

import numpy as np
import cv2
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt

#======================================================================Função Principal=====================================================================#

def display_image(image, title):
    st.image(image, caption=title, use_column_width=True)

def main():
    st.sidebar.title('Processamento de Imagens com OpenCV')
    st.sidebar.subheader('Pré-processamento')

    # Upload da imagem
    uploaded_file = st.file_uploader("Escolha uma imagem...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Leitura da imagem em formato de bytes
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)  # Leitura como imagem colorida

        # Criar colunas para input e output
        col1, col2 = st.columns(2)
        
        # Exibir a imagem original na primeira coluna
        with col1:
            st.image(img, caption='Imagem Original', use_column_width=True)

#======================================================================Redução de ruídos=====================================================================#

        # Converter para escala de cinza
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  

        # Seção de redução de ruídos
        st.sidebar.subheader('Redução de ruídos')
        ruido = st.sidebar.selectbox(
            'Escolha o tipo de remoção de ruído',
            ('Filtro da média', 'Filtro da mediana', 'Filtro gaussiano', 'Filtro bilateral', 'Threshold adaptativo')
        )

        if ruido == 'Filtro da média':
            kernel_size = st.sidebar.slider('Tamanho do kernel', min_value=1, max_value=25, value=3, step=2)
        elif ruido == 'Filtro da mediana':
            ksize = st.sidebar.slider('Tamanho da janela', min_value=1, max_value=25, value=3, step=2)
        elif ruido == 'Filtro gaussiano':
            kernel_size = st.sidebar.slider('Tamanho do kernel', min_value=1, max_value=25, value=3, step=2)
            sigma = st.sidebar.slider('Sigma', min_value=0.0, max_value=10.0, value=1.0, step=0.1)
        elif ruido == 'Filtro bilateral':
            d = st.sidebar.slider('Diâmetro do pixel', min_value=1, max_value=25, value=9, step=2)
            sigma_color = st.sidebar.slider('Sigma cor', min_value=0.0, max_value=100.0, value=75.0, step=1.0)
            sigma_space = st.sidebar.slider('Sigma espaço', min_value=0.0, max_value=100.0, value=75.0, step=1.0)
        elif ruido == 'Threshold adaptativo':
            max_val = st.sidebar.slider('Valor máximo', min_value=0, max_value=255, value=255)
            block_size = st.sidebar.slider('Tamanho do bloco', min_value=3, max_value=25, value=11, step=2)
            C = st.sidebar.slider('Constante C', min_value=0, max_value=10, value=2)

        if st.sidebar.button('Aplicar Redução de ruído'):
            if ruido == 'Filtro da média':
                filtro_media = cv2.blur(gray, (kernel_size, kernel_size))
                with col2:
                    display_image(filtro_media, f'Imagem com Filtro da Média - Kernel {kernel_size}')
            elif ruido == 'Filtro da mediana':
                filtro_mediana = cv2.medianBlur(gray, ksize)
                with col2:
                    display_image(filtro_mediana, f'Imagem com Filtro da Mediana - Janela {ksize}')
            elif ruido == 'Filtro gaussiano':
                filtro_gaussiano = cv2.GaussianBlur(gray, (kernel_size, kernel_size), sigma)
                with col2:
                    display_image(filtro_gaussiano, f'Imagem com Filtro Gaussiano - Kernel {kernel_size}, Sigma {sigma}')
            elif ruido == 'Filtro bilateral':
                filtro_bilateral = cv2.bilateralFilter(gray, d, sigma_color, sigma_space)
                with col2:
                    display_image(filtro_bilateral, f'Imagem com Filtro Bilateral - D {d}, Sigma Color {sigma_color}, Sigma Espaço {sigma_space}')
            elif ruido == 'Threshold adaptativo':
                bin_image = cv2.adaptiveThreshold(gray, max_val, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, C)
                with col2:
                    display_image(bin_image, f'Imagem com Threshold Adaptativo - Max {max_val}, Bloco {block_size}, C {C}')

#=================================================================Função expansão de contraste===============================================================#

        # Função principal que aplica a redução de ruído com base na seleção do usuário e nos parâmetros ajustados
        def apply_noise_reduction(gray, method, params):
            if method == 'Binarizar':
                return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, params['block_size'], params['C'])

            elif method == 'Equalização de histograma':
                return cv2.equalizeHist(gray)

            elif method == 'CLAHE':
                clahe = cv2.createCLAHE(clipLimit=params['clipLimit'], tileGridSize=(params['tileGridSize'], params['tileGridSize']))
                return clahe.apply(gray)

            elif method == 'Transformação Gama':
                return np.array(255 * (gray / 255) ** params['gamma'], dtype='uint8')

            elif method == 'Realce de Contraste':
                kernel = np.array([[0, -1, 0],
                                [-1, params['intensity'], -1],
                                [0, -1, 0]])
                return cv2.filter2D(gray, -1, kernel)

            elif method == 'Normalização do Contraste':
                return cv2.normalize(gray, None, alpha=params['alpha'], beta=params['beta'], norm_type=cv2.NORM_MINMAX)

            elif method == 'Realce Linear':
                return cv2.convertScaleAbs(gray, alpha=params['alpha'], beta=params['beta'])

            elif method == 'Realce Quadrático':
                return np.array(255 * (gray / 255) ** params['power'], dtype='uint8')

            elif method == 'Realce Logarítmico':
                return np.array(255 * np.log1p(gray), dtype='uint8')

        # Seção de Expansão do contraste
        st.sidebar.subheader('Expansão de contraste')
        contraste = st.sidebar.selectbox(
            'Escolha o tipo de expansão de contraste',
            ('Binarizar', 'Equalização de histograma', 'CLAHE', 'Transformação Gama', 'Realce de Contraste', 'Normalização do Contraste', 'Realce Linear', 'Realce Quadrático', 'Realce Logarítmico')
        )

        # Parâmetros para cada técnica
        params = {}

        if contraste == 'Binarizar':
            params['block_size'] = st.sidebar.slider('Tamanho do bloco', min_value=3, max_value=21, step=2, value=11)
            params['C'] = st.sidebar.slider('Constante C', min_value=1, max_value=10, value=2)

        elif contraste == 'CLAHE':
            params['clipLimit'] = st.sidebar.slider('Limite de recorte', min_value=1.0, max_value=4.0, step=0.1, value=2.0)
            params['tileGridSize'] = st.sidebar.slider('Tamanho da grade de blocos', min_value=8, max_value=32, step=2, value=16)

        elif contraste == 'Transformação Gama':
            params['gamma'] = st.sidebar.slider('Valor de gama', min_value=0.1, max_value=3.0, step=0.1, value=1.5)

        elif contraste == 'Realce de Contraste':
            params['intensity'] = st.sidebar.slider('Intensidade do realce', min_value=1, max_value=10, value=5)

        elif contraste == 'Normalização do Contraste':
            params['alpha'] = st.sidebar.slider('Valor alpha', min_value=0, max_value=255, value=0)
            params['beta'] = st.sidebar.slider('Valor beta', min_value=0, max_value=255, value=255)

        elif contraste == 'Realce Linear':
            params['alpha'] = st.sidebar.slider('Valor alpha', min_value=0.1, max_value=3.0, step=0.1, value=0.5)
            params['beta'] = st.sidebar.slider('Valor beta', min_value=0, max_value=100, value=10)

        elif contraste == 'Realce Quadrático':
            params['power'] = st.sidebar.slider('Valor da potência', min_value=1.0, max_value=3.0, step=0.1, value=2.0)

        # Botão para aplicar a Expansão do Contraste
        if st.sidebar.button('Aplicar Expansão de Contraste'):
            result_img = apply_noise_reduction(gray, contraste, params)

            # Exibição da imagem original e da imagem resultante
            with col2:
                st.image(result_img, caption=f"Imagem com {contraste}", use_column_width=True)

#=========================================================================Histograma========================================================================#
    
            # Função para calcular o histograma da imagem
            def calculate_histogram(img):
                hist = cv2.calcHist([img], [0], None, [256], [0, 256])
                return hist
    
            # Função para exibir o histograma
            def plot_histogram(hist):
                plt.figure(figsize=(8, 5))
                plt.title('Histograma')
                plt.xlabel('Intensidade de pixel')
                plt.ylabel('Número de pixels')
                plt.plot(hist, color='gray')
                plt.xlim([0, 256])
                plt.grid(True)
                return plt
    
            # Seção de Histograma
            st.sidebar.subheader('Histograma')
            if st.sidebar.button('Exibir histograma'):
                hist = calculate_histogram(gray)
                plot = plot_histogram(hist)
                with col2:
                    st.pyplot(plot)

if __name__ == "__main__":
    main()

