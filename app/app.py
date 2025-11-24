import tkinter as tk

class MileageTracker:
    def __init__(self, root):
        # Criacao da janela
        self.root = root
        root.title("Mileage tracker")
        root.geometry("400x300")
        # Inicia o loop da aplicação
        



if __name__ == '__main__':
    root = tk.Tk()
    app = MileageTracker(root)
    root.mainloop()