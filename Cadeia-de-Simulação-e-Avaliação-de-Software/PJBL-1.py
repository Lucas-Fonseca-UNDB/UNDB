import streamlit as st
import math

def main():
    st.title("Simulador de Filas M/M/1")
    st.subheader("Cadeira de Simulação e Avaliação de Software - 8° período")
    st.write("Prof.Dr. ALISSON JORGE SILVA ALMEIDA")
    st.write("Grupo: Lucas Fonseca, Luis Rodrigo, Pedro Arthur, Osvaldo Saboia, Diogo Soares")
    #st.markdown("---")

    # Coleta de entradas com limitações
    servidor = 1
    lambda_value = st.number_input("Digite a taxa de chegada de clientes:", min_value=1, max_value=999, step=1)
    unidade_lambda_value = st.selectbox("Escolha a unidade para taxa de chegada:", ["Hora", "Minuto"])
    mu = st.number_input("Digite a taxa de atendimentos:", min_value=1, max_value=999, step=1)
    unidade_mu = st.selectbox("Escolha a unidade para taxa de atendimento:", ["Hora", "Minuto"])

    if unidade_lambda_value == "Minuto":
        lambda_value = lambda_value / 60
    if unidade_mu == "Minuto":
        mu = 60 / mu

    ρ = lambda_value / mu
    n = 1  # Assumindo n como 1, você pode ajustar isso conforme necessário

    st.markdown("---")
    st.subheader("Cálculos")

    calculo_opcoes = [
        "Taxa de ocupação",
        "Probabilidade de ter fila",
        "Probabilidade de ter mais clientes no sistema",
        "Número médio de clientes no sistema",
        "Número médio de clientes na fila",
        "Tempo médio de espera na fila",
        "Tempo médio gasto no sistema por cliente"
    ]

    calculo_selecionado = st.selectbox("Selecione o cálculo desejado:", calculo_opcoes)

    if st.button("Realizar Cálculo"):
        resultado = None
        unidade = ""
        if calculo_selecionado == "Probabilidade de ter fila":
            resultado = (ρ**(n + 1)) * 100
            unidade = "%"
        elif calculo_selecionado == "Probabilidade de ter mais clientes no sistema":
            resultado = ((ρ**n) * (1-ρ)) * 100
            unidade = "%"
        elif calculo_selecionado == "Número médio de clientes no sistema":
            resultado = lambda_value / (mu - lambda_value)
            unidade = " clientes"
        elif calculo_selecionado == "Número médio de clientes na fila":
            resultado = (lambda_value**2) / (mu * (mu - lambda_value))
            unidade = " clientes"
        elif calculo_selecionado == "Tempo médio de espera na fila":
            resultado = (lambda_value / (mu * (mu - lambda_value))) * 60
            unidade = " Minutos"
        elif calculo_selecionado == "Tempo médio gasto no sistema por cliente":
            resultado = (1 / (mu - lambda_value)) * 60
            unidade = " Minutos"
        elif calculo_selecionado == "Taxa de ocupação":
            resultado = ρ
            unidade = "%"

        if resultado is not None:
            st.markdown("---")
            st.subheader("Resultado")
            st.markdown(f"<h3 style='text-align: center; color: #1c83e1;'>{calculo_selecionado}: {resultado:.2f}{unidade}</h3>", unsafe_allow_html=True)

    st.markdown("---")
    st.write("Obrigado por usar o Simulador de Filas!")

if __name__ == "__main__":
    main()
