import streamlit as st
import pandas as pd
import socket
import threading
import queue
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from pyepc import decode
import csv

# Inicialize um dicionário vazio
products_dictionary = {}

def get_products_from_file():
    # Open CSV file
    with open('data.csv', newline='', encoding='utf-8') as csvfile:
        # Create an object CSV reader
        reader_csv = csv.reader(csvfile, delimiter=';')
        
        # Run line by line of CSV reader
        for line_csv in reader_csv:
            # Check if the line has 2 columns
            if len(line_csv) == 2:
                # Define the key of dictionary as first element of line and the value as second element of line
                products_dictionary[line_csv[0]] = line_csv[1]

def rule_gs1_checksum(input_string):
    sum_ = 0
    for i in range(len(input_string)):
        n = int(input_string[len(input_string) - 1 - i])
        sum_ += n * 3 if i % 2 == 0 else n

    result = 0 if sum_ % 10 == 0 else 10 - sum_ % 10
    return result

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
    st.set_page_config(layout="wide", page_title="RFID - Portal")

    # Inicializa a fila para armazenar as mensagens recebidas
    messages_queue = queue.Queue()

    get_products_from_file()

    # Conecta ao servidor de socket
    try:
        #HOST = "127.0.0.1"  # Endereço IP do servidor
        HOST = "169.254.1.1"  # Endereço IP do leitor
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
        df = pd.DataFrame(columns=['Data', 'EPC', 'GTIN', 'Serial Number', 'Antena', 'RSSI'])
        dfConsolidado = pd.DataFrame(columns=['Produto','GTIN', 'Quantidade'])
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

            epc = columns[1]
            antenna = columns[0]
            rssi = columns[2]

            sgtin_decoded = decode(epc)
            serial_number = sgtin_decoded.serial_number
            gtin = "0" + sgtin_decoded.company_prefix + "{:0>4}".format(sgtin_decoded.item_ref)
            check_digit = rule_gs1_checksum(gtin)
            gtin = gtin + str(check_digit)
            gtin = gtin.lstrip('0')

            prod_desc = products_dictionary.get(gtin)
            if prod_desc is None:
                prod_desc = "GTIN não cadastrado"

            isNewRow = True
            # Percorrer as linhas existentes do DataFrame e atualizar uma coluna de uma linha específica
            for index, row in dfConsolidado.iterrows():
                if row['GTIN'] == gtin:  # Check if the line has the same gtin
                    dfConsolidado.at[index, 'Quantidade'] = row['Quantidade']+1  # Refresh the column Quantidade
                    isNewRow = False
            if isNewRow:
                dfConsolidado.loc[len(df)] = [prod_desc,gtin, 1]  # Add the line to DataFrame
            
            with placeholderConsolidado.container():
                st.dataframe(dfConsolidado, use_container_width=True, hide_index=True)
            
            df.loc[len(df)] = [ts, epc, gtin, serial_number, antenna, rssi]  # Add the line to DataFrame
            with placeholder.container():
                st.dataframe(df, use_container_width=True, hide_index=True)

            
            # Create the chart bar
            fig, ax = plt.subplots()
            #ax.bar(dfConsolidado['Produto'], dfConsolidado['Quantidade']) #Format column in vertical
            ax.barh(dfConsolidado['Produto'], dfConsolidado['Quantidade']) #Format column in horizontal

            # Define axis labels
            ax.set_xlabel('Quantidade')
            ax.set_ylabel('Produto')
            # Set axis y to display only integer value range
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))

            with placeholderChart.container():
                st.subheader("Produtos lidos x Quantidade")
                # Display the chart on Streamlit
                st.pyplot(fig)
                #st.bar_chart(dfConsolidado)

        except queue.Empty:
            pass

if __name__ == '__main__':
    main()
