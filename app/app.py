import tkinter as tk
from tkinter import messagebox
import csv
import os
from datetime import datetime

class ExpenseCalculator:
    """
    Classe responsável por calcular as despesas consolidadas de uma viagem.
    Consolida o custo total baseado na quilometragem, pedágios e taxas de estacionamento.
    """
    
    # Taxa padrão por quilômetro (em R$)
    DEFAULT_KM_RATE = 0.50
    
    def __init__(self, km_rate=None):
        """
        Inicializa o calculador de despesas.
        
        Args:
            km_rate (float): Taxa de reembolso por km (padrão: R$ 0.50/km)
        """
        self.km_rate = km_rate if km_rate is not None else self.DEFAULT_KM_RATE
    
    def calculate_km_expense(self, distance):
        """
        Calcula a despesa baseada na quilometragem.
        
        Args:
            distance (float): Distância em km
            
        Returns:
            float: Despesa de quilometragem em R$
        """
        if distance < 0:
            raise ValueError("Distância não pode ser negativa")
        return round(distance * self.km_rate, 2)
    
    def calculate_total_expense(self, distance, tolls=0, parking=0):
        """
        Calcula a despesa total consolidada.
        
        Args:
            distance (float): Distância em km
            tolls (float): Valor de pedágios em R$
            parking (float): Valor de estacionamento em R$
            
        Returns:
            dict: Dicionário com detalhamento das despesas
                {
                    'distance_km': float,
                    'km_expense': float,
                    'tolls': float,
                    'parking': float,
                    'total': float
                }
        """
        try:
            tolls = float(tolls) if tolls else 0
            parking = float(parking) if parking else 0
            distance = float(distance)
            
            if distance < 0:
                raise ValueError("Distância não pode ser negativa")
            if tolls < 0:
                raise ValueError("Pedágio não pode ser negativo")
            if parking < 0:
                raise ValueError("Estacionamento não pode ser negativo")
            
            km_expense = self.calculate_km_expense(distance)
            total = round(km_expense + tolls + parking, 2)
            
            return {
                'distance_km': round(distance, 2),
                'km_expense': km_expense,
                'tolls': round(tolls, 2),
                'parking': round(parking, 2),
                'total': total
            }
        except ValueError as e:
            raise ValueError(f"Erro no cálculo de despesas: {str(e)}")
    
    def get_expense_summary(self, distance, tolls=0, parking=0):
        """
        Retorna um resumo formatado das despesas.
        
        Args:
            distance (float): Distância em km
            tolls (float): Valor de pedágios em R$
            parking (float): Valor de estacionamento em R$
            
        Returns:
            str: String formatada com resumo das despesas
        """
        expense = self.calculate_total_expense(distance, tolls, parking)
        summary = (
            f"=== RESUMO DE DESPESAS ===\n"
            f"Distância: {expense['distance_km']:.2f} km\n"
            f"Despesa km: R$ {expense['km_expense']:.2f}\n"
            f"Pedágios: R$ {expense['tolls']:.2f}\n"
            f"Estacionamento: R$ {expense['parking']:.2f}\n"
            f"─────────────────────────\n"
            f"TOTAL: R$ {expense['total']:.2f}"
        )
        return summary


