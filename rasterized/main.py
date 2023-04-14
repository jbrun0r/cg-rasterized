import numpy as np
import matplotlib.pyplot as plt
from tkinter import *

from service.plot_rasterized_polygon import plot_rasterized_polygon

# windows = Tk()
# windows.mainloop()

resolutions = [100, 300, 600, (800, 600), (1920, 1080)]

semirretas = [
    [(0, 0.866), (0.5, 0)],  # Semirreta da aresta de baixo
    [(0.5, 0), (-0.5, 0)],  # Semirreta da aresta da direita
    [(-0.5, 0), (0, 0.866)]  # Semirreta da aresta da esquerda
]

colors = [
    (255, 255, 255),
    (255, 255, 255),
    (255, 255, 255),
]

plot_rasterized_polygon(resolutions, True, semirretas, colors)
