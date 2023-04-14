from service.rasterize_line import rasterize_line

def rasterize_normalized_line(x0, y0, x1, y1, width, height, aspect_ratio):
    """Rasteriza uma reta definida pelos pontos (x0, y0) e (x1, y1) em uma imagem com a resolução dada por (width, height).
    
    A imagem pode ter um aspect ratio diferente de 1:1, caso em que a reta será proporcional a resolução.
    Caso o aspect ratio seja desejado, a menor dimensão entre width e height é encontrada, e a reta é rasterizada
    levando em consideração a menor dimensão para manter o aspect ratio correto.

    Args:
        x0 (float): Coordenada x do ponto inicial da reta, normalizada entre -1 e 1.
        y0 (float): Coordenada y do ponto inicial da reta, normalizada entre -1 e 1.
        x1 (float): Coordenada x do ponto final da reta, normalizada entre -1 e 1.
        y1 (float): Coordenada y do ponto final da reta, normalizada entre -1 e 1.
        width (int): Largura da imagem em pixels.
        height (int): Altura da imagem em pixels.
        aspect_ratio (bool): Se True, mantém o aspect ratio da imagem.

    Returns:
        numpy.ndarray: Array numpy representando os pixels da reta rasterizada.

    Raises:
        TypeError: Se os argumentos não forem do tipo correto.
        ValueError: Se o aspect ratio não for um booleano.

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
