import random
import timeit

def heapify(unsorted, index, heap_size):
    largest = index
    left_index = 2 * index + 1
    right_index = 2 * index + 2

    if left_index < heap_size and unsorted[left_index] > unsorted[largest]:
        largest = left_index

    if right_index < heap_size and unsorted[right_index] > unsorted[largest]:
        largest = right_index

    if largest != index:
        unsorted[index], unsorted[largest] = unsorted[largest], unsorted[index]
        heapify(unsorted, largest, heap_size)

# O tipo de caminhamento utilizado na função heapify é pré-ordem (preorder traversal).
# Isso ocorre porque a função processa o nó atual (raiz) antes de processar seus filhos.
# A ordem é:
# 1. Processa o nó atual.
# 2. Processa o filho esquerdo.
# 3. Processa o filho direito.

def heap_sort(unsorted):
    n = len(unsorted)
    for i in range(n // 2 - 1, -1, -1):
        heapify(unsorted, i, n)
    for i in range(n - 1, 0, -1):
        unsorted[0], unsorted[i] = unsorted[i], unsorted[0]
        heapify(unsorted, 0, i)
    return unsorted

if __name__ == "__main__":
    try:
        num_elements = int(input("Digite o número de elementos no array: ").strip())
    except ValueError:
        print("Por favor, insira um número inteiro válido.")
        exit(1)

    unsorted = [random.randint(0, 100) for i in range(num_elements)]
    original_unsorted = unsorted.copy()
    print(f"Quantidade de números no array: {num_elements}")
    print("Lista desordenada:", original_unsorted)

    # Mede o tempo de execução usando timeit
    execution_time = timeit.timeit(lambda: heap_sort(original_unsorted.copy()), number=1)

    # Converte o tempo de execução para segundos e milissegundos
    execution_seconds, execution_milliseconds = divmod(execution_time * 1000, 1000)
    execution_milliseconds = int(execution_milliseconds)

    print(f"Tempo de execução: {int(execution_seconds)} segundos e {execution_milliseconds} milissegundos")

    # Ordena a lista e imprime a lista ordenada
    sorted_list = heap_sort(unsorted)
    print("Lista ordenada:", sorted_list)
