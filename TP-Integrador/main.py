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
from globals import ANCHO, ALTO, BLANCO, CANTIDAD_VIDAS, CANTIDAD_VIDAS_PERDER, DIR_PERSONAJE_DERECHA, DIR_PERSONAJE_IZQUIERDA, FOTOGRAMAS_JUEGO, NEGRO, PUNTAJE_INICIAL, SALIR_JUEGO, reloj, pantalla, velocidad_jugador, cola_formas, lock_formas

pygame.init()

pygame.mixer.init()
pygame.mixer.music.load("assets/Musica_de_fondo.mp3") 
pygame.mixer.music.set_volume(0.03)

def inicializar_juego():
    """Función principal para ejecutar el flujo del juego."""
    global tiempo_inicial, ejecutando, stop_event, lock_formas, cola_formas, reloj
    globals.puntaje = PUNTAJE_INICIAL
    globals.vidas = CANTIDAD_VIDAS
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
            return SALIR_JUEGO
    return None


def manejar_movimiento_jugador():
    """Maneja el movimiento del jugador"""
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and jugador.x - velocidad_jugador >= 0:
        jugador.x -= velocidad_jugador
        jugador.direccion_jugador = DIR_PERSONAJE_IZQUIERDA
    elif teclas[pygame.K_RIGHT] and jugador.x + velocidad_jugador <= ANCHO - jugador.ancho_jugador:
        jugador.x += velocidad_jugador
        jugador.direccion_jugador = DIR_PERSONAJE_DERECHA


def dibujar_jugador():
    """Dibuja al jugador en pantalla según su dirección."""
    if jugador.direccion_jugador == DIR_PERSONAJE_DERECHA:
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
    texto_puntaje = fuente.render(f"Puntaje: {globals.puntaje}", True, BLANCO)
    texto_vidas = fuente.render(f"Vidas: {globals.vidas}", True, BLANCO)
    pantalla.blit(texto_puntaje, (10, 10))
    pantalla.blit(texto_vidas, (10, 50))


def verificar_fin_del_juego():
    """Verifica si el jugador ha perdido todas las vidas y muestra el mensaje final."""
    global ejecutando
    if globals.vidas <= CANTIDAD_VIDAS_PERDER:
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
        reloj.tick(FOTOGRAMAS_JUEGO) 
        pantalla.blit(imagen_fondo, (0, 0))
        accion = manejar_eventos()
        if accion == SALIR_JUEGO:
            break

        manejar_movimiento_jugador()
        dibujar_jugador()
        dibujar_formas_en_pantalla()
        mostrar_hud()
        verificar_fin_del_juego()
        pygame.display.flip()
    
    esperar_hilos(hilo_generador, hilo_movedor)
    
    return mostrar_pantalla_fin()

if __name__ == "__main__":
    mostrar_portada()
    nombre_jugador = inicio()
    
    while True:
        personaje_seleccionado = mostrar_seleccion_personaje()
        jugador = Jugador(personaje_seleccionado)
        formas_buenas_seleccionadas, formas_malas_seleccionadas = mostrar_menu()
        accion = ejecutar_juego(nombre_jugador)
        if accion == SALIR_JUEGO:
            break

    pygame.quit()