class MileageTracker:
    def __init__(self, root):
        # Criacao da janela
        self.root = root
        root.title("Mileage tracker")
        root.geometry("600x480")
        
        # Inicializa o calculador de despesas com taxa padrão de R$ 0.50/km
        self.expense_calculator = ExpenseCalculator(km_rate=0.50)

        # Campos do formulário
        frame = tk.Frame(root, padx=10, pady=10)
        frame.pack(fill='both', expand=True)

        tk.Label(frame, text="Endereço Origem:").grid(row=0, column=0, sticky='w')
        self.entry_origin = tk.Entry(frame, width=50)
        self.entry_origin.grid(row=0, column=1, pady=2)

        tk.Label(frame, text="Endereço Destino:").grid(row=1, column=0, sticky='w')
        self.entry_dest = tk.Entry(frame, width=50)
        self.entry_dest.grid(row=1, column=1, pady=2)

        tk.Label(frame, text="Hodômetro Inicial:").grid(row=2, column=0, sticky='w')
        self.entry_start = tk.Entry(frame, width=20)
        self.entry_start.grid(row=2, column=1, sticky='w', pady=2)

        tk.Label(frame, text="Hodômetro Final:").grid(row=3, column=0, sticky='w')
        self.entry_end = tk.Entry(frame, width=20)
        self.entry_end.grid(row=3, column=1, sticky='w', pady=2)

        tk.Label(frame, text="Pedágios (R$):").grid(row=4, column=0, sticky='w')
        self.entry_tolls = tk.Entry(frame, width=20)
        self.entry_tolls.grid(row=4, column=1, sticky='w', pady=2)

        tk.Label(frame, text="Estacionamento (R$):").grid(row=5, column=0, sticky='w')
        self.entry_parking = tk.Entry(frame, width=20)
        self.entry_parking.grid(row=5, column=1, sticky='w', pady=2)

        self.btn_save = tk.Button(frame, text="Salvar Viagem", command=self.save_trip)
        self.btn_save.grid(row=6, column=0, columnspan=2, pady=10)

        self.status = tk.Label(frame, text="", fg="green")
        self.status.grid(row=7, column=0, columnspan=2)
        
        # Área para visualizar resumo de despesas
        tk.Label(frame, text="Resumo de Despesas:", font=("Arial", 9, "bold")).grid(row=8, column=0, sticky='w', pady=(10,0))
        self.expense_text = tk.Text(frame, width=80, height=5)
        self.expense_text.grid(row=9, column=0, columnspan=2, pady=2)
        self.expense_text.config(state='disabled')  # Somente leitura

        # area para visualizar últimos registros
        tk.Label(frame, text="Últimos registros:", font=("Arial", 9, "bold")).grid(row=10, column=0, sticky='w', pady=(10,0))
        self.listbox = tk.Listbox(frame, width=80, height=5)
        self.listbox.grid(row=11, column=0, columnspan=2, pady=2)

        # garante pasta de dados e carrega existentes
        self.data_dir = os.path.join(os.getcwd(), "data")
        os.makedirs(self.data_dir, exist_ok=True)
        self.csv_path = os.path.join(self.data_dir, "trips.csv")
        self.load_existing()

    def load_existing(self):
        self.listbox.delete(0, tk.END)
        if os.path.exists(self.csv_path):
            with open(self.csv_path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    self.listbox.insert(tk.END, " | ".join(row))

    def save_trip(self):
        origin = self.entry_origin.get().strip()
        dest = self.entry_dest.get().strip()
        start = self.entry_start.get().strip()
        end = self.entry_end.get().strip()
        tolls = self.entry_tolls.get().strip() or "0"
        parking = self.entry_parking.get().strip() or "0"

        # validações simples
        if not origin or not dest or not start or not end:
            messagebox.showerror("Erro", "Preencha origem, destino e hodômetros.")
            return
        try:
            start_f = float(start.replace(',', '.'))
            end_f = float(end.replace(',', '.'))
            tolls_f = float(tolls.replace(',', '.'))
            parking_f = float(parking.replace(',', '.'))
        except ValueError:
            messagebox.showerror("Erro", "Hodômetros e valores devem ser numéricos.")
            return

        distance = end_f - start_f
        if distance < 0:
            messagebox.showerror("Erro", "Hodômetro final menor que inicial.")
            return

        # escreve no CSV (adiciona header se não existir)
        new_row = [origin, dest, f"{start_f:.1f}", f"{end_f:.1f}", f"{distance:.1f}", f"{tolls_f:.2f}", f"{parking_f:.2f}"]
        write_header = not os.path.exists(self.csv_path)
        with open(self.csv_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow(["origin", "destination", "start_odometer", "end_odometer", "distance", "tolls", "parking"])
            writer.writerow(new_row)

        self.status.config(text="Viagem salva com sucesso.")
        self.load_existing()
        # limpa campos
        self.entry_origin.delete(0, tk.END)
        self.entry_dest.delete(0, tk.END)
        self.entry_start.delete(0, tk.END)
        self.entry_end.delete(0, tk.END)
        self.entry_tolls.delete(0, tk.END)
        self.entry_parking.delete(0, tk.END)


if __name__ == '__main__':
    root = tk.Tk()
    app = MileageTracker(root)
    root.mainloop()