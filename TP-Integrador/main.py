import pygame
import os
import random

# Inicializa Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Turnos")

# Variables globales
NUM_PLAYERS = 16
GRID_SIZE = 4
CELL_SIZE = WIDTH // GRID_SIZE
MARGIN = 20  # Margen alrededor de cada imagen
selection_time = 30  # Tiempo que durará el proceso de selección aleatoria (en segundos)

# Cargar imagen de jugador
original_image = pygame.image.load('player.png')  # Asegúrate de tener esta imagen en el mismo directorio
original_image = pygame.transform.scale(original_image, (CELL_SIZE - MARGIN * 2, CELL_SIZE - MARGIN * 2))

# Función para recortar la imagen
def crop_image_to_fit(image, target_width, target_height):
    image_width, image_height = image.get_size()

    # Calcular la relación de aspecto de la imagen y de la ventana
    image_aspect_ratio = image_width / image_height
    target_aspect_ratio = target_width / target_height

    if image_aspect_ratio > target_aspect_ratio:
        # La imagen es más ancha, recortar los lados
        new_width = int(image_height * target_aspect_ratio)
        offset = (image_width - new_width) // 2
        cropped_image = image.subsurface((offset, 0, new_width, image_height))
    else:
        # La imagen es más alta, recortar la parte superior e inferior
        new_height = int(image_width / target_aspect_ratio)
        offset = (image_height - new_height) // 2
        cropped_image = image.subsurface((0, offset, image_width, new_height))

    return pygame.transform.scale(cropped_image, (target_width, target_height))

# Cargar y recortar la imagen de fondo para la pantalla de inicio
home_background = pygame.image.load('home.jpg')  # Asegúrate de tener esta imagen en el mismo directorio
home_background = crop_image_to_fit(home_background, WIDTH, HEIGHT)  # Recortar y ajustar la imagen al tamaño de la ventana

# Clase para cada jugador
class Player:
    def __init__(self, player_id):
        self.id = player_id
        self.image = original_image
        self.category = f"Categoría {player_id + 1}"  # Ejemplo de categoría

# Crear jugadores
players = [Player(i) for i in range(NUM_PLAYERS)]
turn = -10  # Controla el turno actual

# Función para mostrar la pantalla de inicio
def show_home_screen():
    screen.blit(home_background, (0, 0))  # Dibujar la imagen de fondo
    pygame.display.flip()

# Función para mostrar jugadores de forma aleatoria antes de la selección definitiva
def random_selection():
    global turn
    for _ in range(selection_time):  # Itera varias veces para simular la elección aleatoria
        turn = random.randint(0, NUM_PLAYERS - 1)  # Selección aleatoria temporal
        draw_board()
        pygame.display.flip()
        pygame.time.delay(200)  # Pequeña pausa para mostrar el cambio rápido

    # Selección definitiva
    turn = random.randint(0, NUM_PLAYERS - 1)

# Función para dibujar el tablero
def draw_board():
    screen.fill((255, 255, 255))  # Limpiar pantalla

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x = i * CELL_SIZE
            y = j * CELL_SIZE

            player_index = i * GRID_SIZE + j

            # Cambiar el color de fondo según el turno
            if player_index == turn:
                background_color =  (255, 255, 128) # Amarillo para el jugador aleatorio
            else:
                background_color = (200, 200, 200)  # Color gris por defecto

            pygame.draw.rect(screen, background_color, (x, y, CELL_SIZE, CELL_SIZE))  # Cuadro de fondo

            # Dibujar la imagen del jugador
            image_rect = players[player_index].image.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
            screen.blit(players[player_index].image, image_rect)

            # Mostrar la categoría del jugador debajo de la imagen
            font = pygame.font.Font(None, 24)  # Fuente por defecto
            category_text = font.render(players[player_index].category, True, (0, 0, 0))
            screen.blit(category_text, (x + CELL_SIZE // 2 - category_text.get_width() // 2, 
                                        y + CELL_SIZE - MARGIN))

# Función para dibujar el tablero definitivo
def draw_board_definitive():
    screen.fill((255, 255, 255))  # Limpiar pantalla

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x = i * CELL_SIZE
            y = j * CELL_SIZE

            player_index = i * GRID_SIZE + j

            # Cambiar el color de fondo según el turno
            if player_index == turn:
                background_color =  (128, 255, 128) # Verde para el jugador en turno
            elif (player_index == turn - 1 and turn % GRID_SIZE > 0) or (player_index == turn + 1 and turn % GRID_SIZE < GRID_SIZE - 1) or \
                 (player_index == turn - GRID_SIZE and turn >= GRID_SIZE) or (player_index == turn + GRID_SIZE and turn < NUM_PLAYERS - GRID_SIZE):
                    background_color = (128, 255, 255)  # Azul para los jugadores adyacentes
            else:
                background_color = (200, 200, 200)  # Color gris por defecto

            pygame.draw.rect(screen, background_color, (x, y, CELL_SIZE, CELL_SIZE))  # Cuadro de fondo

            # Dibujar la imagen del jugador
            image_rect = players[player_index].image.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
            screen.blit(players[player_index].image, image_rect)

            # Mostrar la categoría del jugador debajo de la imagen
            font = pygame.font.Font(None, 24)  # Fuente por defecto
            category_text = font.render(players[player_index].category, True, (0, 0, 0))
            screen.blit(category_text, (x + CELL_SIZE // 2 - category_text.get_width() // 2, 
                                        y + CELL_SIZE - MARGIN))

# Bucle principal del juego
running = True
show_home = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and show_home:  # Al presionar espacio, pasar de la pantalla de inicio
                show_home = False
                random_selection()  # Iniciar selección aleatoria inmediatamente

    if show_home:
        show_home_screen()  # Mostrar pantalla de inicio
    else:
        draw_board_definitive()  # Mostrar el tablero definitivo

    # Actualizar pantalla
    pygame.display.flip()

# Cerrar Pygame
pygame.quit()
