import tkinter as tk
from tkinter import messagebox
from collections import deque
import socket
import threading

HUCRE = 45  #
BG_COLOR = "#263238"

# Renk Paleti
RENK_DUVAR_ANA = "#3E2723"
RENK_DUVAR_HARC = "#5D4037"
RENK_YOL_ANA = "#ECEFF1"
RENK_YOL_KENAR = "#B0BEC5"
RENK_MAVI = "#1976D2"
RENK_KIRMIZI = "#D32F2F"
RENK_HEDEF_DIS = "#FBC02D"
RENK_HEDEF_IC = "#FFF176"
RENK_ROTA = "#76FF03"

# 1: Duvar, 0: Yol, 'S': Başlangıç, 'E': Bitiş
BOLUMLER = [
    # BÖLÜM 1:
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 'S', 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 'E', 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ],
    # BÖLÜM 2:
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 'S', 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 'E', 0, 1],
        [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ],
    # BÖLÜM 3:
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 'S', 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 'E', 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
]


class LabirentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Labirent Pro")
        self.root.configure(bg=BG_COLOR)

        self.level_idx = 0  # Şu anki bölüm indeksi
        self.hamle = 0
        self.oyuncu_pos = None
        self.hedef_pos = None
        self.client_socket = None
        self.current_map = []  # O anki aktif harita matrisi

        self.my_role = 1
        self.my_name = "A Kişisi (Offline)"
        self.my_color = RENK_MAVI
        self.enemy_color = RENK_KIRMIZI

        # --- BUTONLAR ---
        frame = tk.Frame(root, bg=BG_COLOR)
        frame.pack(pady=10)
        btn_style = {"font": ("Arial", 10, "bold"), "bd": 3, "relief": tk.RAISED}

        tk.Button(frame, text="Sıfırla", command=self.restart_level, **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Bilgisayar (BFS)", command=self.bilgisayar_coz, bg="orange", **btn_style).pack(
            side=tk.LEFT, padx=5)
        tk.Button(frame, text="Online Oyna", command=self.online_baglan, bg="#4CAF50", fg="white", **btn_style).pack(
            side=tk.LEFT, padx=5)
        tk.Button(frame, text="Offline Mod", command=self.offline_gec, bg="#546E7A", fg="white", **btn_style).pack(
            side=tk.LEFT, padx=5)

        self.lbl_info = tk.Label(root, text="Bölüm: 1 | Hamle: 0", font=("Arial", 12, "bold"), bg=BG_COLOR, fg="white")
        self.lbl_info.pack(pady=(0, 5))


        self.canvas = tk.Canvas(root, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack()

        self.load_level(0)  # İlk bölümü yükle
        self.root.bind("<KeyPress>", self.klavye_kontrol)

    def load_level(self, level_idx):
        """Belirtilen indeksteki bölümü yükler."""
        self.level_idx = level_idx
        if self.level_idx >= len(BOLUMLER):
            self.level_idx = 0  # Bölümler biterse başa dön

        self.current_map = BOLUMLER[self.level_idx]
        self.rows = len(self.current_map)
        self.cols = len(self.current_map[0])


        new_w = self.cols * HUCRE
        new_h = self.rows * HUCRE
        self.canvas.config(width=new_w, height=new_h)

        # Pencereyi ortala
        self.root.update_idletasks()
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        win_w = new_w + 40  # Kenar boşlukları için
        win_h = new_h + 100
        x = (screen_w // 2) - (win_w // 2)
        y = (screen_h // 2) - (win_h // 2)
        self.root.geometry(f"{win_w}x{win_h}+{x}+{y}")

        self.restart_level()

    def restart_level(self):
        """Mevcut bölümü baştan başlatır."""
        self.canvas.delete("all")
        self.hamle = 0
        self.lbl_info.config(text=f"Bölüm: {self.level_idx + 1} | Hamle: 0 | {self.my_name}")

        for r in range(self.rows):
            for c in range(self.cols):
                val = self.current_map[r][c]
                if val == 'S':
                    self.oyuncu_pos = [r, c]
                    val = 0
                elif val == 'E':
                    self.hedef_pos = [r, c]

                self.kare_ciz_desenli(r, c, val)

        self.oyuncuyu_ciz(self.oyuncu_pos, "ben", self.my_color)

        # Online ise pozisyonu bildir
        if self.client_socket:
            try:
                self.client_socket.send(f"{self.oyuncu_pos[0]},{self.oyuncu_pos[1]}$".encode())
            except:
                pass

    def kare_ciz_desenli(self, r, c, tip):
        x1, y1 = c * HUCRE, r * HUCRE
        x2, y2 = x1 + HUCRE, y1 + HUCRE
        self.canvas.delete(f"cell_{r}_{c}")
        tags = (f"cell_{r}_{c}", "zemin")

        if tip == 1:  # DUVAR
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=RENK_DUVAR_ANA, outline="", tags=tags)
            bd = 2
            self.canvas.create_line(x1, y1 + HUCRE / 2, x2, y1 + HUCRE / 2, fill=RENK_DUVAR_HARC, width=bd, tags=tags)
            self.canvas.create_line(x1 + HUCRE / 2, y1, x1 + HUCRE / 2, y1 + HUCRE / 2, fill=RENK_DUVAR_HARC, width=bd,
                                    tags=tags)
            self.canvas.create_line(x1 + HUCRE / 4, y1 + HUCRE / 2, x1 + HUCRE / 4, y2, fill=RENK_DUVAR_HARC, width=bd,
                                    tags=tags)
            self.canvas.create_line(x2 - HUCRE / 4, y1 + HUCRE / 2, x2 - HUCRE / 4, y2, fill=RENK_DUVAR_HARC, width=bd,
                                    tags=tags)

        elif tip == 'E':  # HEDEF
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=RENK_YOL_ANA, outline=RENK_YOL_KENAR, tags=tags)
            m1 = 6
            self.canvas.create_oval(x1 + m1, y1 + m1, x2 - m1, y2 - m1, fill=RENK_HEDEF_DIS, outline="#F57F17", width=2,
                                    tags=tags)
            m2 = 14
            self.canvas.create_oval(x1 + m2, y1 + m2, x2 - m2, y2 - m2, fill=RENK_HEDEF_IC, outline="", tags=tags)

        elif tip == RENK_ROTA:  # ROTA
            self.canvas.create_rectangle(x1 + 2, y1 + 2, x2 - 2, y2 - 2, fill=RENK_ROTA, outline="", stipple="gray50",
                                         tags=tags)

        else:  # YOL
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=RENK_YOL_ANA, outline=RENK_YOL_KENAR, tags=tags)
            self.canvas.create_rectangle(x1 + 2, y1 + 2, x2 - 2, y2 - 2, outline=RENK_YOL_KENAR, width=1, tags=tags)

    def oyuncuyu_ciz(self, pos, tag, renk):
        self.canvas.delete(tag)
        r, c = pos
        x, y = c * HUCRE, r * HUCRE

        # Fare Çizimi
        self.canvas.create_line(x + HUCRE * 0.5, y + HUCRE * 0.75, x + HUCRE * 0.85, y + HUCRE * 0.95, width=3,
                                fill="black", tags=tag, smooth=True)
        self.canvas.create_oval(x + HUCRE * 0.1, y + HUCRE * 0.1, x + HUCRE * 0.45, y + HUCRE * 0.45, fill=renk,
                                outline="black", tags=tag)
        self.canvas.create_oval(x + HUCRE * 0.55, y + HUCRE * 0.1, x + HUCRE * 0.9, y + HUCRE * 0.45, fill=renk,
                                outline="black", tags=tag)
        self.canvas.create_oval(x + HUCRE * 0.2, y + HUCRE * 0.3, x + HUCRE * 0.8, y + HUCRE * 0.85, fill=renk,
                                outline="black", tags=tag)
        self.canvas.create_oval(x + HUCRE * 0.32, y + HUCRE * 0.45, x + HUCRE * 0.45, y + HUCRE * 0.58, fill="white",
                                outline="black", tags=tag)
        self.canvas.create_oval(x + HUCRE * 0.37, y + HUCRE * 0.5, x + HUCRE * 0.4, y + HUCRE * 0.53, fill="black",
                                tags=tag)
        self.canvas.create_oval(x + HUCRE * 0.55, y + HUCRE * 0.45, x + HUCRE * 0.68, y + HUCRE * 0.58, fill="white",
                                outline="black", tags=tag)
        self.canvas.create_oval(x + HUCRE * 0.6, y + HUCRE * 0.5, x + HUCRE * 0.63, y + HUCRE * 0.53, fill="black",
                                tags=tag)
        self.canvas.create_oval(x + HUCRE * 0.45, y + HUCRE * 0.65, x + HUCRE * 0.55, y + HUCRE * 0.75, fill="black",
                                tags=tag)
        self.canvas.tag_raise(tag)

    def klavye_kontrol(self, event):
        moves = {"Up": (-1, 0), "w": (-1, 0), "Down": (1, 0), "s": (1, 0), "Left": (0, -1), "a": (0, -1),
                 "Right": (0, 1), "d": (0, 1)}
        if event.keysym in moves:
            dr, dc = moves[event.keysym]
            nr, nc = self.oyuncu_pos[0] + dr, self.oyuncu_pos[1] + dc

            # Geçerli harita üzerinden kontrol
            if 0 <= nr < self.rows and 0 <= nc < self.cols and self.current_map[nr][nc] != 1:
                self.oyuncu_pos = [nr, nc]
                self.hamle += 1
                self.lbl_info.config(text=f"Bölüm: {self.level_idx + 1} | Hamle: {self.hamle} | {self.my_name}")
                self.oyuncuyu_ciz(self.oyuncu_pos, "ben", self.my_color)

                if self.client_socket:
                    try:
                        self.client_socket.send(f"{nr},{nc}$".encode())
                    except:
                        pass

                # Kazanma Kontrolü
                if self.oyuncu_pos == self.hedef_pos:
                    if self.client_socket:
                        try:
                            self.client_socket.send(f"WIN:{self.my_role}$".encode())
                        except:
                            pass

                    self.bolum_gec("Tebrikler!", "Bölümü tamamladınız!")

    def bolum_gec(self, baslik, mesaj):
        """Kullanıcıyı bilgilendirir ve sonraki bölüme geçer."""
        messagebox.showinfo(baslik, mesaj)
        next_level = self.level_idx + 1
        if next_level >= len(BOLUMLER):
            messagebox.showinfo("Oyun Bitti", "Tüm bölümleri tamamladınız! Başa dönülüyor.")
            self.load_level(0)
        else:
            self.load_level(next_level)

    def bilgisayar_coz(self):
        self.offline_gec(sessiz=True)
        self.restart_level()
        self.lbl_info.config(text=f"Bölüm: {self.level_idx + 1} | Mod: Bilgisayar")

        queue = deque([(self.oyuncu_pos[0], self.oyuncu_pos[1])])
        visited = {tuple(self.oyuncu_pos): None}
        target = tuple(self.hedef_pos)
        found = False

        while queue:
            curr = queue.popleft()
            if curr == target: found = True; break
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = curr[0] + dr, curr[1] + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if self.current_map[nr][nc] != 1 and (nr, nc) not in visited:
                        visited[(nr, nc)] = curr
                        queue.append((nr, nc))
        if found:
            path = []
            c = target
            while c: path.append(c); c = visited[c]
            path.reverse()
            self.animasyon(path)
        else:
            messagebox.showerror("Hata", "Yol Yok!")

    def animasyon(self, path):
        if not path: return
        r, c = path.pop(0)
        self.oyuncu_pos = [r, c]
        self.kare_ciz_desenli(r, c, RENK_ROTA)
        self.oyuncuyu_ciz([r, c], "ben", self.my_color)
        if path: self.root.after(100, lambda: self.animasyon(path))

    def online_baglan(self):
        if self.client_socket:
            messagebox.showinfo("Bilgi", "Zaten bağlısınız.")
            return
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(('127.0.0.1', 5555))
            threading.Thread(target=self.veri_dinle, daemon=True).start()
            self.lbl_info.config(text="Sunucuya bağlandı...")
        except:
            messagebox.showerror("Hata", "Sunucu kapalı! server.py açık mı?")

    def offline_gec(self, sessiz=False):
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
            self.client_socket = None

        self.my_role = 1
        self.my_name = "A Kişisi (Offline)"
        self.my_color = RENK_MAVI
        self.enemy_color = RENK_KIRMIZI
        self.restart_level()
        if not sessiz:
            self.lbl_info.config(text="Mod: Offline")
            messagebox.showinfo("Mod", "Offline moda geçildi.")

    def veri_dinle(self):
        buffer = ""
        while True:
            try:
                if self.client_socket is None: break
                data = self.client_socket.recv(1024).decode()
                if not data: break
                buffer += data
                while '$' in buffer:
                    paket, buffer = buffer.split('$', 1)
                    if paket.startswith("ID:"):
                        rol = int(paket.split(":")[1])
                        self.my_role = rol
                        if rol == 1:
                            self.my_name = "A Kişisi"
                            self.my_color = RENK_MAVI
                            self.enemy_color = RENK_KIRMIZI
                        else:
                            self.my_name = "B Kişisi"
                            self.my_color = RENK_KIRMIZI
                            self.enemy_color = RENK_MAVI
                        self.root.after(0, lambda: self.root.title(f"Labirent Pro - {self.my_name}"))
                        self.restart_level()  # Kimlik gelince baştan çiz

                    elif paket.startswith("WIN:"):
                        kid = int(paket.split(":")[1])
                        k_isim = "A Kişisi" if kid == 1 else "B Kişisi"
                        # Online oyunda biri kazanınca HERKES bir sonraki tura geçer
                        self.root.after(100, lambda: self.bolum_gec("Tur Bitti",
                                                                    f"{k_isim} kazandı!\nSonraki bölüme geçiliyor..."))

                    elif ',' in paket:
                        r, c = map(int, paket.split(','))
                        self.oyuncuyu_ciz([r, c], "rakip", self.enemy_color)
            except:
                break


if __name__ == "__main__":
    root = tk.Tk()
    app = LabirentApp(root)
    root.mainloop()