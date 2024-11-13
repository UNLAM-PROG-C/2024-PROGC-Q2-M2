from queue import Queue
import pygame
import threading
import time 
import globals
from inicio import inicio
from jugador import Jugador
from hilos import GeneradorFormas, MovimientoFormas
from forma import dibujar_forma
from menu import mostrar_portada, mostrar_menu, mostrar_seleccion_personaje, mostrar_pantalla_fin
from utils import  imagen_fondo
from globals import ANCHO, ALTO, NEGRO, reloj, pantalla, velocidad_jugador, cola_formas, lock_formas

pygame.init()

def ejecutar_juego():
    """Función principal para ejecutar el flujo del juego."""
    global tiempo_inicial, ejecutando, stop_event, lock_formas, cola_formas, reloj

    # Reiniciar el estado del juego
    globals.puntaje = 0
    globals.vidas = 3
    tiempo_inicial = time.time()
    ejecutando = True
    cola_formas = Queue()
    
    # Evento para controlar la detención de hilos
    stop_event = threading.Event()

    # Crear instancias de los generadores y movimiento
    generador_formas = GeneradorFormas(cola_formas, lock_formas, tiempo_inicial, stop_event, formas_buenas_seleccionadas, formas_malas_seleccionadas)
    movimiento_formas = MovimientoFormas(cola_formas, lock_formas, jugador, reloj, tiempo_inicial, stop_event)

    # Iniciar los hilos para generar y mover las formas
    hilo_generador = threading.Thread(target=generador_formas.generar_formas)
    hilo_movedor = threading.Thread(target=movimiento_formas.mover_formas)
    hilo_generador.start()
    hilo_movedor.start()

    # Bucle principal del juego
    while ejecutando:
        reloj.tick(60)  # Controlamos el juego a 60 FPS
        pantalla.blit(imagen_fondo, (0, 0))  # Dibujamos la imagen de fondo

        # Manejamos los eventos del juego
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # Si el jugador cierra la ventana
                ejecutando = False
                stop_event.set()
                return "salir"

        # Manejo del movimiento del jugador
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and jugador.x - velocidad_jugador >= 0:
            jugador.x -= velocidad_jugador  # Movemos al jugador a la izquierda
            jugador.direccion_jugador = 'izquierda'
        elif teclas[pygame.K_RIGHT] and jugador.x + velocidad_jugador <= ANCHO - jugador.ancho_jugador:
            jugador.x += velocidad_jugador  # Movemos al jugador a la derecha
            jugador.direccion_jugador = 'derecha'

        # Dibujamos al jugador según la dirección
        if jugador.direccion_jugador == 'derecha':
            pantalla.blit(jugador.imagen_derecha, (jugador.x, jugador.y))
        else:
            pantalla.blit(jugador.imagen_izquierda, (jugador.x, jugador.y))

        # Dibujamos las formas
        with lock_formas:
            formas_a_dibujar = list(cola_formas.queue)
        for forma in formas_a_dibujar:
            dibujar_forma(forma)

        # Mostramos el puntaje y las vidas
        fuente = pygame.font.SysFont(None, 36)
        texto_puntaje = fuente.render(f"Puntaje: {globals.puntaje}", True, NEGRO)
        texto_vidas = fuente.render(f"Vidas: {globals.vidas}", True, NEGRO)
        pantalla.blit(texto_puntaje, (10, 10))
        pantalla.blit(texto_vidas, (10, 50))

        # Verificamos si el jugador ha perdido todas las vidas
        if globals.vidas <= 0:
            fuente_game_over = pygame.font.SysFont(None, 72)
            texto_game_over = fuente_game_over.render("¡Juego Terminado!", True, NEGRO)
            pantalla.blit(texto_game_over, (ANCHO // 2 - texto_game_over.get_width() // 2, ALTO // 2))
            pygame.display.flip()
            time.sleep(3)
            ejecutando = False
            stop_event.set()

        # Actualizamos la pantalla
        pygame.display.flip()

    # Esperar a que los hilos terminen antes de cerrar
    hilo_generador.join()
    hilo_movedor.join()

    # Mostrar la pantalla de fin del juego y tomar la acción correspondiente
    accion = mostrar_pantalla_fin()
    return accion


# Inicia el flujo principal del juego
if __name__ == "__main__":
    inicio()
    mostrar_portada()
    
    while True:
        # Seleccionar el personaje del jugador
        personaje_seleccionado = mostrar_seleccion_personaje()

        # Crear la instancia del jugador con el personaje seleccionado
        jugador = Jugador(personaje_seleccionado)

        # Mostramos el menú y obtenemos las selecciones del jugador
        formas_buenas_seleccionadas, formas_malas_seleccionadas = mostrar_menu()

        # Ejecutamos el juego y obtenemos la acción seleccionada al final
        accion = ejecutar_juego()

        # Verificamos la acción después de que termina el juego
        if accion == "salir":
            break  # Salimos del bucle principal y cerramos el juego

    pygame.quit()
