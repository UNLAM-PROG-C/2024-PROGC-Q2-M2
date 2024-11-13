import pygame
import time
import threading
from queue import Queue

VEL_CAIDA_LIMITE_INFERIOR = 3
VEL_CAIDA_LIMITE_SUPERIOR = 7
TAM_FORMA_LIMITE_INFERIOR = 40
TAM_FORMA_LIMITE_SUPERIOR = 80
TIPO_FORMA_MALA = "mala"
TIPO_FORMA_BUENA = "buena"
PUNTAJE_INICIAL = 0
CANTIDAD_VIDAS = 3
CANTIDAD_VIDAS_PERDER = 0
SALIR_JUEGO = "salir"
ATRAS_JUEGO = "atras"
TAM_PERSONAJE_LIMITE_INFERIOR = 100
TAM_PERSONAJE_LIMITE_SUPERIOR = 150
CANTIDAD_FLUCTUACION_VIDAS = 1
FOTOGRAMAS_MENU = 30
FOTOGRAMAS_FORMAS = 50
FOTOGRAMAS_JUEGO = 60
DIR_PERSONAJE_DERECHA = "derecha"
DIR_PERSONAJE_IZQUIERDA = "izquierda"
COMPONENTE_ROJO_GRIS = 0.29
COMPONENTE_VERDE_GRIS = 0.59
COMPONENTE_AZUL_GRIS = 0.11

puntaje = 0        # Puntuación del jugador
vidas = 3          # Número de vidas del jugador
# Definimos las dimensiones de la pantalla del juego
ANCHO, ALTO = 800, 600  # Ajusta el tamaño de la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))  # Creamos la pantalla del juego
pygame.display.set_caption("Atrapa las Comidas")  # Título de la ventana

# Definimos colores usando formato RGB
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (16, 0, 37)
CELESTE = (162, 255, 244)
BLUE = (105, 34, 226) 
VERDE = (195, 252, 206)

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

thickness = 2

musica_activa = 1

musica = 0