import threading
import time
import random
import globals
from queue import Queue
from forma import Forma
from globals import ALTO, CANTIDAD_FLUCTUACION_VIDAS, FOTOGRAMAS_FORMAS, TIPO_FORMA_BUENA

class GeneradorFormas:
    def __init__(self, cola, lock, tiempo_inicial, stop_event, formas_buenas_seleccionadas, formas_malas_seleccionadas, frecuencia_base=1.0):
        self.cola = cola
        self.lock = lock
        self.frecuencia_base = frecuencia_base
        self.tiempo_inicial = tiempo_inicial
        self.stop_event = stop_event
        self.formas_buenas_seleccionadas = formas_buenas_seleccionadas
        self.formas_malas_seleccionadas = formas_malas_seleccionadas

    def generar_formas(self):
        while not self.stop_event.is_set():
            tiempo_juego = time.time() - self.tiempo_inicial
            frecuencia = max(0.2, self.frecuencia_base - tiempo_juego * 0.01)
            nueva_forma = Forma(self.formas_buenas_seleccionadas, self.formas_malas_seleccionadas)

            with self.lock:
                self.cola.put(nueva_forma)
            self.stop_event.wait(frecuencia)

def actualizar_forma(forma, incremento_velocidad, jugador):
        """Actualiza la posición de una forma y verifica si colisiona o sale de la pantalla.
        Retorna None si la forma debe eliminarse (colisión o fuera de pantalla).
        """
        forma.y += forma.velocidad + incremento_velocidad
        if forma.y > ALTO:
            return None

        if (jugador.y < forma.y + forma.tamano and
            jugador.x < forma.x + forma.tamano and
            jugador.x + jugador.ancho_jugador > forma.x):
            if forma.tipo ==  TIPO_FORMA_BUENA:
                globals.puntaje += CANTIDAD_FLUCTUACION_VIDAS
            else:
                globals.vidas -= CANTIDAD_FLUCTUACION_VIDAS
            return None  

        return forma


def procesar_formas(self):
        """Procesa todas las formas, actualiza su posición y detecta colisiones."""
        formas_actualizadas = []
        while not self.cola.empty():
            forma = self.cola.get()
            tiempo_juego = time.time() - self.tiempo_inicial
            incremento_velocidad = tiempo_juego * 0.002

            forma_actualizada = actualizar_forma(forma, incremento_velocidad, self.jugador)
            if forma_actualizada:
                formas_actualizadas.append(forma_actualizada)

        return formas_actualizadas

class MovimientoFormas:
    def __init__(self, cola, lock, jugador, reloj, tiempo_inicial, stop_event):
        self.cola = cola
        self.lock = lock
        self.jugador = jugador
        self.reloj = reloj
        self.tiempo_inicial = tiempo_inicial
        self.stop_event = stop_event

    def mover_formas(self):
        """Controla el movimiento de las formas y detecta colisiones."""
        while not self.stop_event.is_set():
            self.reloj.tick(FOTOGRAMAS_FORMAS)

            with self.lock:
                formas_actualizadas = procesar_formas(self)
                for forma in formas_actualizadas:
                    self.cola.put(forma)