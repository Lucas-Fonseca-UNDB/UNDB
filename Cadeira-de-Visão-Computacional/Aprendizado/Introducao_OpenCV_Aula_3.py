import cv2
import numpy as np
import streamlit as st

def detect_points(image: np.ndarray) -> np.ndarray:
    corners = cv2.goodFeaturesToTrack(image, 100, 0.01, 10)
    corners = np.int0(corners)
    for corner in corners:
        x, y = corner.ravel()
        cv2.circle(image, (x, y), 3, 255, -1)
    return image

def detect_lines(image: np.ndarray) -> np.ndarray:
    edges = cv2.Canny(image, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
    if lines is not None:
        for rho, theta in lines[:, 0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            x2 = int(x0 - 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            y2 = int(y0 - 1000 * (a))
            cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
    return image

def detect_edges(image: np.ndarray, method: str) -> np.ndarray:
    if method == "Canny":
        edges = cv2.Canny(image, 100, 200)
    elif method == "Roberts":
        kernelx = np.array([[1, 0], [0, -1]], dtype=int)
        kernely = np.array([[0, 1], [-1, 0]], dtype=int)
        edges_x = cv2.filter2D(image, cv2.CV_16S, kernelx)
        edges_y = cv2.filter2D(image, cv2.CV_16S, kernely)
        edges = cv2.convertScaleAbs(edges_x + edges_y)
    elif method == "Sobel":
        edges = cv2.Sobel(image, cv2.CV_64F, 1, 1, ksize=3)
        edges = cv2.convertScaleAbs(edges)
    elif method == "Prewitt":
        kernelx = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]], dtype=int)
        kernely = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=int)
        edges_x = cv2.filter2D(image, cv2.CV_16S, kernelx)
        edges_y = cv2.filter2D(image, cv2.CV_16S, kernely)
        edges = cv2.convertScaleAbs(edges_x + edges_y)
    elif method == "Laplaciano":
        edges = cv2.Laplacian(image, cv2.CV_64F)
        edges = cv2.convertScaleAbs(edges)
    return edges

def main():
    st.title("Detecção de Características em Imagens")
    
    uploaded_file = st.file_uploader("Escolha uma imagem...", type=["jpg", "jpeg", "png"])
    detection_type = st.selectbox("Escolha o tipo de detecção", ["Pontos", "Linhas", "Canny", "Roberts", "Sobel", "Prewitt", "Laplaciano"])
    
    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        gray_img = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)

        # Aplicar a técnica de detecção selecionada
        if detection_type == "Pontos":
            result_img = detect_points(gray_img.copy())
        elif detection_type == "Linhas":
            result_img = detect_lines(gray_img.copy())
        else:
            result_img = detect_edges(gray_img.copy(), detection_type)

        # Criar colunas para input e output
        col1, col2 = st.columns(2)
        
        # Exibir a imagem original na primeira coluna
        with col1:
            img = cv2.imdecode(file_bytes, 0)
            st.image(img, caption='Imagem Original', use_column_width=True)
        
        # Exibir a imagem com a técnica de detecção aplicada na segunda coluna
        with col2:
            st.image(result_img, caption=f'{detection_type} Detectadas', use_column_width=True)

#======================================================================Redução de ruídos=====================================================================#

if __name__ == "__main__":
    main()