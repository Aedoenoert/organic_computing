import pandas as pd
import matplotlib.pyplot as plt

# Pfade zu deiner CSV-Datei
csv_file_path = 'population_ws2324.csv'

# Daten einlesen
data = pd.read_csv(csv_file_path)

# Definitionsbereiche berechnen
data['lower_bound_1'] = data['center_1'] - data['spread_1']
data['upper_bound_1'] = data['center_1'] + data['spread_1']
data['lower_bound_2'] = data['center_2'] - data['spread_2']
data['upper_bound_2'] = data['center_2'] + data['spread_2']

# Definitionsbereich für jedes Merkmal
definitionsbereich_center_1 = (data['lower_bound_1'].min(), data['upper_bound_1'].max())
definitionsbereich_center_2 = (data['lower_bound_2'].min(), data['lower_bound_2'].max())

print("Definitionsbereich center_1:", definitionsbereich_center_1)
print("Definitionsbereich center_2:", definitionsbereich_center_2)



population_length = len(data)
print("Länge der Population", population_length)

# Eindeutige Aktionen zählen
unique_actions = data['action'].unique()
num_unique_actions = len(unique_actions)

print("Anzahl der unterschiedlichen Aktionen:", num_unique_actions)

# Eindeutige Kombinationen von Bedingungen zählen
unique_rules = data[['center_1', 'center_2']].drop_duplicates()
num_unique_rules = len(unique_rules)

print("Anzahl der verschiedenen Regeln in der Population:", num_unique_rules)
