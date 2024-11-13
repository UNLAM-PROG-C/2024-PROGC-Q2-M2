import pygame
import threading    
import time
from queue import Queue
from globals import ALTO, ANCHO, CELESTE, COMPONENTE_AZUL_GRIS, COMPONENTE_ROJO_GRIS, COMPONENTE_VERDE_GRIS, TAM_PERSONAJE_LIMITE_INFERIOR, TAM_PERSONAJE_LIMITE_SUPERIOR, TIPO_FORMA_BUENA, TIPO_FORMA_MALA, thickness

# Función para cargar imágenes con manejo de errores
def cargar_imagen(ruta, escala=None, tipo_forma=None):
    try:
        imagen = pygame.image.load(ruta).convert_alpha()
        if tipo_forma == TIPO_FORMA_MALA:
            filtro_blanco_negro(imagen)
        if escala:
            imagen = pygame.transform.scale(imagen, escala)
        return imagen
    except pygame.error as e:
        print(f"Error al cargar la imagen '{ruta}': {e}")
        pygame.quit()
        exit()

def filtro_blanco_negro(imagen):
    ancho, alto = imagen.get_size()
    for x in range(ancho):
        for y in range(alto):
            color = imagen.get_at((x, y))
            gris = int(COMPONENTE_ROJO_GRIS * color.r + COMPONENTE_VERDE_GRIS * color.g + COMPONENTE_AZUL_GRIS * color.b)
            imagen.set_at((x, y), (gris, gris, gris, color.a))  # Mantener la transparencia

def draw_text(text, font, color, surface, x, y):
    """Función para dibujar texto en la pantalla con borde más grueso.""" 
    outline_color = CELESTE 
    for dx in range(-thickness, thickness + 1): 
        for dy in range(-thickness, thickness + 1): 
            if dx != 0 or dy != 0:
                text_obj = font.render(text, True, outline_color) 
                text_rect = text_obj.get_rect(center=(x + dx, y + dy)) 
                surface.blit(text_obj, text_rect)
    
    text_obj = font.render(text, True, color) 
    text_rect = text_obj.get_rect(center=(x, y)) 
    surface.blit(text_obj, text_rect)



# Cargar imágenes de las formas buenas y malas
imagenes_formas_buenas = {
    'Hamburguesa': cargar_imagen('img/comida_rapida_snacks/15_burger.png', tipo_forma= TIPO_FORMA_BUENA),
    'Papas Fritas': cargar_imagen('img/comida_rapida_snacks/44_frenchfries.png', tipo_forma= TIPO_FORMA_BUENA),
    'Pancho': cargar_imagen('img/comida_rapida_snacks/54_hotdog.png', tipo_forma= TIPO_FORMA_BUENA),
    'Nacho': cargar_imagen('img/comida_rapida_snacks/71_nacho.png', tipo_forma= TIPO_FORMA_BUENA),
    'Pizza': cargar_imagen('img/comida_rapida_snacks/81_pizza.png', tipo_forma= TIPO_FORMA_BUENA),
    'Pochoclos': cargar_imagen('img/comida_rapida_snacks/83_popcorn.png', tipo_forma= TIPO_FORMA_BUENA),
    'Sanguche': cargar_imagen('img/comida_rapida_snacks/92_sandwich.png', tipo_forma= TIPO_FORMA_BUENA),
    'Chocolate': cargar_imagen('img/dulces_postres/26_chocolate.png', tipo_forma= TIPO_FORMA_BUENA),
    'Torta': cargar_imagen('img/dulces_postres/30_chocolatecake.png', tipo_forma= TIPO_FORMA_BUENA)
}

imagenes_formas_malas = {
    'Hamburguesa': cargar_imagen('img/comida_rapida_snacks/15_burger.png', tipo_forma= TIPO_FORMA_MALA),
    'Papas Fritas': cargar_imagen('img/comida_rapida_snacks/44_frenchfries.png', tipo_forma= TIPO_FORMA_MALA),
    'Pancho': cargar_imagen('img/comida_rapida_snacks/54_hotdog.png', tipo_forma= TIPO_FORMA_MALA),
    'Nacho': cargar_imagen('img/comida_rapida_snacks/71_nacho.png', tipo_forma= TIPO_FORMA_MALA),
    'Pizza': cargar_imagen('img/comida_rapida_snacks/81_pizza.png', tipo_forma= TIPO_FORMA_MALA),
    'Pochoclos': cargar_imagen('img/comida_rapida_snacks/83_popcorn.png', tipo_forma=TIPO_FORMA_MALA),
    'Sanguche': cargar_imagen('img/comida_rapida_snacks/92_sandwich.png', tipo_forma= TIPO_FORMA_MALA),
    'Chocolate': cargar_imagen('img/dulces_postres/26_chocolate.png', tipo_forma=TIPO_FORMA_MALA),
    'Torta': cargar_imagen('img/dulces_postres/30_chocolatecake.png', tipo_forma=TIPO_FORMA_MALA)
}

# Cargar imágenes de personajes disponibles
imagenes_personajes = {
    'Katy Perry': {
        'derecha': cargar_imagen('img/nenita1_der.png', (TAM_PERSONAJE_LIMITE_INFERIOR, TAM_PERSONAJE_LIMITE_SUPERIOR)),
        'izquierda': cargar_imagen('img/nenita1_iz.png', (TAM_PERSONAJE_LIMITE_INFERIOR, TAM_PERSONAJE_LIMITE_SUPERIOR))
    },
    'Emi Mernes': {
        'derecha': cargar_imagen('img/aros-der.png', (TAM_PERSONAJE_LIMITE_INFERIOR, TAM_PERSONAJE_LIMITE_SUPERIOR)),
        'izquierda': cargar_imagen('img/aros-iz.png', (TAM_PERSONAJE_LIMITE_INFERIOR, TAM_PERSONAJE_LIMITE_SUPERIOR))
    },
    'Nene Malo': {
        'derecha': cargar_imagen('img/nene1-der.png', (TAM_PERSONAJE_LIMITE_INFERIOR, TAM_PERSONAJE_LIMITE_SUPERIOR)),
        'izquierda': cargar_imagen('img/nene1-iz.png', (TAM_PERSONAJE_LIMITE_INFERIOR, TAM_PERSONAJE_LIMITE_SUPERIOR))
    },
    'Bizza': {
        'derecha': cargar_imagen('img/will-der.png', (TAM_PERSONAJE_LIMITE_INFERIOR, TAM_PERSONAJE_LIMITE_SUPERIOR)),
        'izquierda': cargar_imagen('img/will-iz.png', (TAM_PERSONAJE_LIMITE_INFERIOR, TAM_PERSONAJE_LIMITE_SUPERIOR))
    },
}

# Cargar imagen de fondo
imagen_fondo = cargar_imagen('img/day2.png', (ANCHO, ALTO))

imagen_portada = cargar_imagen('img/portada.png', (ANCHO, ALTO))

imagen_inicio = cargar_imagen('img/inicio.png', (ANCHO, ALTO))