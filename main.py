import streamlit as st
import pandas as pd
import socket
import threading
import queue
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Função para receber mensagens do servidor em uma thread separada
def receive_messages(sock, messages_queue):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            messages_queue.put((datetime.now().strftime("%d/%m/%Y %H:%M:%S"), data.decode()))
            print(f"Msg do server: {data.decode()}")
        except Exception as e:
            print(f"Erro ao receber mensagem do servidor: {e}")
            break

# Função principal
def main():
    st.set_page_config(layout="wide")

    # Inicializa a fila para armazenar as mensagens recebidas
    messages_queue = queue.Queue()

    # Conecta ao servidor de socket
    try:
        HOST = "127.0.0.1"  # Endereço IP do servidor
        PORT = 14150  # Porta do servidor
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        # Define o emoji de bola verde
        green_ball_emoji = "\U0001F7E2"  # Unicode para o emoji de bola verde
        # Concatena o emoji com o texto
        status_text = f"{green_ball_emoji} Conectado ao leitor: {HOST}:{PORT}"
        # Exibe o texto com o emoji
        st.write(status_text)
        
        # Cria um DataFrame vazio para armazenar as mensagens
        df = pd.DataFrame(columns=['Data', 'EPC', 'Antena', 'RSSI'])
        dfConsolidado = pd.DataFrame(columns=['EPC', 'Quantidade'])
    except Exception as e:
        # Define o emoji de bola vermelha
        red_ball_emoji = "\U0001F534"  # Unicode para o emoji de bola vermelha
        # Concatena o emoji com o texto
        status_text = f"{red_ball_emoji} Não conectado ao leitor: {HOST}:{PORT}"
        # Exibe o texto com o emoji
        st.write(status_text)
        st.error(f"Erro ao conectar ao leitor: {e}")
        return

    # Inicia a thread para receber mensagens do servidor
    receive_thread = threading.Thread(target=receive_messages, args=(s, messages_queue))
    receive_thread.start()

    tab1, tab2, tab3 = st.tabs(["Resumo", "EPC's", "Gráfico"])
    with tab1:
        placeholderConsolidado = st.empty()
    with tab2:
        placeholder = st.empty()
    with tab3:
        placeholderChart = st.empty()
    
    while True:
        try:
            ts, message = messages_queue.get(timeout=1)

            columns = message.split(',')
            if len(columns) < 3:
                continue

            isNewRow = True
            # Percorrer as linhas existentes do DataFrame e atualizar uma coluna de uma linha específica
            for index, row in dfConsolidado.iterrows():
                if row['EPC'] == columns[1]:  # Verifica se a linha tem o mesmo timestamp
                    dfConsolidado.at[index, 'Quantidade'] = row['Quantidade']+1  # Atualiza a coluna 'Mensagem' para a nova mensagem
                    isNewRow = False
            if isNewRow:
                dfConsolidado.loc[len(df)] = [columns[1], 1]  # Adiciona a mensagem ao DataFrame
            
            with placeholderConsolidado.container():
                st.dataframe(dfConsolidado, use_container_width=True, hide_index=True)
            
            df.loc[len(df)] = [ts, columns[1], columns[0], columns[2]]  # Adiciona a mensagem ao DataFrame
            with placeholder.container():
                st.dataframe(df, use_container_width=True, hide_index=True)

            
            # Criando o gráfico de barras
            fig, ax = plt.subplots()
            #ax.bar(dfConsolidado['EPC'], dfConsolidado['Quantidade']) #Formato Coluna vertical
            ax.barh(dfConsolidado['EPC'], dfConsolidado['Quantidade']) #Formato Coluna horizontal

            # Definindo os rótulos dos eixos
            ax.set_xlabel('Quantidade')
            ax.set_ylabel('EPC')
            # Configurando o eixo y para exibir apenas valores inteiros
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))

            with placeholderChart.container():
                st.subheader("Produtos lidos x Quantidade")
                # Exibindo o gráfico no Streamlit
                st.pyplot(fig)
                #st.bar_chart(dfConsolidado)


        except queue.Empty:
            pass

if __name__ == '__main__':
    main()
