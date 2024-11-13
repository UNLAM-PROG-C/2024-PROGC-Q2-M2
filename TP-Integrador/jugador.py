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