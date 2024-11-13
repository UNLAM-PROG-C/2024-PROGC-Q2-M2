import pygame
import random
from utils import imagenes_formas_buenas, imagenes_formas_malas, ANCHO
from globals import TAM_FORMA_LIMITE_INFERIOR, TAM_FORMA_LIMITE_SUPERIOR, TIPO_FORMA_BUENA, TIPO_FORMA_MALA, VEL_CAIDA_LIMITE_INFERIOR, VEL_CAIDA_LIMITE_SUPERIOR, pantalla, ANCHO

# Clase que representa una forma que cae (puede ser buena o mala)
class Forma:
    def __init__(self, formas_buenas_seleccionadas, formas_malas_seleccionadas):
        self.formas_seleccionadas = formas_buenas_seleccionadas + formas_malas_seleccionadas
        self.tamano = random.randint(TAM_FORMA_LIMITE_INFERIOR, TAM_FORMA_LIMITE_SUPERIOR)  # Tamaño aleatorio de la forma
        self.nombre = random.choice(self.formas_seleccionadas)  # Nombre de la forma
        self.x = random.randint(0, ANCHO - self.tamano)  # Posición horizontal aleatoria
        self.y = -self.tamano  # Posición inicial (fuera de la pantalla, para caer desde arriba)
        self.velocidad = random.uniform(VEL_CAIDA_LIMITE_INFERIOR, VEL_CAIDA_LIMITE_SUPERIOR)  # Velocidad de caída

        # Tipo de la forma (buena o mala)
        if self.nombre in formas_buenas_seleccionadas:
            self.tipo = TIPO_FORMA_BUENA
        else:
            self.tipo = TIPO_FORMA_MALA 

        # Asignamos la imagen correspondiente según el tipo (buena o mala)
        if self.tipo == TIPO_FORMA_BUENA:
            self.imagen = imagenes_formas_buenas[self.nombre]
        else:
            self.imagen = imagenes_formas_malas[self.nombre]
        
        # Redimensionamos la imagen al tamaño de la forma
        self.imagen = pygame.transform.scale(self.imagen, (self.tamano, self.tamano))

    def mover(self, incremento_velocidad, alto_pantalla):
        """Mueve la forma hacia abajo. Retorna True si sale de la pantalla."""
        self.y += self.velocidad + incremento_velocidad
        return self.y > alto_pantalla

    def colisiona_con(self, jugador):
        """Verifica si la forma colisiona con el jugador."""
        return (
            jugador.y < self.y + self.tamano and
            jugador.x < self.x + self.tamano and
            jugador.x + jugador.ancho_jugador > self.x
        )

# Función para dibujar una forma en la pantalla
def dibujar_forma(forma):
    pantalla.blit(forma.imagen, (forma.x, forma.y))  # Dibujamos la imagen en la posición de la forma