
import os
from datetime import datetime
import pygame
import sys
from globals import ANCHO, ALTO, GRIS, CELESTE, pantalla, thickness
from utils import imagen_inicio, draw_text

pygame.init()

font_path = 'fonts/dogicapixelbold.ttf' 
size = 25
font = pygame.font.Font(font_path, size)
all_fonts = pygame.font.get_fonts() 
small_font = pygame.font.Font(font_path, 20)

input_active = False
user_text = ""


def save_score(username, score):
    """Guarda el nombre de usuario y el puntaje en un archivo de texto."""
    filename = "historial_record.txt"
    file_exists = os.path.isfile(filename)
    
    with open(filename, "a") as file:
        if not file_exists:
            file.write(f"{'Nombre de Usuario':<20} | {'Puntaje':<7} | {'Fecha':<19}\n")
            file.write("=" * 49 + "\n")
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{username:<20} | {score:<7} | {current_time:<19}\n")
    print("Puntaje guardado con éxito.")

def inicio():
    """Pantalla de inicio donde el usuario ingresa su nombre."""
    global input_active, user_text
    clock = pygame.time.Clock()
    running = True

    while running:
        pantalla.blit(imagen_inicio, (0, 0))
        draw_text("Ingrese su nombre:", font, GRIS, pantalla, ANCHO // 2, ALTO // 2 - 50)
        input_box = pygame.Rect(ANCHO // 2 - 100, ALTO // 2, 200, 50)
        pygame.draw.rect(pantalla, GRIS, input_box)
        pygame.draw.rect(pantalla, CELESTE, input_box, 4)

        text_surface = small_font.render(user_text, True, CELESTE)
        pantalla.blit(text_surface, (input_box.x + 5, input_box.y + 10))
        input_box.w = max(200, text_surface.get_width() + 10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False
            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        if user_text:
                            running = False
                    elif event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode

        pygame.display.flip()
        clock.tick(30)
    return user_text