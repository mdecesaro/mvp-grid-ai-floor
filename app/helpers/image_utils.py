# app/helpers/image_utils.py

import io
from PIL import Image, ImageTk, ImageDraw
import customtkinter as ctk


def create_rounded_photo(image_blob, size=(40, 40), border_color="#00FFAA", border_width=2, scale_factor=4):
    """
    Cria uma imagem circular com borda suavizada, usando upscaling + antialiasing.

    Args:
        image_blob (bytes): imagem binária
        size (tuple): tamanho final (ex: (40, 40))
        border_color (str): cor da borda
        border_width (int): largura da borda
        scale_factor (int): fator de escala para suavizar borda

    Returns:
        ImageTk.PhotoImage: imagem Tkinter com borda circular lisa
    """
    # Escalar tudo para cima
    w, h = size[0] * scale_factor, size[1] * scale_factor
    bw = border_width * scale_factor

    # Redimensionar imagem
    image_stream = io.BytesIO(image_blob)
    img = Image.open(image_stream).convert("RGBA").resize((w - 2*bw, h - 2*bw), Image.LANCZOS)

    # Base com fundo transparente
    final_img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(final_img)

    # Desenhar borda suavizada
    draw.ellipse((0, 0, w-1, h-1), fill=border_color)

    # Máscara circular para a imagem central
    mask = Image.new("L", img.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, img.size[0]-1, img.size[1]-1), fill=255)

    # Colar imagem com máscara
    final_img.paste(img, (bw, bw), mask)

    # Reduzir para tamanho final com antialiasing
    final_img = final_img.resize(size, Image.LANCZOS)

    return ImageTk.PhotoImage(final_img)

def create_rounded_rect_photo(image_blob, size=(80, 60), corner_radius=10, border_color="#00FFAA", border_width=2, scale_factor=4):
    """
    Cria uma imagem com cantos arredondados e borda suavizada.

    Args:
        image_blob (bytes): imagem binária
        size (tuple): tamanho final (ex: (80, 60))
        corner_radius (int): raio dos cantos arredondados
        border_color (str): cor da borda
        border_width (int): largura da borda
        scale_factor (int): fator de upscaling para suavização

    Returns:
        ImageTk.PhotoImage: imagem Tkinter com cantos arredondados e borda lisa
    """
    w, h = size[0] * scale_factor, size[1] * scale_factor
    bw = border_width * scale_factor
    cr = corner_radius * scale_factor

    # Redimensionar imagem original
    image_stream = io.BytesIO(image_blob)
    img = Image.open(image_stream).convert("RGBA").resize((w - 2*bw, h - 2*bw), Image.LANCZOS)

    # Criar imagem base com fundo transparente
    final_img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(final_img)

    # Desenhar retângulo com cantos arredondados (borda)
    draw.rounded_rectangle((0, 0, w, h), radius=cr, fill=border_color)

    # Criar máscara com cantos arredondados para imagem interna
    mask = Image.new("L", img.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle((0, 0, img.size[0], img.size[1]), radius=cr - bw, fill=255)

    # Colar imagem redimensionada com máscara
    final_img.paste(img, (bw, bw), mask)

    # Reduzir de volta ao tamanho final com antialiasing
    final_img = final_img.resize(size, Image.LANCZOS)

    return ImageTk.PhotoImage(final_img)


def open_icon_png(icon_path, size=(24, 24)):
    """
    Carrega um arquivo PNG como CTkImage para usar nos widgets CustomTkinter.

    Args:
        icon_path (str): Caminho do arquivo PNG.
        size (tuple): Tamanho desejado (width, height), padrão (24, 24).

    Returns:
        CTkImage: Imagem pronta para usar no CustomTkinter.
    """
    try:
        img = Image.open(icon_path)
        img = img.resize(size, Image.LANCZOS)
        return ctk.CTkImage(light_image=img, size=size)
    except Exception as e:
        print(f"Erro ao abrir a imagem {icon_path}: {e}")
        return None