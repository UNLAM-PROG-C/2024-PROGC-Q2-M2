import pygame
import time 
from utils import imagenes_personajes, imagen_portada, draw_text, imagenes_formas_buenas, imagenes_formas_malas, filtro_blanco_negro
from globals import ALTO, ANCHO, DIR_PERSONAJE_DERECHA, FOTOGRAMAS_MENU, SALIR_JUEGO, pantalla, reloj, BLANCO, NEGRO, GRIS, VERDE, CELESTE 


def mostrarTop5():      
    registros = []
    with open('historial_record.txt', 'r') as archivo:
        lineas = archivo.readlines()[2:] 

        for linea in lineas:
            datos = linea.split('|')
            nombre = datos[0].strip()
            puntaje = int(datos[1].strip())
            fecha = datos[2].strip()
            registros.append((nombre, puntaje, fecha))

    top5 = sorted(registros, key=lambda x: x[1], reverse=True)[:5]

    pygame.display.set_caption("Top 5 Jugadores")
    fuente = pygame.font.Font('fonts/dogicapixelbold.ttf', 15)
    fuente_titulo = pygame.font.Font('fonts/dogicapixelbold.ttf', 20)
    blanco = (255, 255, 255)
    gris = (50, 50, 50)
    celeste = (0, 191, 255)
    pantalla.fill(gris)

    
    titulo_texto = fuente_titulo.render("Top 5 Jugadores", True, celeste)
    pantalla.blit(titulo_texto, (150, 30))

    
    encabezados = ["Nombre", "Puntaje", "Fecha"]
    x_offset = [50, 250, 400]
    for i, encabezado in enumerate(encabezados):
        texto = fuente.render(encabezado, True, blanco)
        pantalla.blit(texto, (x_offset[i], 100))

    # Dibujar cada registro del top 5 en la tabla
    for i, (nombre, puntaje, fecha) in enumerate(top5):
        y = 150 + i * 50
        pantalla.blit(fuente.render(nombre, True, blanco), (x_offset[0], y))
        pantalla.blit(fuente.render(str(puntaje), True, blanco), (x_offset[1], y))
        pantalla.blit(fuente.render(fecha, True, blanco), (x_offset[2], y))

    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
        pygame.display.flip()

