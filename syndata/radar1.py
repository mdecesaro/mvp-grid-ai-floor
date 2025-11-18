import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
# Configurações do gráfico
# -----------------------------
n = 12
angles = np.linspace(0, 2*np.pi, n, endpoint=False) + np.pi/2

labels = ["Frontal", "Frontal Left", "Diagonal Left Up", "Lateral Left",
          "Diagonal Left Down", "Back Left", "Back", "Back Right",
          "Diagonal Right Down", "Lateral Right", "Diagonal Right Up", "Frontal Right"]

# -----------------------------
# Médias por setor
# -----------------------------
sector_means = {
    "Frontal": 656.69,
    "Frontal Left": 709.45,
    "Diagonal Left Up": 818.20,
    "Lateral Left": 764.34,
    "Diagonal Left Down": 695.36,
    "Back Left": 734.55,
    "Back": 877.06,
    "Back Right": 681.65,
    "Diagonal Right Down": 860.56,
    "Lateral Right": 579.45,
    "Diagonal Right Up": 631.10,
    "Frontal Right": 695.68
}

MAX_TIME = 1300
values = np.array([sector_means[label] for label in labels])
values_normalized = values / MAX_TIME
# -----------------------------
# Polígono do atleta
# -----------------------------
x = np.append(values_normalized * np.cos(angles), values_normalized[0] * np.cos(angles[0]))
y = np.append(values_normalized * np.sin(angles), values_normalized[0] * np.sin(angles[0]))

# Dodecágono de referência
R = 1
x_poly = np.append(R * np.cos(angles), R * np.cos(angles[0]))
y_poly = np.append(R * np.sin(angles), R * np.sin(angles[0]))

# -----------------------------
# Plot moderno
# -----------------------------
fig, ax = plt.subplots(figsize=(7,7), facecolor='#1e1e2f')
ax.set_facecolor('#1e1e2f')

# Dodecágono
ax.plot(x_poly, y_poly, color='#888888', linewidth=1.5, linestyle='--')

# Polígono do atleta
ax.plot(x, y, color='#00ffe0', linewidth=1)
ax.fill(x, y, color='#00ffe0', alpha=0.50)

# Linhas radiais
for i in range(n):
    ax.plot([0, x_poly[i]], [0, y_poly[i]], color='#555555', linestyle='--', linewidth=0.8)

# -----------------------------
# Offsets iniciais para cada setor
# -----------------------------

# Deslocamento radial (distância do centro)
offsets = [0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12]

# Deslocamento vertical (cima/baixo)
vertical_offsets = [-0.20, -0.18, -0.14, -0.08, -0.03, 0.03, 0.03, 0.01, -0.03, -0.08, -0.14, -0.18]

# Deslocamento horizontal (direita/esquerda)
horizontal_offsets = [0.0, 0.07, 0.09, 0.11, 0.10, 0.07, 0.0, -0.05, -0.05, -0.10, -0.08, -0.05]

for i, label in enumerate(labels):
    # Label principal
    ax.text(1.15 * np.cos(angles[i]),
            1.15 * np.sin(angles[i]),
            label,
            ha='center', va='center',
            color='white', fontsize=11, weight='bold')
    
    # Valor do tempo, com deslocamentos radial, vertical e horizontal
    r = 1.15 + offsets[i]
    x_pos = r * np.cos(angles[i]) + horizontal_offsets[i]
    y_pos = r * np.sin(angles[i]) + vertical_offsets[i]
    
    ax.text(x_pos, y_pos,
            f"{sector_means[label]:.0f} ms",
            ha='center', va='center',
            color='#00ffe0', fontsize=10, weight='bold')


# Ajustes finais
ax.set_aspect('equal')
ax.axis('off')
plt.show()
