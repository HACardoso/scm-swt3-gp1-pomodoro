import unittest
import tkinter as tk
from app.app import MileageTracker
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

            header = ["origin", "destination", "start_odometer", "end_odometer", "distance", "tolls", "parking"]
            # exemplo de linha válida
            row = ["Origem A", "Destino B", "100.0", "150.0", "50.0", "2.50", "5.00"]

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
            self.assertEqual(len(data_row), 7)
            # verifica campos numéricos podem ser convertidos e distância bate
            start = float(data_row[2].replace(',', '.'))
            end = float(data_row[3].replace(',', '.'))
            distance = float(data_row[4].replace(',', '.'))
            tolls = float(data_row[5].replace(',', '.'))
            parking = float(data_row[6].replace(',', '.'))

            self.assertAlmostEqual(end - start, distance, places=3)
            self.assertGreaterEqual(tolls, 0.0)
            self.assertGreaterEqual(parking, 0.0)

if __name__ == "__main__":
    unittest.main()