#  Función para mostrar la pantalla de portada
def mostrar_portada():
    """Muestra la pantalla de portada con un botón para iniciar el juego."""
    portada_activa = True
    musica_activa = True
    fuente_titulo = pygame.font.Font('fonts/dogicapixelbold.ttf', 55)
    fuente_boton = pygame.font.Font('fonts/dogicapixelbold.ttf', 30)
    ancho_boton = 280
    alto_boton = 75
    
    x_boton_salir = 20
    y_boton_salir = ALTO - alto_boton - 20

    # Posición del botón "Jugar"
    x_boton = (ANCHO // 2) - (ancho_boton // 2)
    y_boton = (ALTO // 2) - (alto_boton // 2)
    
    espacio_entre_botones = 20  # Espacio entre los botones verticalmente
    y_boton_musica = y_boton + alto_boton + espacio_entre_botones
    y_boton_top5 = y_boton_musica + alto_boton + espacio_entre_botones

    boton_jugar = pygame.Rect(x_boton, y_boton, ancho_boton, alto_boton)
    boton_musica = pygame.Rect(x_boton, y_boton_musica, ancho_boton, alto_boton)
    boton_top5 = pygame.Rect(x_boton, y_boton_top5, ancho_boton, alto_boton)
    boton_salir = pygame.Rect(x_boton_salir, y_boton_salir, ancho_boton - 110, alto_boton - 20)


    while portada_activa:
        pantalla.blit(imagen_portada, (0, 0))  # Dibujamos la imagen de fondo
        texto_titulo = fuente_titulo.render("Tengo Hambre", True, BLANCO)
        pantalla.blit(texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, 100))

        # Dibujar botones y textos
        pygame.draw.rect(pantalla, GRIS, boton_jugar)
        texto_boton = fuente_boton.render("Jugar!", True, CELESTE)
        pantalla.blit(texto_boton, texto_boton.get_rect(center=boton_jugar.center))
        
        pygame.draw.rect(pantalla, GRIS, boton_musica)
        texto_boton_musica = fuente_boton.render("Musica", True, CELESTE)
        pantalla.blit(texto_boton_musica, texto_boton_musica.get_rect(center=boton_musica.center))
        
        pygame.draw.rect(pantalla, GRIS, boton_top5)
        texto_boton_top5 = fuente_boton.render("Top 5", True, CELESTE)
        pantalla.blit(texto_boton_top5, texto_boton_top5.get_rect(center=boton_top5.center))
        
        pygame.draw.rect(pantalla, GRIS, boton_salir)
        texto_boton_salir = fuente_boton.render(SALIR_JUEGO, True, CELESTE)
        texto_boton_salir_rect = texto_boton_salir.get_rect(center=boton_salir.center)
        pantalla.blit(texto_boton_salir, texto_boton_salir_rect)

        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(evento.pos):
                    portada_activa = False
                elif boton_musica.collidepoint(evento.pos):
                    if musica_activa:
                        pygame.mixer.music.play(-1)
                        musica_activa = False
                    else:
                        pygame.mixer.music.stop() 
                        musica_activa = True
                elif boton_top5.collidepoint(evento.pos):
                    mostrarTop5()
                    pygame.quit()
                    exit()
                elif boton_salir.collidepoint(evento.pos):
                    pygame.quit()
                    exit()

        pygame.display.flip()
        reloj.tick(FOTOGRAMAS_MENU)

# Función para mostrar la pantalla de final del juego
def mostrar_pantalla_fin():
    """Muestra la pantalla final del juego con las opciones de 'Volver a Jugar' o 'Salir'."""
    fin_activo = True
    fuente_game_over = pygame.font.SysFont(None, 72)
    fuente_boton = pygame.font.SysFont(None, 48)
    ancho_boton = 250
    alto_boton = 100

    filtro_blanco_negro(pantalla)

    texto_game_over = fuente_game_over.render("¡Juego Terminado!", True, BLANCO)
    pantalla.blit(texto_game_over, (ANCHO // 2 - texto_game_over.get_width() // 2, ALTO // 3))

    # Posiciones de los botones
    x_boton_volver = (ANCHO // 4) - (ancho_boton // 2)
    x_boton_salir = (3 * ANCHO // 4) - (ancho_boton // 2)
    y_botones = ALTO // 3 + texto_game_over.get_height() + 20

    boton_volver = pygame.Rect(x_boton_volver, y_botones, ancho_boton, alto_boton)
    boton_salir = pygame.Rect(x_boton_salir, y_botones, ancho_boton, alto_boton)

    # Dibujar el botón "Volver a Jugar"
    pygame.draw.rect(pantalla, (0, 150, 0), boton_volver)
    texto_boton_volver = fuente_boton.render("Volver a Jugar", True, BLANCO)
    texto_boton_volver_rect = texto_boton_volver.get_rect(center=boton_volver.center)
    pantalla.blit(texto_boton_volver, texto_boton_volver_rect)

    # Dibujar el botón "Salir"
    pygame.draw.rect(pantalla, (150, 0, 0), boton_salir)
    texto_boton_salir = fuente_boton.render("Salir", True, BLANCO)
    texto_boton_salir_rect = texto_boton_salir.get_rect(center=boton_salir.center)
    pantalla.blit(texto_boton_salir, texto_boton_salir_rect)

    while fin_activo:
        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver.collidepoint(evento.pos):
                    return "volver"
                elif boton_salir.collidepoint(evento.pos):
                    return "salir"

        pygame.display.flip()
        reloj.tick(FOTOGRAMAS_MENU)


# Función para mostrar el menú de selección
def mostrar_menu():
    """Muestra el menú de selección de comidas buenas y malas.
    """
    fuente_titulo = pygame.font.SysFont(None, 72)
    while True:
        menu_activo = True
        opciones = list(imagenes_formas_buenas.keys())
        seleccionadas_buenas = []
        seleccionadas_malas = []
        fuente = pygame.font.SysFont(None, 36)
        ancho_boton = 200
        alto_boton = 50
        ancho_imagen = 50

        # Calculamos la posición 'x' centrada para los botones de las formas buenas y malas
        x_centrada_buena = (ANCHO // 4) - (ancho_boton // 2)
        x_centrada_mala = (3 * ANCHO // 4) - (ancho_boton // 2)

        # Definimos las posiciones y tamaños de los botones
        botones_buenas = [
            (pygame.Rect((idx % 3) * (ancho_imagen + 20) + x_centrada_buena, 200 + (idx // 3) * (alto_boton + 20), ancho_imagen, alto_boton), opcion, imagenes_formas_buenas[opcion])
            for idx, opcion in enumerate(opciones)
        ]
        botones_malas = [
            (pygame.Rect((idx % 3) * (ancho_imagen + 20) + x_centrada_mala, 200 + (idx // 3) * (alto_boton + 20), ancho_imagen, alto_boton), opcion, imagenes_formas_buenas[opcion])
            for idx, opcion in enumerate(opciones)
        ]

        while menu_activo:
            pantalla.fill(BLANCO)
            texto_titulo = fuente_titulo.render("Selección de Comidas", True, NEGRO)
            pantalla.blit(texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, 50))

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    # Verificar clic en botones de formas buenas
                    manejar_seleccion(pos, botones_buenas, seleccionadas_buenas, seleccionadas_malas)
                    # Verificar clic en botones de formas malas
                    manejar_seleccion(pos, botones_malas, seleccionadas_malas, seleccionadas_buenas)
                elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                    menu_activo = False

            # Dibujar los botones y mostrar el texto correspondiente
            mostrar_botones(botones_buenas, seleccionadas_buenas, "Comidas Buenas:", x_centrada_buena, 150, (0, 200, 0), ancho_imagen, alto_boton)
            mostrar_botones(botones_malas, seleccionadas_malas, "Comidas Malas:", x_centrada_mala, 150, (200, 0, 0), ancho_imagen, alto_boton)

            # Mostrar instrucciones
            instrucciones = [
                "Haz clic en las comidas para seleccionar/deseleccionar.",
                "Presiona ENTER para comenzar el juego."
            ]
            for idx, instruccion in enumerate(instrucciones):
                texto_instruccion = fuente.render(instruccion, True, NEGRO)
                pantalla.blit(texto_instruccion, (ANCHO // 2 - texto_instruccion.get_width() // 2, 450 + idx * 30))

            pygame.display.flip()
            reloj.tick(FOTOGRAMAS_MENU)

        # Validar que al menos haya una forma buena y una mala seleccionada
        if seleccionadas_buenas and seleccionadas_malas:
            return seleccionadas_buenas, seleccionadas_malas
        else:
            # Mostrar mensaje de error si no se seleccionó ninguna opción válida
            fuente_error = pygame.font.SysFont(None, 48)
            texto_error = fuente_error.render("Debe seleccionar al menos una forma buena y una forma mala.", True, (255, 0, 0)) # Ajustar para que se vea bien
            pantalla.blit(texto_error, (ANCHO // 2 - texto_error.get_width() // 2, ALTO // 2))
            pygame.display.flip()
            time.sleep(2)  # Pausa para que el usuario vea el mensaje

# Función para manejar la selección de opciones del menú
def manejar_seleccion(pos, botones, seleccionadas, seleccionadas_contrarias):
    """Maneja la selección y deselección de opciones del menú.
    """
    for boton, opcion, imagen in botones:
        if boton.collidepoint(pos):
            if opcion not in seleccionadas:
                if opcion in seleccionadas_contrarias:
                    seleccionadas_contrarias.remove(opcion)
                seleccionadas.append(opcion)
            else:
                seleccionadas.remove(opcion)

# Función para mostrar los botones en pantalla
def mostrar_botones(botones, seleccionadas, titulo, x, y, color_seleccionado, ancho_boton, alto_boton):
    """Dibuja los botones y muestra el título correspondiente.
    """
    fuente = pygame.font.SysFont(None, 36)
    texto = fuente.render(titulo, True, NEGRO)
    pantalla.blit(texto, (x, y))
    for boton, opcion, imagen in botones:
        seleccionado = opcion in seleccionadas
        color_boton = color_seleccionado if seleccionado else (200, 200, 200)
        pygame.draw.rect(pantalla, color_boton, boton)
        posicion_x = boton.x + (ancho_boton - imagen.get_width()) // 2
        posicion_y = boton.y + (alto_boton - imagen.get_height()) // 2
        pantalla.blit(imagen, (posicion_x, posicion_y))

def mostrar_seleccion_personaje():
    """Muestra el menú para seleccionar el personaje del jugador."""
    seleccion_activa = True
    fuente_titulo = pygame.font.SysFont(None, 72)
    fuente_boton = pygame.font.SysFont(None, 36)
    ancho_boton = 150
    alto_boton = 200

    # Posiciones iniciales de los botones de personajes
    espaciado = 50
    x_inicial = (ANCHO - (len(imagenes_personajes) * (ancho_boton + espaciado) - espaciado)) // 2
    y_boton = ALTO // 2 - alto_boton // 2

    botones_personajes = []

    # Crear rectángulos para cada personaje
    for idx, nombre_personaje in enumerate(imagenes_personajes.keys()):
        x_boton = x_inicial + idx * (ancho_boton + espaciado)
        boton = pygame.Rect(x_boton, y_boton, ancho_boton, alto_boton)
        botones_personajes.append((boton, nombre_personaje))

    personaje_seleccionado = None

    while seleccion_activa:
        pantalla.fill(BLANCO)  # Fondo blanco
        texto_titulo = fuente_titulo.render("Seleccioná tu Personaje", True, NEGRO)
        pantalla.blit(texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, 50))

        # Dibujar los botones de personajes
        for boton, nombre_personaje in botones_personajes:
            pygame.draw.rect(pantalla, (200, 200, 200), boton)
            imagen_personaje = imagenes_personajes[nombre_personaje][DIR_PERSONAJE_DERECHA]
            pantalla.blit(imagen_personaje, (boton.x + (ancho_boton // 2) - imagen_personaje.get_width() // 2, boton.y + (alto_boton // 2) - imagen_personaje.get_height() // 2))
            texto_nombre = fuente_boton.render(nombre_personaje, True, NEGRO)
            pantalla.blit(texto_nombre, (boton.x + (ancho_boton // 2) - texto_nombre.get_width() // 2, boton.y + alto_boton))

        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for boton, nombre_personaje in botones_personajes:
                    if boton.collidepoint(pos):
                        personaje_seleccionado = nombre_personaje
                        seleccion_activa = False

        pygame.display.flip()
        reloj.tick(FOTOGRAMAS_MENU)

    return personaje_seleccionado