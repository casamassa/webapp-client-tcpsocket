import streamlit as st
import socket
import threading
import queue
from datetime import datetime

# Função para receber mensagens do servidor em uma thread separada
def receive_messages(sock, messages_queue):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            messages_queue.put((datetime.now().strftime("%d/%m/%Y %H:%M:%S"), data.decode()))
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
        st.write("Conectado ao servidor de socket.")
    except Exception as e:
        st.error(f"Erro ao conectar ao servidor de socket: {e}")
        return

    # Inicia a thread para receber mensagens do servidor
    receive_thread = threading.Thread(target=receive_messages, args=(s, messages_queue))
    receive_thread.start()

    # Exibe as mensagens recebidas em tempo real
    st.write("Mensagens do servidor:")
    while True:
        try:
            ts, message = messages_queue.get(timeout=1)
            st.write(f"Data: {ts}, {message}")
        except queue.Empty:
            pass

if __name__ == '__main__':
    main()
