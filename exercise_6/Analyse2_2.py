import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

# CSV-Datei einlesen
file_path = 'population_ws2324.csv'
df = pd.read_csv(file_path)

# Eindeutige Aktionen in der Population identifizieren
unique_actions = df['action'].unique()

# Farbzuordnung für Aktionen definieren
action_colors = {'yellow': 'yellow', 'brown': 'brown', 'black': 'black', 'blue': 'blue', 'beige': 'beige', 'red': 'red', 'white': 'white'}
"""
# Figure und Axis erstellen
fig, ax = plt.subplots(figsize=(10, 6))

# Jede Regel in der Population durchgehen und Rechtecke zeichnen
for index, row in df.iterrows():
    action = row['action']
    color = action_colors.get(action, 'gray')  # Falls die Aktion nicht in der Farbzuordnung ist, verwende grau

    # Rechteck um den Definitionsbereich zeichnen
    rect = Rectangle((row['center_1'] - row['spread_1'], row['center_2'] - row['spread_2']),
                     2 * row['spread_1'], 2 * row['spread_2'], linewidth=1, edgecolor='black', facecolor=color, alpha=0.5)
    ax.add_patch(rect)

# Achsentitel und Legende hinzufügen
plt.xlabel('center_1')
plt.ylabel('center_2')
plt.title('2D Darstellung der Classifier mit Berücksichtigung der Spreads')

# Legende für Aktionen hinzufügen
legend_patches = [Rectangle((0, 0), 1, 1, color=color, alpha=0.5, label=action) for action, color in action_colors.items()]
ax.legend(handles=legend_patches, title='Aktionen', loc='upper right')

# Plot anzeigen
plt.show()
"""


# Figure und Axis erstellen
fig, ax = plt.subplots(figsize=(10, 6))

# Jede Regel in der Population durchgehen und Punkte zeichnen
for index, row in df.iterrows():
    action = row['action']
    color = action_colors.get(action, 'gray')  # Falls die Aktion nicht in der Farbzuordnung ist, verwende grau

    # Punkt um den Center zeichnen
    ax.scatter(row['center_1'], row['center_2'], color=color, label=action)

# Achsentitel und Legende hinzufügen
plt.xlabel('center_1')
plt.ylabel('center_2')
plt.title('2D Darstellung der Classifier')

# Legende für Aktionen hinzufügen
legend_patches = [Rectangle((0, 0), 1, 1, color=color, label=action) for action, color in action_colors.items()]
ax.legend(handles=legend_patches, title='Aktionen', loc='upper right')

# Plot anzeigen
plt.show()
