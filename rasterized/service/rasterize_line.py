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
