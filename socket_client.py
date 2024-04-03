import socket
import threading
import time
import queue
from datetime import datetime

class SocketClient:

    def __init__(self, host="127.0.0.1", port=14150):
        self.HOST = host
        self.PORT = port
        self.messages_queue = queue.Queue()

    def receive_messages(self, sock):
        while True:
            try:
                data = sock.recv(1024)
                if not data:
                    break
                print(f"Mensagem do servidor: {data.decode()}")
                self.messages_queue.put((datetime.now().strftime("%d/%m/%Y %H:%M:%S"), data.decode()))
            except Exception as e:
                print(f"Erro ao receber mensagem do servidor: {e}")
                break

    def keep_connection_alive(self, sock):
        while True:
            time.sleep(10)  # Envia uma mensagem vazia a cada 10 segundos
            try:
                sock.sendall(b"")
            except Exception as e:
                print(f"Erro ao manter a conexão: {e}")
                break

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((self.HOST, self.PORT))
                print(f"Conectado ao servidor: {self.HOST}")
            except Exception as e:
                print(f"Erro ao conectar ao servidor: {e}")
                return

            # Inicia uma thread para receber mensagens do servidor
            receive_thread = threading.Thread(target=self.receive_messages, args=(s,))
            receive_thread.start()

            # Inicia uma thread para manter a conexão ativa
            keep_alive_thread = threading.Thread(target=self.keep_connection_alive, args=(s,))
            keep_alive_thread.start()

            receive_thread.join()  # Espera a thread de recebimento terminar
            keep_alive_thread.join()  # Espera a thread de manutenção da conexão terminar

if __name__ == "__main__":
    socketClient = SocketClient()
    socketClient.run()
