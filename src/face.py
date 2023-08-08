import tkinter as tk

class FaceGUI:
    def __init__(self, master, strategia):
        self.master = master
        self.strategia = strategia  # Instância da classe Strat
        master.title("Robô Arbety")
        master.geometry("800x600")
        master.configure(bg="#163340")
        
        
        # Texto extraído da imagem
        self.title_text = "DOUBLE ARBETY"
        
        # Título no centro e acima
        self.title_label = tk.Label(master, text=self.title_text, font=("Arial", 24), bg="#163340", fg="white")
        self.title_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        # Central frame
        self.center_frame = tk.Frame(master, bg="#163340")
        self.center_frame.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        # Banca
        self.bankroll_label = tk.Label(self.center_frame, text="Banca: 50,00", font=("Arial", 16), bg="#163340", fg="white")
        self.bankroll_label.grid(row=0, column=0, padx=20, pady=10)

        # Lucro
        self.profit_label = tk.Label(self.center_frame, text="Lucro: 0,00", font=("Arial", 16), bg="#163340", fg="white")
        self.profit_label.grid(row=0, column=1, padx=20, pady=10)

        # Acertos e Perdas
        self.hits_label = tk.Label(self.center_frame, text="Acertos: 0", font=("Arial", 16), bg="#163340", fg="white")
        self.hits_label.grid(row=1, column=0, padx=20, pady=10)
        self.losses_label = tk.Label(self.center_frame, text="Perdas: 0", font=("Arial", 16), bg="#163340", fg="white")
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
        self.toggle_robot_button = tk.Button(self.center_frame, text="Ligar/Desligar Robô", font=("Arial", 16), command=self.toggle_robot_status)
        self.toggle_robot_button.grid(row=4, column=0, padx=20, pady=10, columnspan=2)

        # Canvas para desenhar as bolas coloridas
        self.canvas = tk.Canvas(self.center_frame, width=520, height=60, bg="white")
        self.canvas.grid(row=5, column=0, padx=50, pady=50, columnspan=3)
        self.draw_balls()

        # Status do robô (inicialmente desligado)
        self.robot_status = False

    def atualizar_banca(self):
        banca = self.strategia.valor_aposta
        self.bankroll_label.config(text=f"Banca: {banca:.2f}")
        

    
    def toggle_robot_status(self):
        self.robot_status = not self.robot_status
        status_text = "Robô Ligado" if self.robot_status else "Robô Desligado"
        self.robot_status_label.config(text=status_text)
        if self.robot_status:
            self.strategia.ligar_robo()
        else:
            self.strategia.desligar_robo()
        self.draw_balls()

    def draw_balls(self):
        # Desenhar uma caixa cinza
        self.canvas.create_rectangle(2, 2, 520, 60, fill="gray")
        # Aqui você pode adicionar lógica para desenhar as bolas conforme suas cores
        # ...

    # Você pode adicionar outras funções para atualizar outros elementos da interface conforme necessário

