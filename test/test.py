import unittest
import tkinter as tk
from app.app import MileageTracker, ExpenseCalculator
import tempfile
import os
import csv


class Test1(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.app = MileageTracker(self.root)

    def tearDown(self):
        self.root.destroy()
    

    def test_window_opens(self):

        print(self.app.root.title())
        self.assertEqual(self.app.root.title(), "Mileage tracker")

    def test_smoke_write_and_validate_csv(self):
        # smoke-test que escreve diretamente no CSV e valida formato e valores
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = os.path.join(tmp, "data")
            os.makedirs(data_dir, exist_ok=True)
            csv_path = os.path.join(data_dir, "trips.csv")

            header = ["origin", "destination", "start_odometer", "end_odometer", "distance", "tolls", "parking", "km_expense", "total_expense"]
            # exemplo de linha válida
            row = ["Origem A", "Destino B", "100.0", "150.0", "50.0", "2.50", "5.00", "25.00", "32.50"]

            # escreve arquivo
            with open(csv_path, "w", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerow(row)

            # lê e valida
            with open(csv_path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)

            # valida header
            self.assertGreaterEqual(len(rows), 2)
            self.assertEqual(rows[0], header)

            # valida a linha de dados
            data_row = rows[1]
            self.assertEqual(len(data_row), 9)
            # verifica campos numéricos podem ser convertidos e distância bate
            start = float(data_row[2].replace(',', '.'))
            end = float(data_row[3].replace(',', '.'))
            distance = float(data_row[4].replace(',', '.'))
            tolls = float(data_row[5].replace(',', '.'))
            parking = float(data_row[6].replace(',', '.'))
            km_expense = float(data_row[7].replace(',', '.'))
            total_expense = float(data_row[8].replace(',', '.'))

            self.assertAlmostEqual(end - start, distance, places=3)
            self.assertGreaterEqual(tolls, 0.0)
            self.assertGreaterEqual(parking, 0.0)
            self.assertGreaterEqual(km_expense, 0.0)
            self.assertGreaterEqual(total_expense, 0.0)


class TestExpenseCalculator(unittest.TestCase):
    """Testes unitários para a classe ExpenseCalculator"""
    
    def setUp(self):
        """Configura um calculador com taxa padrão de R$ 0.50/km"""
        self.calculator = ExpenseCalculator(km_rate=0.50)
    
    def test_calculate_km_expense_basic(self):
        """Testa o cálculo básico de despesa por km"""
        result = self.calculator.calculate_km_expense(100)
        self.assertEqual(result, 50.00)
    
    def test_calculate_km_expense_decimal(self):
        """Testa cálculo com distância decimal"""
        result = self.calculator.calculate_km_expense(50.5)
        self.assertEqual(result, 25.25)
    
    def test_calculate_km_expense_zero(self):
        """Testa cálculo com distância zero"""
        result = self.calculator.calculate_km_expense(0)
        self.assertEqual(result, 0.00)
    
    def test_calculate_km_expense_negative_raises_error(self):
        """Testa que distância negativa levanta ValueError"""
        with self.assertRaises(ValueError):
            self.calculator.calculate_km_expense(-10)
    
    def test_calculate_total_expense_all_components(self):
        """Testa cálculo total com todos os componentes"""
        result = self.calculator.calculate_total_expense(100, 20.50, 15.00)
        
        self.assertEqual(result['distance_km'], 100.00)
        self.assertEqual(result['km_expense'], 50.00)
        self.assertEqual(result['tolls'], 20.50)
        self.assertEqual(result['parking'], 15.00)
        self.assertEqual(result['total'], 85.50)
    
    def test_calculate_total_expense_only_distance(self):
        """Testa cálculo com apenas quilometragem"""
        result = self.calculator.calculate_total_expense(75)
        
        self.assertEqual(result['distance_km'], 75.00)
        self.assertEqual(result['km_expense'], 37.50)
        self.assertEqual(result['tolls'], 0.00)
        self.assertEqual(result['parking'], 0.00)
        self.assertEqual(result['total'], 37.50)
    
    def test_calculate_total_expense_with_tolls_only(self):
        """Testa cálculo com apenas pedágios"""
        result = self.calculator.calculate_total_expense(50, tolls=25.00)
        
        self.assertEqual(result['distance_km'], 50.00)
        self.assertEqual(result['km_expense'], 25.00)
        self.assertEqual(result['tolls'], 25.00)
        self.assertEqual(result['parking'], 0.00)
        self.assertEqual(result['total'], 50.00)
    
    def test_calculate_total_expense_with_parking_only(self):
        """Testa cálculo com apenas estacionamento"""
        result = self.calculator.calculate_total_expense(30, parking=10.00)
        
        self.assertEqual(result['distance_km'], 30.00)
        self.assertEqual(result['km_expense'], 15.00)
        self.assertEqual(result['tolls'], 0.00)
        self.assertEqual(result['parking'], 10.00)
        self.assertEqual(result['total'], 25.00)
    
    def test_calculate_total_expense_string_inputs(self):
        """Testa cálculo com inputs em string"""
        result = self.calculator.calculate_total_expense("100", "20.50", "15")
        
        self.assertEqual(result['distance_km'], 100.00)
        self.assertEqual(result['km_expense'], 50.00)
        self.assertEqual(result['tolls'], 20.50)
        self.assertEqual(result['parking'], 15.00)
        self.assertEqual(result['total'], 85.50)
    
    def test_calculate_total_expense_negative_distance_raises_error(self):
        """Testa que distância negativa levanta ValueError"""
        with self.assertRaises(ValueError):
            self.calculator.calculate_total_expense(-10, 5, 5)
    
    def test_calculate_total_expense_negative_tolls_raises_error(self):
        """Testa que pedágio negativo levanta ValueError"""
        with self.assertRaises(ValueError):
            self.calculator.calculate_total_expense(100, -5, 5)
    
    def test_calculate_total_expense_negative_parking_raises_error(self):
        """Testa que estacionamento negativo levanta ValueError"""
        with self.assertRaises(ValueError):
            self.calculator.calculate_total_expense(100, 5, -5)
    
    def test_calculate_total_expense_invalid_distance_string(self):
        """Testa que string inválida para distância levanta ValueError"""
        with self.assertRaises(ValueError):
            self.calculator.calculate_total_expense("abc", 5, 5)
    
    def test_get_expense_summary_format(self):
        """Testa se o resumo é formatado corretamente"""
        summary = self.calculator.get_expense_summary(100, 20.50, 15.00)
        
        # Verifica se contém os campos esperados
        self.assertIn("RESUMO DE DESPESAS", summary)
        self.assertIn("Distância: 100.00 km", summary)
        self.assertIn("Despesa km: R$ 50.00", summary)
        self.assertIn("Pedágios: R$ 20.50", summary)
        self.assertIn("Estacionamento: R$ 15.00", summary)
        self.assertIn("TOTAL: R$ 85.50", summary)
    
    def test_custom_km_rate(self):
        """Testa calculador com taxa personalizada"""
        custom_calculator = ExpenseCalculator(km_rate=0.75)
        result = custom_calculator.calculate_km_expense(100)
        self.assertEqual(result, 75.00)
    
    def test_precision_rounding(self):
        """Testa que os valores são arredondados corretamente para 2 casas decimais"""
        result = self.calculator.calculate_total_expense(33.33, 12.345, 9.876)
        
        # Verifica precisão de 2 casas decimais
        self.assertEqual(result['km_expense'], 16.67)
        self.assertEqual(result['tolls'], 12.35)
        self.assertEqual(result['parking'], 9.88)


class TestExpenseCalculatorEdgeCases(unittest.TestCase):
    """Testes para casos extremos"""
    
    def setUp(self):
        self.calculator = ExpenseCalculator(km_rate=0.50)
    
    def test_very_large_distance(self):
        """Testa com distância muito grande"""
        result = self.calculator.calculate_total_expense(10000)
        self.assertEqual(result['km_expense'], 5000.00)
        self.assertEqual(result['total'], 5000.00)
    
    def test_very_small_distance(self):
        """Testa com distância muito pequena"""
        result = self.calculator.calculate_total_expense(0.01)
        self.assertEqual(result['km_expense'], 0.01)
    
    def test_empty_string_for_tolls_and_parking(self):
        """Testa que strings vazias são tratadas como 0"""
        result = self.calculator.calculate_total_expense(100, "", "")
        self.assertEqual(result['tolls'], 0.00)
        self.assertEqual(result['parking'], 0.00)
        self.assertEqual(result['total'], 50.00)


if __name__ == "__main__":
    unittest.main()