from queue import Queue
import pygame
import threading
import time 
import globals
from inicio import save_score, inicio
from jugador import Jugador
from hilos import GeneradorFormas, MovimientoFormas
from forma import dibujar_forma
from menu import mostrar_portada, mostrar_menu, mostrar_seleccion_personaje, mostrar_pantalla_fin
from utils import  imagen_fondo
from globals import ANCHO, ALTO, NEGRO, reloj, pantalla, velocidad_jugador, cola_formas, lock_formas

pygame.init()

pygame.mixer.init()
pygame.mixer.music.load("musica_fondo.mp3") 

def inicializar_juego():
    """Función principal para ejecutar el flujo del juego."""
    global tiempo_inicial, ejecutando, stop_event, lock_formas, cola_formas, reloj

    # Reiniciar el estado del juego
    globals.puntaje = 0
    globals.vidas = 3
    tiempo_inicial = time.time()
    ejecutando = True
    cola_formas = Queue()
    stop_event = threading.Event()

def iniciar_hilos():
    """Inicia los hilos para generar y mover formas."""
    generador_formas = GeneradorFormas(cola_formas, lock_formas, tiempo_inicial, stop_event, formas_buenas_seleccionadas, formas_malas_seleccionadas)
    movimiento_formas = MovimientoFormas(cola_formas, lock_formas, jugador, reloj, tiempo_inicial, stop_event)

    hilo_generador = threading.Thread(target=generador_formas.generar_formas)
    hilo_movedor = threading.Thread(target=movimiento_formas.mover_formas)
    hilo_generador.start()
    hilo_movedor.start()

    return hilo_generador, hilo_movedor


def manejar_eventos():
    """Maneja los eventos del juego."""
    global ejecutando
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
            stop_event.set()
            return "salir"
    return None


def manejar_movimiento_jugador():
    """Maneja el movimiento del jugador"""
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and jugador.x - velocidad_jugador >= 0:
        jugador.x -= velocidad_jugador
        jugador.direccion_jugador = 'izquierda'
    elif teclas[pygame.K_RIGHT] and jugador.x + velocidad_jugador <= ANCHO - jugador.ancho_jugador:
        jugador.x += velocidad_jugador
        jugador.direccion_jugador = 'derecha'


def dibujar_jugador():
    """Dibuja al jugador en pantalla según su dirección."""
    if jugador.direccion_jugador == 'derecha':
        pantalla.blit(jugador.imagen_derecha, (jugador.x, jugador.y))
    else:
        pantalla.blit(jugador.imagen_izquierda, (jugador.x, jugador.y))


def dibujar_formas_en_pantalla():
    """Dibuja las formas presentes en la cola compartida."""
    with lock_formas:
        formas_a_dibujar = list(cola_formas.queue)
    for forma in formas_a_dibujar:
        dibujar_forma(forma)


def mostrar_hud():
    """Dibuja el puntaje y las vidas en la pantalla."""
    fuente = pygame.font.SysFont(None, 36)
    texto_puntaje = fuente.render(f"Puntaje: {globals.puntaje}", True, NEGRO)
    texto_vidas = fuente.render(f"Vidas: {globals.vidas}", True, NEGRO)
    pantalla.blit(texto_puntaje, (10, 10))
    pantalla.blit(texto_vidas, (10, 50))


def verificar_fin_del_juego():
    """Verifica si el jugador ha perdido todas las vidas y muestra el mensaje final."""
    global ejecutando
    if globals.vidas <= 0:
        fuente_game_over = pygame.font.SysFont(None, 72)
        texto_game_over = fuente_game_over.render("¡Juego Terminado!", True, NEGRO)
        pantalla.blit(texto_game_over, (ANCHO // 2 - texto_game_over.get_width() // 2, ALTO // 2))
        pygame.display.flip()
        time.sleep(0.8)
        ejecutando = False
        stop_event.set()


def esperar_hilos(hilo_generador, hilo_movedor):
    """Espera a que los hilos terminen antes de continuar."""
    hilo_generador.join()
    hilo_movedor.join()

    save_score(nombre_jugador, globals.puntaje)
    


def ejecutar_juego(nombre_jugador):
    """Función principal para ejecutar el flujo del juego."""
    inicializar_juego()
    hilo_generador, hilo_movedor = iniciar_hilos()
    
    while ejecutando:
        reloj.tick(60)  # Controlamos el juego a 60 FPS
        pantalla.blit(imagen_fondo, (0, 0))  # Dibujamos la imagen de fondo

        # Manejo de eventos y movimiento del jugador
        accion = manejar_eventos()
        if accion == "salir":
            break

        manejar_movimiento_jugador()
        dibujar_jugador()

        # Dibujar formas y mostrar el HUD
        dibujar_formas_en_pantalla()
        mostrar_hud()

        # Verificar si el juego terminó
        verificar_fin_del_juego()

        # Actualizar la pantalla
        pygame.display.flip()
    
    esperar_hilos(hilo_generador, hilo_movedor)
    
    return mostrar_pantalla_fin()

# Inicia el flujo principal del juego
if __name__ == "__main__":
    mostrar_portada()
    nombre_jugador = inicio()
    
    while True:
        # Seleccionar el personaje del jugador
        personaje_seleccionado = mostrar_seleccion_personaje()

        # Crear la instancia del jugador con el personaje seleccionado
        jugador = Jugador(personaje_seleccionado)

        # Mostramos el menú y obtenemos las selecciones del jugador
        formas_buenas_seleccionadas, formas_malas_seleccionadas = mostrar_menu()

        # Ejecutamos el juego y obtenemos la acción seleccionada al final
        accion = ejecutar_juego(nombre_jugador)

        # Verificamos la acción después de que termina el juego
        if accion == "salir":
            break  # Salimos del bucle principal y cerramos el juego

    pygame.quit()
