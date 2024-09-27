import streamlit as st
import math

def main():
    st.title("Simulador de Filas M/M/c")
    st.subheader("Cadeira de Simulação e Avaliação de Software - 8° período")
    st.write("Prof.Dr. ALISSON JORGE SILVA ALMEIDA")
    st.write("Grupo: Lucas Fonseca, Luis Rodrigo, Pedro Arthur, Osvaldo Saboia, Diogo Soares")

    # Coleta de entradas com limitações
    c = st.number_input("Digite o número de servidores:", min_value=1, max_value=999, step=1)
    lambda_value = st.number_input("Digite a taxa de chegada de clientes:", min_value=1, max_value=999, step=1)
    unidade_lambda_value = st.selectbox("Escolha a unidade para taxa de chegada:", ["Hora", "Minuto"])
    mu = st.number_input("Digite a taxa de atendimentos:", min_value=1, max_value=999, step=1)
    unidade_mu = st.selectbox("Escolha a unidade para taxa de atendimento:", ["Hora", "Minuto"])

    if unidade_lambda_value == "Minuto":
        lambda_value = lambda_value / 60
    if unidade_mu == "Minuto":
        mu = 60 / mu

    ρ = lambda_value / (c * mu)

    st.markdown("---")
    st.subheader("Cálculos")

    # Adiciona o selectbox para escolher o cálculo
    calculo_selecionado = st.selectbox("Escolha o cálculo a ser realizado:", [
        "Taxa de ocupação (ρ)",
        "Probabilidade de ter fila (P0)",
        "Número médio de clientes na fila (Lq)",
        "Número médio de clientes no sistema (L)",
        "Tempo médio de espera na fila (Wq)",
        "Tempo médio gasto no sistema por cliente (W)"
    ])

    # Cálculos para o sistema M/M/c
    def calc_p0(c, ρ):
        if ρ == 1:
            return 0  # ou algum outro valor apropriado para tratar o caso especial
        sum_terms = sum((c * ρ) ** n / math.factorial(n) for n in range(c))
        last_term = (c * ρ) ** c / (math.factorial(c) * (1 - ρ))
        return 1 / (sum_terms + last_term)

    if ρ == 1:
        st.error("A taxa de ocupação (ρ) não pode ser igual a 1.")
    else:
        p0 = calc_p0(c, ρ)
        Lq = (p0 * (c * ρ) ** c * ρ) / (math.factorial(c) * (1 - ρ) ** 2)
        L = Lq + c * ρ
        Wq = Lq / lambda_value
        W = Wq + 1 / mu

        if calculo_selecionado == "Taxa de ocupação (ρ)":
            resultado = ρ
            unidade = "%"
        elif calculo_selecionado == "Probabilidade de ter fila (P0)":
            resultado = p0
            unidade = "%"
        elif calculo_selecionado == "Número médio de clientes na fila (Lq)":
            resultado = Lq
            unidade = "%"
        elif calculo_selecionado == "Número médio de clientes no sistema (L)":
            resultado = L
            unidade = "%"
        elif calculo_selecionado == "Tempo médio de espera na fila (Wq)":
            resultado = Wq
            unidade = "%"
        elif calculo_selecionado == "Tempo médio gasto no sistema por cliente (W)":
            resultado = W
            unidade = "%"

    if resultado is not None:
        st.markdown("---")
        st.subheader("Resultado")
        st.markdown(f"<h3 style='text-align: center; color: #1c83e1;'>{calculo_selecionado}: {resultado:.2f}{unidade}</h3>", unsafe_allow_html=True)

    st.markdown("---")
    st.write("Obrigado por usar o Simulador de Filas!")

if __name__ == "__main__":
    main()