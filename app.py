import streamlit as st
from socket_client import SocketClient
import threading

st.set_page_config(layout="wide")

def main():
    # Inicializa o cliente de socket
    socketClient = SocketClient(host="127.0.0.1", port=14150)

    # Função para executar o cliente de socket em uma thread separada
    def run_socket_client():
        socketClient.run()

    # Inicia o cliente de socket em uma thread separada
    socket_thread = threading.Thread(target=run_socket_client)
    socket_thread.start()

    # Exibe uma mensagem simples no Streamlit
    st.write("Hello world")

if __name__ == '__main__':
    main()
