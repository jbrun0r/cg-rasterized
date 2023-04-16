import numpy as np

def fill_rasterized_polygon(img: np.ndarray, colors) -> np.ndarray:
    """
    Preenche um polígono rasterizado com as cores especificadas.

    Args:
        img (np.ndarray): um array numpy representando a imagem rasterizada do polígono.
        colors (List[Tuple[int, int, int]]): uma lista de tuplas de três valores (R, G, B) especificando a cor de preenchimento.

    Returns:
        np.ndarray: um array numpy representando a imagem com o polígono preenchido.

    Raises:
        TypeError: se `img` não for um array numpy ou `colors` não for uma lista de tuplas de três inteiros.

    Example:
        >>> img = np.zeros((10, 10))
        >>> img[1:9, 1:9] = 1
        >>> colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        >>> filled_img = fill_rasterized_polygon(img, colors)
    """
    
    # Encontre o valor mínimo e máximo de y e x
    min_yx = np.min(np.transpose(np.where(img != 0)), axis=0)
    max_yx = np.max(np.transpose(np.where(img != 0)), axis=0)
    min_y, min_x = min_yx[0], min_yx[1]
    max_y, max_x = max_yx[0], max_yx[1]
    
    # Percorra cada linha verticalmente
    for y in range(min_y, max_y + 1):

        # Verifique se a linha contém pelo menos um pixel dentro do polígono
        if np.any(img[y] != 0):

            # Encontre os pontos de interseção da linha com as arestas do polígono
            intersections = []
            for x in range(min_x, max_x + 1):
                if (img[y, x] != 0).any():
                    intersections.append(x)

            # Ordene os pontos de interseção em ordem crescente de x
            intersections.sort()

            # Preencha o intervalo entre cada par de interseções
            for i in range(0, len(intersections), 2):
                start = intersections[i]
                end = intersections[i + 1] if i + 1 < len(intersections) else max_x
                color = colors[(i//2) % len(colors)]
                img[y, start:end] = color
                
    return img
