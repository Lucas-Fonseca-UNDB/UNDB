import timeit
import random
import streamlit as st

def heapify(unsorted, index, heap_size):
    # Encontra o maior entre o nó raiz, o filho esquerdo e o filho direito
    largest = index
    left_index = 2 * index + 1
    right_index = 2 * index + 2

    if left_index < heap_size and unsorted[left_index] > unsorted[largest]:
        largest = left_index

    if right_index < heap_size and unsorted[right_index] > unsorted[largest]:
        largest = right_index

    # Troca e continua heapificando se a raiz não for a maior
    if largest != index:
        unsorted[largest], unsorted[index] = unsorted[index], unsorted[largest]
        heapify(unsorted, largest, heap_size)

def heap_sort(unsorted):
    n = len(unsorted)
    # Constrói um max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(unsorted, i, n)
    # Extrai elementos um por um
    for i in range(n - 1, 0, -1):
        unsorted[0], unsorted[i] = unsorted[i], unsorted[0]
        heapify(unsorted, 0, i)
    return unsorted

def main():
    st.title("Heap Sort com Streamlit")
    
    # Entrada do usuário para o número de elementos no array
    num_elements = st.number_input("Digite o número de elementos no array:", min_value=1, step=1)
    
    if st.button("Gerar e Ordenar Array"):
        # Gera uma lista de números aleatórios
        unsorted = [random.randint(0, 100) for i in range(num_elements)]
        original_unsorted = unsorted.copy()
        
        # Exibe a quantidade de números no array e a lista desordenada
        st.write(f"Quantidade de números no array: {num_elements}")
        st.write("Lista desordenada:", original_unsorted)
        
        # Mede o tempo de execução da função heap_sort usando timeit
        execution_time = timeit.timeit(lambda: heap_sort(original_unsorted.copy()), number=1)
        
        # Converte o tempo de execução para segundos e milissegundos
        execution_seconds = int(execution_time)
        execution_milliseconds = (execution_time - execution_seconds) * 1000
        
        # Exibe o tempo de execução formatado
        st.write(f"Tempo de execução: {execution_seconds} segundos e {execution_milliseconds:.3f} milissegundos")
        
        # Ordena a lista e exibe a lista ordenada
        sorted_list = heap_sort(unsorted)
        st.write("Lista ordenada:", sorted_list)
        
        # Prepara os resultados para salvar em um arquivo .txt
        result_text = (
            f"Quantidade de números no array: {num_elements}\n"
            f"Lista desordenada: {original_unsorted}\n"
            f"Tempo de execução: {execution_seconds} segundos e {execution_milliseconds:.3f} milissegundos\n"
            f"Lista ordenada: {sorted_list}\n"
        )
        
        # Adiciona um botão para baixar o arquivo .txt
        st.download_button(
            label="Baixar Resultados",
            data=result_text,
            file_name="resultado.txt",
            mime="text/plain"
        )

if __name__ == "__main__":
    main()