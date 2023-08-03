import tkinter as tk

class FaceGUI:
    def __init__(self, master):
        self.master = master
        master.title("Robô Arbety")
        master.geometry("800x550")
        master.configure(bg="#163340")
        
        # Texto extraído da imagem
        self.title_text = "DOUBLE MILLION"

        # Central frame
        self.center_frame = tk.Frame(master, bg="#163340")
        self.center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

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
        self.toggle_robot_button = tk.Button(self.center_frame, text="Ligar/Desligado Robô", font=("Arial", 16), command=self.toggle_robot_status)
        self.toggle_robot_button.grid(row=4, column=0, padx=20, pady=10, columnspan=2)

        # Canvas para desenhar as bolas coloridas
        self.canvas = tk.Canvas(self.center_frame, width=100, height=100, bg="white")
        self.canvas.grid(row=5, column=0, padx=20, pady=10, columnspan=2)
        self.draw_balls()

        # Status do robô (inicialmente desligado)
        self.robot_status = False

    def toggle_robot_status(self):
        self.robot_status = not self.robot_status
        self.robot_status_label.config(text="Robô Ligado" if self.robot_status else "Robô Desligado")
        self.draw_balls()

    def draw_balls(self):
        # Desenhar bolas coloridas no canvas
        self.canvas.create_oval(10, 10, 30, 30, fill="red")
        self.canvas.create_oval(40, 10, 60, 30, fill="green")
        self.canvas.create_oval(70, 10, 90, 30, fill="white")

# Criando a janela principal
root = tk.Tk()
face_gui = FaceGUI(root)
root.mainloop()
