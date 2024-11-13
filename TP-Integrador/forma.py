import pygame
import random
from utils import imagenes_formas_buenas, imagenes_formas_malas, ANCHO
from globals import TAM_FORMA_LIMITE_INFERIOR, TAM_FORMA_LIMITE_SUPERIOR, TIPO_FORMA_BUENA, TIPO_FORMA_MALA, VEL_CAIDA_LIMITE_INFERIOR, VEL_CAIDA_LIMITE_SUPERIOR, pantalla, ANCHO

class Forma:
    def __init__(self, formas_buenas_seleccionadas, formas_malas_seleccionadas):
        self.formas_seleccionadas = formas_buenas_seleccionadas + formas_malas_seleccionadas
        self.tamano = random.randint(TAM_FORMA_LIMITE_INFERIOR, TAM_FORMA_LIMITE_SUPERIOR) 
        self.nombre = random.choice(self.formas_seleccionadas)  
        self.x = random.randint(0, ANCHO - self.tamano)  
        self.y = -self.tamano  
        self.velocidad = random.uniform(VEL_CAIDA_LIMITE_INFERIOR, VEL_CAIDA_LIMITE_SUPERIOR)

        if self.nombre in formas_buenas_seleccionadas:
            self.tipo = TIPO_FORMA_BUENA
        else:
            self.tipo = TIPO_FORMA_MALA 
        if self.tipo == TIPO_FORMA_BUENA:
            self.imagen = imagenes_formas_buenas[self.nombre]
        else:
            self.imagen = imagenes_formas_malas[self.nombre]
        
        self.imagen = pygame.transform.scale(self.imagen, (self.tamano, self.tamano))

def dibujar_forma(forma):
    pantalla.blit(forma.imagen, (forma.x, forma.y)) 