from utils import imagenes_personajes
from globals import ALTO, ANCHO, DIR_PERSONAJE_DERECHA, DIR_PERSONAJE_IZQUIERDA

class Jugador:
    def __init__(self, personaje='Nena 1'):
        self.ancho_jugador = 100
        self.alto_jugador = int(self.ancho_jugador * 1.5)
        self.imagen_derecha = imagenes_personajes[personaje][DIR_PERSONAJE_DERECHA]
        self.imagen_izquierda = imagenes_personajes[personaje][DIR_PERSONAJE_IZQUIERDA]

        self.x = ANCHO // 2 - self.ancho_jugador // 2
        self.y = ALTO - self.alto_jugador - 10
        self.direccion_jugador = DIR_PERSONAJE_DERECHA

    def mover(self, direccion, velocidad, limites):
        """Mueve al jugador dentro de los límites de la pantalla."""
        if direccion == DIR_PERSONAJE_IZQUIERDA and self.x - velocidad >= limites[DIR_PERSONAJE_IZQUIERDA]:
            self.x -= velocidad
            self.direccion_jugador = DIR_PERSONAJE_IZQUIERDA
        elif direccion == DIR_PERSONAJE_DERECHA and self.x + velocidad <= limites[DIR_PERSONAJE_DERECHA]:
            self.x += velocidad
            self.direccion_jugador = DIR_PERSONAJE_DERECHA

    def dibujar(self, pantalla):
        """Dibuja al jugador en pantalla según la dirección."""
        imagen = self.imagen_derecha if self.direccion_jugador == DIR_PERSONAJE_DERECHA else self.imagen_izquierda
        pantalla.blit(imagen, (self.x, self.y))