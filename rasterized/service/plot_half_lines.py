import matplotlib.pyplot as plt
from service.rasterize_half_lines import rasterize_half_lines

def plot_half_lines(resolutions, aspect_ratio, semirretas, colors):
    for resolution in resolutions:
        img = rasterize_half_lines(resolution, aspect_ratio=aspect_ratio, semirretas = semirretas, colors=colors)
        plt.imshow(img)
        plt.show()
