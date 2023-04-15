import numpy as np
from service.rasterize_normalized_line import rasterize_normalized_line

def rasterize_half_lines(resolution, aspect_ratio=True, semirretas=None, colors=None):
    """
    Rasteriza uma lista de semirretas em uma imagem.

    Parâmetros
    ----------
    resolution : int ou tuple(int, int)
        Resolução da imagem a ser gerada. Se um número inteiro for fornecido, 
        será usado como largura e altura da imagem. Se uma tupla (largura, altura) 
        for fornecida, será usada para especificar a largura e altura da imagem 
        respectivamente.
    aspect_ratio : bool, opcional
        Se True, mantém a proporção da imagem em 16:9, fazendo com que a altura 
        seja calculada automaticamente com base na largura. O padrão é True.
    semirretas : list, opcional
        Uma lista de semirretas a serem rasterizadas. Cada semirreta é definida
        por uma lista de dois pontos: [ponto_inicial, ponto_final]. O padrão é uma
        lista de quatro semirretas pré-definidas: vertical, horizontal e duas diagonais.
    colors : list, opcional
        Uma lista de cores a serem usadas para desenhar as semirretas. O padrão é uma
        lista de quatro cores pré-definidas: vermelho, verde, azul e amarelo.

    Retorna
    -------
    img : numpy.ndarray, shape (height, width, 3), dtype=np.uint8
        A imagem rasterizada como uma matriz numpy de três dimensões (RGB).

    Exemplos
    --------
    >>> semirretas = [
    ...     [(0, -1), (0, 1)],         # Semirreta vertical
    ...     [(-1, 0), (1, 0)],         # Semirreta horizontal
    ...     [(-1, -1), (1, 1)],     # Semirreta inclinada na direção positiva
    ...     [(1, -1), (-1, 1)],  # Semirreta inclinada na direção oposta
    ... ]
    >>> colors = [
    ...     (255, 0, 0),  # Vermelho
    ...     (0, 255, 0),  # Verde
    ...     (0, 0, 255),  # Azul
    ...     (255, 255, 0),  # Amarelo
    ... ]
    >>> img = rasterize_semirretas(512, True, semirretas, colors)

    >>> img = rasterize_semirretas((640, 480), False)
    """
    
    ASPECT_RATIO = 16/9
    if isinstance(resolution, int):
        width = height = resolution
    else:
        width, height = resolution
        if aspect_ratio:
            height = int(width/ASPECT_RATIO)  # Proporção de aspecto 16:9
    img = np.zeros((height, width, 3), dtype=np.uint8)
    if semirretas is None:
        semirretas = [
            [(0, -1), (0, 1)],         # Semirreta vertical
            [(-1, 0), (1, 0)],         # Semirreta horizontal
            [(-1, -1), (1, 1)],     # Semirreta inclinada na direção positiva
            [(1, -1), (-1, 1)],  # Semirreta inclinada na direção oposta
        ]

    for i, semirreta in enumerate(semirretas):
        pixels = rasterize_normalized_line(semirreta[0][0], semirreta[0][1], semirreta[1][0], semirreta[1][1], width, height, aspect_ratio)
        for x, y in pixels:
            if x >= 0 and x < width and y >= 0 and y < height:
                if colors is None:
                    img[y, x] = (255,255,255)
                elif len(colors) == 1:
                    img[y, x] = colors[0]
                else:
                    img[y, x] = colors[i]
                    
    return img
