import pygame
import time
import threading
from queue import Queue

puntaje = 0        # Puntuación del jugador
vidas = 3          # Número de vidas del jugador
# Definimos las dimensiones de la pantalla del juego
ANCHO, ALTO = 800, 600  # Ajusta el tamaño de la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))  # Creamos la pantalla del juego
pygame.display.set_caption("Atrapa las Comidas")  # Título de la ventana

# Definimos colores usando formato RGB
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
CELESTE = (162, 255, 244)

# Velocidad de movimiento del jugador
velocidad_jugador = 10

reloj = pygame.time.Clock()  # Reloj para controlar los FPS del juego

# Variables del estado del juego
ejecutando = True  # Controla si el juego sigue ejecutándose

tiempo_inicial = time.time()  # Tiempo en el que inicia el juego

# Cola y lock (bloqueo) para manejar la comunicación entre hilos
cola_formas = Queue()           # Cola para las formas
lock_formas = threading.Lock()  # Lock para evitar problemas de acceso concurrente a la cola

# Listas para almacenar las selecciones de formas buenas y malas del jugador
formas_buenas_seleccionadas = []
formas_malas_seleccionadas = []

font_path = 'fonts/dogicapixelbold.ttf' 
size = 25
font = pygame.font.Font(font_path, size)
all_fonts = pygame.font.get_fonts() 
small_font = pygame.font.Font(font_path, 20)