import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox
import  tkinter as tk

from service.plot_rasterized_polygon import plot_rasterized_polygon

window = Tk()
window.title("Rasterizar Polígonos")
window.geometry("862x519")
window.resizable(False,False)
window.configure(bg="#3A7FF6")

canvas = tk.Canvas(
    window, bg="#243e76", height=519, width=862,
    bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)
canvas.create_rectangle(431, 0, 431 + 431, 0 + 519, fill="#FCFCFC", outline="")

# Half Lines
canvas.create_text(
    490.0, 156.0, text="Lista de semirretas", fill="#515486",
    font=("Arial-BoldMT", int(13.0)), anchor="w")
half_lines_entry = tk.Entry(bd=0, bg="#F6F7F9",fg="#000716",  highlightthickness=0)
half_lines_entry.place(x=490.0, y=137+25, width=321.0, height=35)
half_lines_string = "0 0.866 0.5 0, 0.5 0 -0.5 0, -0.5 0 0 0.866"
half_lines_entry.insert(0,half_lines_string)


# Resolution
canvas.create_text(
    490.0, 234.5, text="Resolução", fill="#515486",
    font=("Arial-BoldMT", int(13.0)), anchor="w")
resolution_entry = tk.Entry(bd=0, bg="#F6F7F9", fg="#000716",  highlightthickness=0)
resolution_entry.place(x=490.0, y=218+25, width=321.0, height=35)
resolution_entry.insert(0, "1280x720")

# Color
canvas.create_text(
    490.0, 315.5, text="Cor(R,G,B)",
    fill="#515486", font=("Arial-BoldMT", int(13.0)), anchor="w")
color_entry = tk.Entry(bd=0, bg="#F6F7F9", fg="#000716", highlightthickness=0)
color_entry.place(x=490.0, y=299+25, width=321.0, height=35)
color_entry.insert(0, "255,255,255")

canvas.create_text(
    646.5, 428.5, text="Generate",
    fill="#FFFFFF", font=("Arial-BoldMT", int(13.0)))
canvas.create_text(
    540.0, 88.0, text="Polígono:",
    fill="#515486", font=("Arial-BoldMT", int(22.0)))

title = tk.Label(
    text="Rasterização de Polígonos", bg="#243e76",
    fg="white",justify="left", font=("Arial-BoldMT", int(20.0)))
title.place(x=20.0, y=120.0)
canvas.create_rectangle(25, 160, 33 + 60, 160 + 5, fill="#FCFCFC", outline="")

info_text = tk.Label(
    text="Para rasterizar polígonos basta\n"
    "inserir a lista de semirretas,\n"
    "a resolução e a cor do polígono.\n"
    "\n\n\n\n"
    ,
    bg="#243e76", fg="white", justify="left",
    font=("Georgia", int(16.0)))
info_text.place(x=20.0, y=200.0)

footer_text = tk.Label(
    text="Created using Tkinter,\n"
    "Numpy and Matplotlib.",
    bg="#243e76", fg="#f6e05e", justify="left",
    font=("Georgia", int(12.0)))

footer_text.place(x=20.0, y=412.0)


def plot():
    half_lines = half_lines_entry.get()
    half_lines = half_lines.split(", ")
    half_lines = [s.split() for s in half_lines]
    half_lines = [[(float(s[i]), float(s[i+1])) for i in range(0, len(s), 2)] for s in half_lines]
    
    resolution = resolution_entry.get()
    w, h = map(int, resolution.split("x"))
    resolution = [(w, h)]

    color = color_entry.get()
    color = list(map(int, color.split(",")))
    color = [tuple(color)]
    
    return plot_rasterized_polygon(resolution, True, half_lines, color)

rasterize_btn_img = PhotoImage(file="button.png")
rasterize_btn = tk.Button(
    image=rasterize_btn_img, borderwidth=0, highlightthickness=0,
    command=plot, relief="flat", cursor="hand2")
rasterize_btn.place(x=490, y=401, width=321, height=55)

window.mainloop()

quadrado = [
    [(0.5, -0.5), (0.5, 0.5)],   # Aresta da direita
    [(0.5, 0.5), (-0.5, 0.5)],   # Aresta superior
    [(-0.5, 0.5), (-0.5, -0.5)], # Aresta da esquerda
    [(-0.5, -0.5), (0.5, -0.5)]  # Aresta inferior
]

hexagon = [
    [(0.5, 0), (0.25, 0.433)],   # semirreta da aresta superior direita
    [(0.25, 0.433), (-0.25, 0.433)],  # semirreta da aresta superior
    [(-0.25, 0.433), (-0.5, 0)],   # semirreta da aresta superior esquerda
    [(-0.5, 0), (-0.25, -0.433)],   # semirreta da aresta inferior esquerda
    [(-0.25, -0.433), (0.25, -0.433)],  # semirreta da aresta inferior
    [(0.25, -0.433), (0.5, 0)]   # semirreta da aresta inferior direita
]
