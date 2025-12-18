import socket
import threading

# Sunucu Ayarları
HOST = '0.0.0.0'  # Tüm ağlardan bağlantıyı kabul et
PORT = 5555

clients = []


def handle_client(client_socket, addr, player_id):
    print(f"[YENİ BAĞLANTI] {addr} bağlandı. ID: {player_id}")

    # Oyuncuya kimliğini bildir (1 veya 2)
    try:
        client_socket.send(f"ID:{player_id}$".encode())
    except:
        return

    while True:
        try:
            msg = client_socket.recv(1024)
            if not msg:
                break

            # Gelen mesajı diğer oyuncuya ilet
            for c in clients:
                if c != client_socket:
                    try:
                        c.send(msg)
                    except:
                        clients.remove(c)
        except:
            break

    print(f"[AYRILDI] {addr} bağlantısı koptu.")
    if client_socket in clients:
        clients.remove(client_socket)
    client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(2)
    print(f"[DİNLİYOR] Sunucu {HOST}:{PORT} üzerinde açık...")

    player_id = 1
    while True:
        client_sock, addr = server.accept()
        clients.append(client_sock)

        # İlk gelen 1 (Mavi), İkinci gelen 2 (Kırmızı) olur
        pid = 1 if len(clients) == 1 else 2

        thread = threading.Thread(target=handle_client, args=(client_sock, addr, pid))
        thread.start()


if __name__ == "__main__":
    start_server()