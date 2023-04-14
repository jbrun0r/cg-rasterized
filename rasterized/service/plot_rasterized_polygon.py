import matplotlib.pyplot as plt
from service.rasterize_half_lines import rasterize_half_lines
from service.fill_rasterized_polygon import fill_rasterized_polygon

def plot_rasterized_polygon(resolutions, aspect_ratio, semirretas, colors):
    for resolution in resolutions:
        img = rasterize_half_lines(resolution, aspect_ratio, semirretas, colors)
        img = fill_rasterized_polygon(img)
        plt.imshow(img)
        plt.gca().invert_yaxis()
        plt.show()
