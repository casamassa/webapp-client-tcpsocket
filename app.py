import streamlit as st
from socket_client import SocketClient
import threading
import queue

st.set_page_config(layout="wide")

def main():
    # Inicializa o cliente de socket
    socketClient = SocketClient(host="127.0.0.1", port=14150)
    
    # Função para exibir as mensagens recebidas em tempo real
    def display_messages():
        while True:
            try:
                ts, message = socketClient.messages_queue.get(timeout=1)
                st.write(f"Data: {ts}, {message}")
            except queue.Empty:
                pass

    # Executa o cliente de socket para estabelecer a conexão e iniciar a recepção de mensagens
    socketClient.run()

    # Exibe uma mensagem inicial
    st.write("Mensagens do servidor:")

    # Inicia a função de exibição de mensagens em uma thread separada
    display_thread = threading.Thread(target=display_messages)
    display_thread.start()

    # Aguarda até que o Streamlit seja fechado
    display_thread.join()

if __name__ == '__main__':
    main()
