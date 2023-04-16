import matplotlib.pyplot as plt
from service.rasterize_half_lines import rasterize_half_lines

def plot_half_lines(resolutions, aspect_ratio, semirretas, colors):
    """
    Plota as semirretas, primeiro na forma de linhas contínuas e, 
    em seguida, rasteriza em diferentes resoluções.

    Args:
        resolutions (list): Lista de tuplas representando as diferentes resoluções para rasterizar as semirretas.
            Cada tupla contém a largura e a altura da imagem em pixels (exemplo: [(200, 200), (400, 400), (800, 800)]).
        aspect_ratio (float): Proporção entre a largura e a altura do espaço onde as semirretas estão contidas.
        semirretas (list): Lista de listas contendo as coordenadas (x, y) das extremidades das semirretas.
            Cada sublista contém duas tuplas com as coordenadas das extremidades da semirreta (exemplo: [[(0, 0), (1, 1)], [(1, 1), (2, 0)]]).
        colors (list): Lista de tuplas de três valores (R, G, B) especificando a cor das semirretas e do polígono.

    Returns:
        None (exibe o plot diretamente)

    Raises:
        None
    """
    
    # Mostra as semirretas no modelo continuo
    fig, ax = plt.subplots()
    # Percorrendo todas as arestas 
    for aresta in semirretas:
            x = [p[0] for p in aresta]
            y = [p[1] for p in aresta]
            ax.plot(x, y)

    fig, ax1 = plt.subplots(figsize=(20,10))
    for resolution in resolutions:

        # Rasteriza as semirretas na resolução escolhida
        img = rasterize_half_lines(resolution, aspect_ratio, semirretas, colors)
        
        # Mostra as semirretas rasterizadas no primeiro subplot
        ax1.imshow(img)
        ax1.set_title(f'Semirretas rasterizadas - Resolução: {resolution[0]} x {resolution[1]}')
        ax1.invert_yaxis()
        ax1.axis('off')
        
        # Mostra os subplots
        plt.show()
