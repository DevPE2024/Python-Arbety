import tkinter as tk
from strat import Strat
import queue

class FaceGUI:
    def __init__(self, master, strategia):
        self.master = master
        self.strategia = strategia  
        master.title("Robô Arbety")
        master.geometry("700x550")
        master.configure(bg="#163340")
        self.continuous_update()

        # Texto extraído da imagem
        self.title_text = "DOUBLE ARBETY"

        # Título no centro e acima
        self.title_label = tk.Label(master, text=self.title_text, font=("Arial", 24), bg="#163340", fg="white")
        self.title_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        # Central frame
        self.center_frame = tk.Frame(master, bg="#163340")
        self.center_frame.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        # Banca
        self.bankroll_label = tk.Label(self.center_frame, text=f"Banca: {self.strategia.valor_aposta}", font=("Arial", 16), bg="#163340", fg="white")
        self.bankroll_label.grid(row=0, column=0, padx=20, pady=10)

        # Lucro
        self.profit_label = tk.Label(self.center_frame, text=f"Lucro: {self.calculate_profit()}", font=("Arial", 16), bg="#163340", fg="white")
        self.profit_label.grid(row=0, column=1, padx=20, pady=10)

        # Acertos e Perdas
        self.hits_label = tk.Label(self.center_frame, text=f"Acertos: {self.strategia.acertos}", font=("Arial", 16), bg="#163340", fg="white")
        self.hits_label.grid(row=1, column=0, padx=20, pady=10)
        self.losses_label = tk.Label(self.center_frame, text=f"Perdas: {self.strategia.quantidade_perdas}", font=("Arial", 16), bg="#163340", fg="white")
        self.losses_label.grid(row=1, column=1, padx=20, pady=10)

        # Valor da Aposta
        self.bet_value_label = tk.Label(self.center_frame, text="Valor da Aposta:", font=("Arial", 16), bg="#163340", fg="white")
        self.bet_value_label.grid(row=2, column=0, padx=20, pady=10)
        self.bet_value_entry = tk.Entry(self.center_frame, font=("Arial", 16))
        self.bet_value_entry.grid(row=2, column=1, padx=20, pady=10)

        # Status do Robô
        self.robot_status_label = tk.Label(self.center_frame, text="Robô Desligado", font=("Arial", 16), bg="#163340", fg="white")
        self.robot_status_label.grid(row=3, column=0, padx=20, pady=10, columnspan=2)

        # Botão para alternar o status do robô
        self.toggle_robot_button = tk.Button(self.center_frame, text="Ligar/Desligado Robô", font=("Arial", 16), command=self.toggle_robot_status)
        self.toggle_robot_button.grid(row=4, column=0, padx=20, pady=10, columnspan=2)

        # Canvas para desenhar as bolas coloridas
        self.canvas = tk.Canvas(self.center_frame, width=520, height=60, bg="white")
        self.canvas.grid(row=5, column=0, padx=50, pady=50, columnspan=3)

        # Status do robô (inicialmente desligado)
        self.robot_status = False

    def toggle_robot_status(self):
        self.robot_status = not self.robot_status
        self.robot_status_label.config(text="Robô Ligado" if self.robot_status else "Robô Desligado")
         # No momento da ativação do robô, não atualizamos o valor da aposta diretamente. Apenas usamos o valor da UI quando necessário.
        if self.robot_status:
            valor_aposta = float(self.bet_value_entry.get())
            if valor_aposta <= self.strategia.saldo_inicial:
                print("Robô Ligado")
            else:
                print("Valor da aposta é maior do que a banca disponível!")
                self.robot_status = False
                self.robot_status_label.config(text="Robô Desligado")


    def update_balls(self):
        cores = self.strategia.get_last_colors()
        if len(cores) > 0:  # Verifica se cores não é uma lista vazia
            self.start_drawing_balls(cores)
            self.update_labels()
            if self.robot_status:
                self.master.after(1000, self.update_balls)
        
            else:
                print("Lista vazia, estamos esperando as cores.")
                if self.robot_status:  # Se o robô ainda estiver ligado
                    self.master.after(5000, self.update_balls)  # Tente novamente em 5 segundos
                else:
                    print("Erro ao obter as cores!")
                    self.robot_status = False
                    self.robot_status_label.config(text="Robô Desligado")


    def start_drawing_balls(self, colors):
        # Desenhar uma caixa cinza
        self.canvas.create_rectangle(2, 2, 520, 60, fill="gray")
       
        # Loop para criar as bolas
        for i in range(len(colors)):
            x1 = 20 + i * 30
            y1 = 20
            x2 = x1 + 20
            y2 = y1 + 20

            self.canvas.create_oval(x1, y1, x2, y2, fill=colors[i])
            
    def continuous_update(self):
        self.update_balls()
        self.master.after(1000, self.continuous_update)  


    def calculate_profit(self):
        return self.strategia.lucro  

    def update_labels(self):
        try:
            self.bankroll_label.config(text=f"Banca: {self.strategia.valor_aposta}")
            self.profit_label.config(text=f"Lucro: {self.strategia.lucro}")
            self.hits_label.config(text=f"Acertos: {self.strategia.acertos}")
            self.losses_label.config(text=f"Perdas: {self.strategia.quantidade_perdas}")
        except tk.TclError:
            pass

