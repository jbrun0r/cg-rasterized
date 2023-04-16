# Rasterizar

### GUI
Desenvolvida para consumir as função desenvolvidades neste projeto de forma mais amigavel nesta GUI você pode inserir as coordenadas para plot semirretas e polígonos. A GUI mostra as semirretas no modelo contínuo, as semirretas rasterizadas e se as semirretas compõem um polígono convexo mostra a imagem resultante com o polígono preenchido no subplot do gráfico.

![png](https://github.com/jbrun0r/cg-rasterized/blob/assets/rasterized/assets/Captura%20de%20tela%20de%202023-04-16%2000-51-34.png?raw=true)


#### Default
A GUI é carregada com um polígono default, a GUI plota as semirretas definidas no modelo contínuo, as arestas do polígono rasterizado e depois o polígono preenchido na cor escolhida nos subplots do gráfico.

![png](https://github.com/jbrun0r/cg-rasterized/blob/assets/rasterized/assets/Captura%20de%20tela%20de%202023-04-16%2000-52-30.png?raw=true)

### Service

```python
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox
import  tkinter as tk
```


```python
def rasterize_line(x0, y0, x1, y1):
    """Rasteriza uma reta.

    Args:
        x0 (int): coordenada x do ponto inicial da reta.
        y0 (int): coordenada y do ponto inicial da reta.
        x1 (int): coordenada x do ponto final da reta.
        y1 (int): coordenada y do ponto final da reta.

    Returns:
        list: lista de tuplas (x, y) representando os pixels que a reta atravessa.

    Exemplo:
    >>> rasterize_line(0, 0, 5, 5)
    [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    """
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1
    err = dx - dy
    
    pixels = []
    
    if dx >= dy:
        while True:
            pixels.append((x0, y0))
            if x0 == x1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
    else:
        while True:
            pixels.append((x0, y0))
            if y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dx:
                err -= dx
                y0 += sy
            if e2 < dy:
                err += dy
                x0 += sx
    
    return pixels
```

Este é um algoritmo de rasterização de linhas, que é baseado no algoritmo de Bresenham para determinar quais pixels devem ser ativados ao desenhar uma linha entre dois pontos em um plano cartesiano.

O algoritmo começa calculando as diferenças entre as coordenadas x e y dos dois pontos, e então determina a direção em que a linha deve ser desenhada (isto é, se ela deve ser desenhada da esquerda para a direita ou da direita para a esquerda, de cima para baixo ou de baixo para cima). Em seguida, o algoritmo utiliza um loop para percorrer cada pixel da linha, calculando o erro entre a posição atual do pixel e a posição ideal da linha em cada iteração. Com base neste erro, o algoritmo determina qual pixel deve ser ativado para desenhar a linha da maneira mais precisa possível.

O resultado é uma lista de tuplas que contém as coordenadas x e y de cada pixel ao longo da linha. Esta lista pode ser utilizada para desenhar a linha na tela ou em outro contexto de rasterização.

O algoritmo funciona por meio de uma abordagem incremental, calculando os pixels da linha um por vez. Ele utiliza a ideia de erro acumulado para determinar qual dos dois pixels próximos deve ser escolhido para a linha, com base em qual tem a menor distância para o valor real da linha.

Assim, o algoritmo é otimizado em relação a outros algoritmos que precisam fazer cálculos matemáticos mais complexos para determinar os pixels da linha.

O algoritmo trata as situações em que |Δx| > |Δy| e |Δy| > |Δx|. Ele verifica se dx (a diferença entre as coordenadas x dos pontos inicial e final) é maior ou igual a dy (a diferença entre as coordenadas y dos pontos inicial e final), e escolhe entre desenhar a reta ao longo do eixo x ou y com base nessa condição.

O algoritmo também trata as situações em que as semirretas crescem (m > 0) ou decrescem (m < 0), porque ele utiliza o valor de sx e sy para determinar o sentido da reta em relação ao eixo x e y. Se x0 é maior que x1, sx é definido como -1, o que indica que a reta está se movendo para a esquerda. Se y0 é maior que y1, sy é definido como -1, o que indica que a reta está se movendo para baixo.

O algoritmo também lida com situações em que a reta é horizontal ou vertical. Se a diferença entre as coordenadas x é zero (ou seja, a reta é vertical), o algoritmo apenas adiciona o pixel atual (x0, y0) à lista de pixels e incrementa y0 até que y0 alcance y1. Se a diferença entre as coordenadas y é zero (ou seja, a reta é horizontal), o algoritmo faz o mesmo, mas incrementa x0 em vez de y0.


```python
def rasterize_normalized_line(x0, y0, x1, y1, width, height, aspect_ratio):
    """Rasteriza uma reta definida pelos pontos (x0, y0) e (x1, y1)
    em uma imagem com a resolução dada por (width, height).

    A reta pode ser definida por coordenadas normalizadas entre -1 e 1, onde
    (-1,-1) representa o canto inferior esquerdo e 
    (1,1) representa o canto superior direito da imagem.
    A imagem pode ter um aspect ratio diferente de 1:1,
    caso em que a reta será proporcional à resolução, com a menor dimensão
    sendo usada para manter o aspect ratio correto.

    Args:
        x0 (float): Coordenada x do ponto inicial da reta, normalizada entre -1 e 1.
        y0 (float): Coordenada y do ponto inicial da reta, normalizada entre -1 e 1.
        x1 (float): Coordenada x do ponto final da reta, normalizada entre -1 e 1.
        y1 (float): Coordenada y do ponto final da reta, normalizada entre -1 e 1.
        width (int): Largura da imagem em pixels.
        height (int): Altura da imagem em pixels.
        aspect_ratio (bool, optional): Se True (default), mantém o aspect ratio da imagem.

    Returns:
        list: Lista de tuplas (x, y) representando os pixels da reta rasterizada.

    Raises:
        TypeError: Se os argumentos não forem do tipo correto.
        ValueError: Se o aspect ratio não for um booleano.

    Exemplo:
        Para rasterizar uma reta com as coordenadas normalizadas
        (-0.5, -0.5) e (0.5, 0.5) em uma imagem com resolução de 256x256, 
        mantendo o aspect ratio, pode-se chamar a função assim:
        >>> rasterize_normalized_line(-0.5, -0.5, 0.5, 0.5, 256, 256)
    """

    # Reta original
    # Em vez de simplesmente converter as coordenadas normalizadas para as 
    # coordenadas de pixel usando a fórmula int((x + 1) * (size - 1) / 2), 
    # podemos usar a fórmula int(x * min(size) / 2 + min(size) / 2)
    # que leva em consideração a menor dimensão entre width e height.
    # Dessa forma, a imagem será exibida com o aspect ratio correto.
    if(aspect_ratio):
      # Encontra a menor dimensão entre width e height
      min_size = min(width, height)

      # Converte as coordenadas normalizadas para as coordenadas de pixel
      x0 = int(x0 * min_size / 2 + min_size / 2)
      y0 = int(y0 * min_size / 2 + min_size / 2)
      x1 = int(x1 * min_size / 2 + min_size / 2)
      y1 = int(y1 * min_size / 2 + min_size / 2)
    
    # Reta proporcional a resolução
    else:
      # Converte as coordenadas normalizadas para as coordenadas de pixel
      x0 = int((x0 + 1) * (width - 1) / 2)
      y0 = int((y0 + 1) * (height - 1) / 2)
      x1 = int((x1 + 1) * (width - 1) / 2)
      y1 = int((y1 + 1) * (height - 1) / 2)

    # Rasteriza a reta
    pixels = rasterize_line(x0, y0, x1, y1)

    return pixels
```

A função rasterize_normalized_line é responsável por rasterizar uma reta definida por dois pontos normalizados em uma imagem com uma determinada resolução. Os pontos normalizados possuem coordenadas x e y entre -1 e 1, enquanto a resolução é dada por um par de valores inteiros width e height.

A função pode opcionalmente manter o aspect ratio da imagem, fazendo com que a menor dimensão da imagem seja utilizada para a rasterização da reta, de forma que o aspect ratio seja mantido. Isso é útil quando se quer manter a proporção correta da imagem, evitando que a reta seja distorcida.

A função começa convertendo as coordenadas normalizadas dos pontos para as coordenadas de pixel da imagem. Para fazer essa conversão, ela utiliza a fórmula int(x * min_size / 2 + min_size / 2) quando o aspect ratio é mantido, e int((x + 1) * (width - 1) / 2) quando o aspect ratio não é mantido. A primeira fórmula leva em consideração a menor dimensão entre width e height, enquanto a segunda considera a resolução inteira.

Depois de converter as coordenadas normalizadas para as coordenadas de pixel, a função chama a função rasterize_line que efetivamente rasteriza a reta na imagem. Essa função é implementada em um módulo externo chamado rasterize_line, que não é mostrado aqui.

Por fim, a função retorna uma matriz numpy representando os pixels da reta rasterizada. Se ocorrer algum erro durante a execução da função, a mesma levanta exceções do tipo TypeError ou ValueError, de acordo com o tipo de erro encontrado


```python
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
        por uma lista de dois pontos: [ponto_inicial, ponto_final]. Uma semirreta é um
        segmento de reta que se estende indefinidamente a partir de seu ponto inicial.
        O padrão é uma lista de quatro semirretas pré-definidas: vertical, horizontal e
        duas diagonais.
    colors : list, opcional
        Uma lista de cores a serem usadas para desenhar as semirretas. A lista deve ter
        o mesmo número de elementos que a lista de semirretas. As cores podem ser 
        especificadas como tuplas de valores RGB de 0 a 255. Se nenhuma cor for 
        especificada, a imagem será desenhada em branco.

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
    
    if isinstance(resolution, int):
        width = height = resolution
    else:
        width, height = resolution
    img = np.zeros((height, width, 3), dtype=np.uint8)
    if semirretas is None:
        semirretas = [
            [(0, -1), (0, 1)],         # Semirreta vertical
            [(-1, 0), (1, 0)],         # Semirreta horizontal
            [(-1, -1), (1, 1)],        # Semirreta inclinada na direção positiva
            [(1, -1), (-1, 1)],        # Semirreta inclinada na direção oposta
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
```

A função rasterize_half_lines é responsável por rasterizar uma lista de semirretas em uma imagem. Ela aceita vários parâmetros opcionais que permitem personalizar a imagem gerada, como resolução, proporção de aspecto, cores e lista de semirretas.

O parâmetro resolution define a resolução da imagem a ser gerada. Se for um número inteiro, é usado como largura e altura da imagem. Se for uma tupla, a largura e a altura são definidas pelos valores da tupla. O parâmetro aspect_ratio define se a proporção de aspecto da imagem deve ser mantida em 16:9. Se True, a altura é calculada automaticamente com base na largura. O parâmetro semirretas é uma lista de semirretas a serem rasterizadas. Cada semirreta é definida por uma lista de dois pontos: [ponto_inicial, ponto_final]. O parâmetro colors é uma lista de cores a serem usadas para desenhar as semirretas.

Se o parâmetro semirretas não for fornecido, a função cria uma lista de quatro semirretas pré-definidas: vertical, horizontal e duas diagonais. Se o parâmetro colors não for fornecido, a função usa uma lista de quatro cores pré-definidas: vermelho, verde, azul e amarelo.

A função itera sobre a lista de semirretas e rasteriza cada semirreta usando a função rasterize_normalized_line, que retorna uma lista de pixels que pertencem à semirreta. Esses pixels são então desenhados na imagem usando a lista de cores fornecida ou a cor padrão, dependendo do número de cores fornecido. Por fim, a função retorna a imagem rasterizada como uma matriz numpy de três dimensões (RGB).

A função é útil para desenhar semirretas em um espaço cartesiano, como em um gráfico, por exemplo. Ao permitir a personalização da imagem gerada, a função pode ser usada em uma variedade de aplicações, desde visualização de dados até jogos e simulações.


```python
triangulo_eq = [
    [(0, 0.618), (0.5, 0.191)],           # primeira semirreta
    [(0.5, 0.191), (0.309, -0.404)],      # segunda semirreta
    [(0.309, -0.404), (-0.309, -0.404)],  # terceira semirreta
    [(-0.309, -0.404), (-0.5, 0.191)],    # quarta semirreta
    [(-0.5, 0.191), (0, 0.618)]           # quinta semirreta
]

colors = [
    (255, 0, 0),    # Vermelho
    (0, 255, 0),    # Verde
    (0, 0, 255),    # Azul
    (255, 255, 0),  # Amarelo
    (255, 0, 255)   # Magenta
]

resolutions = [100, 300, 600, (800, 600), (1920, 1080)]

for resolution in resolutions:
    img = rasterize_half_lines(resolution, aspect_ratio=True, semirretas=triangulo_eq, colors=colors)
    plt.imshow(img)
    plt.gca().invert_yaxis()
    plt.show()
```


    
![png](https://github.com/jbrun0r/cg-rasterized/blob/assets/rasterized/assets/output_7_0.png?raw=true)
    



    
![png](https://github.com/jbrun0r/cg-rasterized/blob/assets/rasterized/assets/output_7_1.png?raw=true)
    



    
![png](https://github.com/jbrun0r/cg-rasterized/blob/assets/rasterized/assets/output_7_2.png?raw=true)
    



    
![png](https://github.com/jbrun0r/cg-rasterized/blob/assets/rasterized/assets/output_7_3.png?raw=true)
    



    
![png](https://github.com/jbrun0r/cg-rasterized/blob/assets/rasterized/assets/output_7_4.png?raw=true)
    



```python
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
```

A função fill_rasterized_polygon preenche um polígono rasterizado com as cores especificadas. O polígono é representado por uma imagem (numpy array) onde as arestas do polígono já estão rasterizadas e os pixels dentro do polígono têm valor diferente de zero.

A função começa encontrando o valor mínimo e máximo de y e x na imagem para determinar a região na qual o polígono se encontra. Em seguida, ela percorre cada linha verticalmente e verifica se a linha contém pelo menos um pixel dentro do polígono. Se sim, a função encontra os pontos de interseção da linha com as arestas do polígono e os ordena em ordem crescente de x. A partir disso, a função preenche o intervalo entre cada par de interseções com a cor especificada.

A função recebe dois argumentos: img e colors. img é a imagem com as arestas do polígono já rasterizadas e colors é uma lista de tuplas de três valores (R, G, B) especificando a cor de preenchimento.

A função retorna a imagem img com o polígono preenchido com as cores especificadas.


```python
def plot_rasterized_polygon(resolutions, aspect_ratio, semirretas, colors):
  
    # Mostra as semirretas no modelo continuo
    fig, ax = plt.subplots()
    # Percorrendo todas as arestas 
    for aresta in semirretas:
            x = [p[0] for p in aresta]
            y = [p[1] for p in aresta]
            ax.plot(x, y)

    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(20,10))
    for resolution in resolutions:

        # Rasteriza as semirretas na resolução escolhida
        img = rasterize_half_lines(resolution, aspect_ratio, semirretas, colors)
        
        # Mostra as semirretas rasterizadas no primeiro subplot
        ax1.imshow(img)
        ax1.set_title(f'Semirretas rasterizadas - Resolução: {resolution[0]} x {resolution[1]}')
        ax1.invert_yaxis()
        ax1.axis('off')
        
        # Preenche o polígono na imagem rasterizada
        img = fill_rasterized_polygon(img, colors)
        
        # Mostra a imagem resultante no segundo subplot
        ax2.imshow(img)
        ax2.set_title(f'Polígono preenchido - Resolução: {resolution[0]} x {resolution[1]}')
        ax2.invert_yaxis()
        ax2.axis('off')
        
        # Mostra ambos os subplots
        plt.show()
```

Essa função cria um gráfico com dois subplots para mostrar a rasterização e o preenchimento de um polígono definido por semirretas em diferentes resoluções.

A função recebe quatro parâmetros:

resolutions: uma lista de tuplas representando as resoluções das imagens rasterizadas a serem criadas.
aspect_ratio: uma tupla representando a relação de aspecto da imagem, ou seja, a razão entre a largura e a altura da imagem.
semirretas: uma lista de listas, cada uma contendo duas tuplas representando as coordenadas do início e do fim de uma semirreta.
colors: uma lista de tuplas de três valores (R, G, B) especificando as cores de preenchimento do polígono.
A função primeiro plota as semirretas no primeiro subplot do gráfico. Para cada resolução especificada, a função rasteriza as semirretas naquela resolução usando a função rasterize_half_lines e mostra a imagem rasterizada no primeiro subplot. Em seguida, a função preenche o polígono rasterizado usando a função fill_rasterized_polygon e mostra a imagem resultante no segundo subplot do gráfico.

Por fim, a função mostra ambos os subplots para cada resolução especificada.


```python
hexagon = [
    [(0.5, 0), (0.25, 0.433)],          # semirreta da aresta superior direita
    [(0.25, 0.433), (-0.25, 0.433)],    # semirreta da aresta superior
    [(-0.25, 0.433), (-0.5, 0)],        # semirreta da aresta superior esquerda
    [(-0.5, 0), (-0.25, -0.433)],       # semirreta da aresta inferior esquerda
    [(-0.25, -0.433), (0.25, -0.433)],  # semirreta da aresta inferior
    [(0.25, -0.433), (0.5, 0)]          # semirreta da aresta inferior direita
]

colors = [
    (131,111,255)
]

resolutions = [(800, 600)]

plot_rasterized_polygon(resolutions, True, hexagon, colors)
```


    
![png](https://github.com/jbrun0r/cg-rasterized/blob/assets/rasterized/assets/output_12_0.png?raw=true)
    



    
![png](https://github.com/jbrun0r/cg-rasterized/blob/assets/rasterized/assets/output_12_1.png?raw=true)
    
