import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pantalla de Inicio")


WHITE = (255, 255, 255)
BLACK = (16, 0, 37)
BLUE = (105, 34, 226) 
GRIS = (46,46,66)
CELESTE = (162, 255, 244)

font_path = 'fonts/dogicapixelbold.ttf' 
size = 25
font = pygame.font.Font(font_path, size)
all_fonts = pygame.font.get_fonts() 
small_font = pygame.font.Font(font_path, 20)

input_active = False
user_text = ""

background_image = pygame.image.load("img/inicio.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

def draw_text(text, font, color, surface, x, y):
    """Función para dibujar texto en la pantalla con borde más grueso.""" 
    outline_color = CELESTE 
    thickness = 2
    for dx in range(-thickness, thickness + 1): 
        for dy in range(-thickness, thickness + 1): 
            if dx != 0 or dy != 0:
                text_obj = font.render(text, True, outline_color) 
                text_rect = text_obj.get_rect(center=(x + dx, y + dy)) 
                surface.blit(text_obj, text_rect)
    # Dibujar el texto principal 
    text_obj = font.render(text, True, color) 
    text_rect = text_obj.get_rect(center=(x, y)) 
    surface.blit(text_obj, text_rect)

def save_score(username, score):
    """Guarda el nombre de usuario y el puntaje en un archivo de texto."""
    with open("historial_record.txt", "a") as file:
        file.write(f"{username}: {score}\n")

def inicio():
    """Pantalla de inicio donde el usuario ingresa su nombre."""
    global input_active, user_text
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.blit(background_image, (0, 0))
        draw_text("Ingrese su nombre:", font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
        pygame.draw.rect(screen, BLACK, input_box)
        pygame.draw.rect(screen, CELESTE, input_box, 4)

        text_surface = small_font.render(user_text, True, CELESTE)
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 10))
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
                            save_score(user_text, 0) 
                            running = False
                    elif event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode

        pygame.display.flip()
        clock.tick(30)

