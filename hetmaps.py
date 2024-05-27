import matplotlib.pyplot as plt
from mplsoccer import Pitch, heatmap
import pandas as pd

# Crie um DataFrame de exemplo com coordenadas de passes
data = {
    'x': [10, 20, 30, 40, 50, 60, 70],
    'y': [40, 30, 20, 10, 20, 30, 40],
    'completed_pass': [1, 0, 1, 1, 0, 1, 1]
}
passes_df = pd.DataFrame(data)

# Crie um campo de futebol com mplsoccer
pitch = Pitch(pitch_type='statsbomb')

# Crie um gráfico de calor
fig, ax = pitch.draw()
#heatmap(passes_df['x'], passes_df['y'], ax=ax)
stats = pitch.bin_statistic_positional(passes_df['x'], passes_df['y'])
pitch.heatmap_positional(stats, edgecolors='w', cmap='hot', ax=ax)

# Adicione um título
ax.set_title('Gráfico de Calor de Passes Completos')

# Exiba o gráfico
plt.show()
