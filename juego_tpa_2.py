import pygame, sys, time
# Importa la librería Pygame para el desarrollo de juegos y 'sys' para funciones del sistema.

#Constantes
ANCHO, ALTO = 1280, 720
# Define el ancho y alto de la ventana del juego en píxeles.
FPS = 60
# Establece el número de fotogramas por segundo (Frame Per Second) para la fluidez del juego.

# Colores
BLANCO = (255, 255, 255)
# Define el color blanco usando valores RGB.
NEGRO = (0, 0, 0)
# Define el color negro.
AZUL = (50, 120, 255)
# Define el color azul.
ROJO = (255, 50, 50)
# Define el color rojo.
VERDE = (50, 200, 50)
# Define el color verde.
GRIS = (150, 150, 150)
# Define el color gris.
MARRON = (139, 69, 19)
# Define el color marrón.

#Inicio del juego
pygame.init()
# Inicializa todos los módulos de Pygame necesarios para el juego.
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
# Crea la ventana de visualización (la superficie de juego) con el ancho y alto definidos.
pygame.display.set_caption("EMPTY SOLDIER")
# Establece el título de la ventana del juego.
RELOJ = pygame.time.Clock()
# Crea un objeto Clock para controlar la velocidad de fotogramas del juego.
FUENTE = pygame.font.SysFont("Arial", 24)
# Carga una fuente del sistema (Arial) con un tamaño de 24 para texto general.
FUENTE_PEQUE = pygame.font.SysFont("Arial", 18)
# Carga una fuente del sistema (Arial) con un tamaño de 18 para texto más pequeño.

#Clases
class Boton:
# Define la clase Boton para crear botones interactivos en la interfaz.
    
    def __init__(self, x, y, w, h, texto):
    # Constructor de la clase Boton.
        
        self.rect = pygame.Rect(x, y, w, h)
        # Crea un objeto Rect (rectángulo) que define la posición y el tamaño del botón.
        
        self.texto = texto
        # Almacena el texto que se mostrará en el botón.

    def dibujar(self, surface):
    # Método para dibujar el botón en una superficie dada.
        
        pygame.draw.rect(surface, GRIS, self.rect)
        # Dibuja el cuerpo principal del botón con color gris.
        
        pygame.draw.rect(surface, BLANCO, self.rect, 2)
        # Dibuja un borde blanco alrededor del botón con un grosor de 2 píxeles.
        
        texto_img = FUENTE.render(self.texto, True, BLANCO)
        # Renderiza el texto del botón en una superficie de imagen con color blanco y antialiasing (True).
        
        surface.blit(texto_img, (self.rect.x + (self.rect.w - texto_img.get_width())//2,
        # Dibuja la imagen del texto en el centro horizontal del botón.
                                 self.rect.y + (self.rect.h - texto_img.get_height())//2))
        # Dibuja la imagen del texto en el centro vertical del botón.

    def esta_click(self, pos):
    # Método para verificar si el botón ha sido clickeado.
        
        return self.rect.collidepoint(pos)
        # Retorna True si la posición del click (pos) colisiona con el rectángulo del botón.

class InputBox:
# Define la clase InputBox para crear campos de entrada de texto interactivos.
    
    def __init__(self, x, y, w, h, texto=""):
    # Constructor de la clase InputBox.
        
        self.rect = pygame.Rect(x, y, w, h)
        # Crea un objeto Rect que define la posición y el tamaño del campo de entrada.
        
        self.color_inactivo = GRIS
        # Define el color del campo de entrada cuando no está activo.
        
        self.color_activo = AZUL
        # Define el color del campo de entrada cuando está activo.
        
        self.color = self.color_inactivo
        # Establece el color inicial del campo de entrada como inactivo.
        
        self.texto = texto
        # Almacena el texto actual en el campo de entrada.
        
        self.txt_surface = FUENTE.render(texto, True, BLANCO)
        # Renderiza el texto inicial en una superficie de imagen.
        
        self.activo = False
        # Bandera para indicar si el campo de entrada está activo (si se puede escribir en él).
        
        self.oculto = False  # para password
        # Bandera para ocultar el texto (útil para campos de contraseña).

    def manejar_evento(self, event):
    # Método para manejar los eventos del teclado y ratón para el campo de entrada.
        
        if event.type == pygame.MOUSEBUTTONDOWN:
        # Si el evento es un click del ratón.
            
            # Si se clickea dentro, se activa
            if self.rect.collidepoint(event.pos):
            # Verifica si el click del ratón ocurrió dentro del campo de entrada.
                
                self.activo = True
                # Activa el campo de entrada.
                
                self.color = self.color_activo
                # Cambia el color del campo de entrada a activo.
            
            else:
            # Si el click del ratón fue fuera del campo de entrada.
                
                self.activo = False
                # Desactiva el campo de entrada.
                
                self.color = self.color_inactivo
                # Cambia el color del campo de entrada a inactivo.
        
        if event.type == pygame.KEYDOWN and self.activo:
        # Si el evento es una tecla presionada y el campo de entrada está activo.
            
            if event.key == pygame.K_BACKSPACE:
            # Si la tecla presionada es la de retroceso (borrar).
                
                self.texto = self.texto[:-1]
                # Elimina el último carácter del texto.
            
            elif event.key == pygame.K_RETURN:
            # Si la tecla presionada es Enter.
                
                return "enter"
                # Retorna la cadena "enter" para indicar que se presionó Enter.
            
            else:
            # Si es cualquier otra tecla.
                
                if len(self.texto) < 15 and event.unicode.isprintable():
                # Si la longitud del texto es menor a 15 y el carácter es imprimible.
                    
                    self.texto += event.unicode
                    # Añade el carácter al texto del campo de entrada.
            
            self.txt_surface = FUENTE.render("*"*len(self.texto) if self.oculto else self.texto, True, BLANCO)
            # Renderiza el texto actualizado. Si self.oculto es True, muestra asteriscos; de lo contrario, muestra el texto real.
            
        return None
        # Retorna None si no se presiona Enter.

    def dibujar(self, surface):
    # Método para dibujar el campo de entrada en una superficie.
        
        # Texto
        surface.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Dibuja el texto renderizado dentro del campo de entrada, con un pequeño desplazamiento.
        
        # Rectangulo
        pygame.draw.rect(surface, self.color, self.rect, 2)
        # Dibuja el rectángulo del campo de entrada con su color actual y un borde de 2 píxeles.

class Bala:
# Define la clase Bala para representar los proyectiles disparados.
    
    def __init__(self, x, y, direccion):
    # Constructor de la clase Bala.
        
        self.rect = pygame.Rect(x, y, 8, 4)
        # Crea un rectángulo para la bala con su posición y tamaño.
        
        self.vel = 15 * direccion  # direccion: 1 o -1
        # Establece la velocidad de la bala, multiplicada por la dirección (1 para derecha, -1 para izquierda).
        
        self.color = ROJO
        # Define el color de la bala como rojo.

    def mover(self):
    # Método para mover la bala.
        
        self.rect.x += self.vel
        # Actualiza la posición x de la bala según su velocidad.

    def dibujar(self, surface):
    # Método para dibujar la bala en una superficie.
        
        pygame.draw.rect(surface, self.color, self.rect)
        # Dibuja la bala como un rectángulo con su color.

class Bicicleta:
# Define la clase Bicicleta.
    
    def __init__(self, x, y):
    # Constructor de la clase Bicicleta.
        
        self.rect = pygame.Rect(x, y, 80, 40)
        # Crea un rectángulo para la bicicleta con su posición y tamaño.
        
        self.color = MARRON
        # Define el color de la bicicleta como marrón.
        
        self.ocupada = False
        # Bandera para indicar si la bicicleta está siendo usada por un jugador.

    def dibujar(self, surface):
    # Método para dibujar la bicicleta en una superficie.
        
        pygame.draw.rect(surface, self.color, self.rect)
        # Dibuja el cuerpo principal de la bicicleta.
        
        # Ruedas
        pygame.draw.circle(surface, GRIS, (self.rect.x + 15, self.rect.y + 40), 12)
        # Dibuja la primera rueda de la bicicleta como un círculo gris.
        pygame.draw.circle(surface, GRIS, (self.rect.x + 65, self.rect.y + 40), 12)
        # Dibuja la segunda rueda de la bicicleta.

class JugadorPVP:
# Define la clase JugadorPVP para los personajes controlables.
    
    def __init__(self, x, y, color, teclas):
    # Constructor de la clase JugadorPVP.
        
        self.rect = pygame.Rect(x, y, 40, 60)
        # Crea un rectángulo para el jugador con su posición y tamaño.
        
        self.color = color
        # Define el color del jugador.
        
        self.vel = 5
        # Establece la velocidad de movimiento del jugador.
        
        self.teclas = teclas
        # Diccionario que mapea acciones a teclas (ej. 'izquierda': pygame.K_a).
        
        self.balas = []
        # Lista para almacenar las balas disparadas por el jugador.
        
        self.en_bicicleta = False
        # Bandera para indicar si el jugador está montado en una bicicleta.
        
        self.bicicleta = None
        # Referencia al objeto Bicicleta si el jugador está montado.
        
        self.nombre = "Jugador"
        # Nombre por defecto del jugador.
        
        self.vida = 100
        # Puntos de vida del jugador.
        
        self.fuerza = 10
        # Atributo de fuerza del jugador.
        
        self.defensa = 5
        # Atributo de defensa del jugador.
        
        self.direccion = 1  # 1 = derecha, -1 = izquierda
        # Dirección a la que mira el jugador (para el disparo).

        self.ultimo_dash = 0
        # Guarda el momento en que se hizo el último dash (inicializado en 0 para que esté disponible al inicio).

        self.cooldown_dash = 1.5
        # Tiempo (en segundos) que debe esperar el jugador entre un dash y el siguiente.

        self.ultimo_daño = time.time ()
        # Guarda el tiempo actual como el último momento en que el jugador recibió daño (se usa para bloquear regeneración).

        self.vidas_restantes = 3
        # Número total de veces que el jugador puede reaparecer antes de perder definitivamente.

    def dash(self):
    # Método que permite al jugador moverse rápidamente una distancia corta (efecto "dash").

        ahora = time.time()
        # Obtiene el tiempo actual en segundos.

        if ahora - self.ultimo_dash >= self.cooldown_dash:
        # Verifica si ha pasado suficiente tiempo desde el último dash (cooldown cumplido).

            distancia_dash = 80
            # Define la distancia del desplazamiento rápido.

            if self.direccion == 1:
            # Si el jugador está mirando hacia la derecha.

                self.rect.x += distancia_dash
                # Lo desplaza 80 píxeles hacia la derecha.

            else:
            # Si está mirando hacia la izquierda.

                self.rect.x -= distancia_dash
                # Lo desplaza 80 píxeles hacia la izquierda.

            self.ultimo_dash = ahora
            # Actualiza el momento del último dash para aplicar el cooldown.

    def manejar_eventos(self, keys, colisiones):
    # Método para manejar los eventos de movimiento del jugador.
        
        if self.en_bicicleta:
        # Si el jugador está en bicicleta.
            
            velocidad_actual = 9
            # La velocidad del jugador es mayor (9).
        
        else:
        # Si el jugador no está en bicicleta.
            
            velocidad_actual = self.vel
            # La velocidad del jugador es su velocidad base (5).

        if keys[self.teclas['izquierda']]:
        # Si la tecla para moverse a la izquierda está presionada.
            
            self.rect.x -= velocidad_actual
            # Mueve al jugador a la izquierda.
            
            self.direccion = -1
            # Establece la dirección a la izquierda.
            
            if self.colisiona(colisiones):
            # Si el jugador colisiona con un obstáculo después de moverse.
                
                self.rect.x += velocidad_actual
                # Deshace el movimiento para evitar la colisión.

        if keys[self.teclas['derecha']]:
        # Si la tecla para moverse a la derecha está presionada.
            
            self.rect.x += velocidad_actual
            # Mueve al jugador a la derecha.
            
            self.direccion = 1
            # Establece la dirección a la derecha.
            
            if self.colisiona(colisiones):
            # Si el jugador colisiona con un obstáculo.
                
                self.rect.x -= velocidad_actual
                # Deshace el movimiento.

        if keys[self.teclas['arriba']]:
        # Si la tecla para moverse arriba está presionada.
            
            self.rect.y -= velocidad_actual
            # Mueve al jugador hacia arriba.
            
            if self.colisiona(colisiones):
            # Si el jugador colisiona con un obstáculo.
                
                self.rect.y += velocidad_actual
                # Deshace el movimiento.

        if keys[self.teclas['abajo']]:
        # Si la tecla para moverse abajo está presionada.
            
            self.rect.y += velocidad_actual
            # Mueve al jugador hacia abajo.
            
            if self.colisiona(colisiones):
            # Si el jugador colisiona con un obstáculo.
                
                self.rect.y -= velocidad_actual
                # Deshace el movimiento.

        if self.en_bicicleta and self.bicicleta:
        # Si el jugador está en bicicleta y tiene una bicicleta asociada.
            
            # Mover bicicleta junto con jugador
            self.bicicleta.rect.x = self.rect.x - 20
            # Mueve la bicicleta para que su posición x esté relacionada con la del jugador.
            self.bicicleta.rect.y = self.rect.y + 30
            # Mueve la bicicleta para que su posición y esté relacionada con la del jugador.

    def colisiona(self, colisiones):
    # Método para verificar colisiones del jugador con obstáculos.
        
        for obstaculo in colisiones:
        # Itera sobre la lista de obstáculos.
            
            if self.rect.colliderect(obstaculo):
            # Si el rectángulo del jugador colisiona con el rectángulo de un obstáculo.
                
                return True
                # Retorna True, indicando una colisión.
        
        return False
        # Retorna False si no hay colisiones.

    def disparar(self):
    # Método para que el jugador dispare una bala.
        
        if len(self.balas) < 5:
        # Si el número de balas en pantalla es menor a 5 (límite de balas).
            
            if self.direccion == 1:
            # Si el jugador mira a la derecha.
                
                x = self.rect.right
                # La bala aparece a la derecha del jugador.
            
            else:
            # Si el jugador mira a la izquierda.
                
                x = self.rect.left - 8
                # La bala aparece a la izquierda del jugador.
            
            y = self.rect.centery
            # La bala aparece a la altura del centro del jugador.
            
            self.balas.append(Bala(x, y, self.direccion))
            # Añade una nueva instancia de Bala a la lista de balas del jugador.

    def actualizar_balas(self, colisiones, otro_jugador):
    # Método para actualizar la posición de las balas y manejar colisiones.
        
        for bala in self.balas[:]:
        # Itera sobre una copia de la lista de balas (para poder eliminar elementos durante la iteración).
            
            bala.mover()
            # Mueve la bala.
            
            # Quitar si sale de pantalla
            if bala.rect.right < 0 or bala.rect.left > ANCHO:
            # Si la bala se sale por los bordes de la pantalla.
                
                self.balas.remove(bala)
                # Elimina la bala de la lista.
                
                continue
                # Pasa a la siguiente bala.

            if bala.rect.colliderect (otro_jugador.rect):
            # Verifica si la bala colisiona con el rectángulo del otro jugador.

                if bala in self.balas:
                # Asegura que la bala aún esté en la lista de balas del jugador (evita errores si ya fue eliminada).

                    self.balas.remove (bala)
                    # Elimina la bala de la lista para que desaparezca tras impactar.

                    daño = max (1, self.fuerza - otro_jugador.defensa)
                    # Calcula el daño causado, como la diferencia entre la fuerza del atacante y la defensa del defensor.
                    # Usa `max(1, ...)` para garantizar que al menos cause 1 punto de daño.

                    otro_jugador.ultimo_daño = time.time()
                    # Registra el momento en que el jugador fue dañado (usado para bloquear regeneración de vida temporalmente).

                    otro_jugador.vida -= daño
                    # Aplica el daño al jugador golpeado, reduciendo su vida.

                continue
                # Pasa a la siguiente bala sin seguir verificando esta (ya impactó o fue eliminada).

            # Quitar si choca obstaculo
            for obstaculo in colisiones:
            # Itera sobre la lista de obstáculos.
                
                if bala.rect.colliderect(obstaculo):
                # Si la bala colisiona con un obstáculo.
                    
                    if bala in self.balas:
                    # Verifica si la bala aún está en la lista (evita errores si ya fue eliminada).
                        
                        self.balas.remove(bala)
                        # Elimina la bala de la lista.
                    
                    break
                    # Sale del bucle de obstáculos una vez que la bala choca con uno.

    def regenerar_vida (self):
    # Método que permite al jugador recuperar vida lentamente si no ha recibido daño recientemente.

        ahora = time.time()
        # Obtiene el tiempo actual en segundos desde la época UNIX.

        if not hasattr (self, 'ultimo_regenerado'):
        # Verifica si el jugador ya tiene un atributo para controlar el último momento de regeneración.

            self.ultimo_regenerado = 0
            # Si no existe, lo inicializa en 0 (evita errores en la primera llamada).

        if ahora - self.ultimo_daño > 3:
        # Solo permite regenerar si han pasado más de 3 segundos desde que recibió daño.

            if self.vida < 100 and ahora - self.ultimo_regenerado >= 0.5:
            # Comprueba si la vida actual es menor al máximo (100)
            # y si han pasado al menos 0.5 segundos desde la última regeneración.

                self.vida += 0.5
                # Aumenta lentamente la vida del jugador (0.5 puntos por tic).

                self.vida = min(self.vida, 100)
                # Se asegura de que la vida no supere el máximo (100 HP).

                self.ultimo_regenerado = ahora
                # Actualiza el momento en que se regeneró vida, para controlar el cooldown de 0.5s.

    def montar_bicicleta(self, bicicleta):
    # Método para que el jugador intente montar una bicicleta.
        
        if not self.en_bicicleta and not bicicleta.ocupada:
        # Si el jugador no está en una bicicleta y la bicicleta no está ocupada.
            
            if self.rect.colliderect(bicicleta.rect):
            # Si el jugador está lo suficientemente cerca de la bicicleta para colisionar con ella.
                
                self.en_bicicleta = True
                # Establece la bandera de que el jugador está en bicicleta a True.
                
                self.bicicleta = bicicleta
                # Asigna la bicicleta al jugador.
                
                bicicleta.ocupada = True
                # Marca la bicicleta como ocupada.
                
                # Posicionar jugador sobre bici
                self.rect.x = bicicleta.rect.x + 20
                # Reposiciona al jugador en la posición x de la bicicleta.
                self.rect.y = bicicleta.rect.y - 30
                # Reposiciona al jugador en la posición y de la bicicleta.

    def desmontar_bicicleta(self):
    # Método para que el jugador desmonte de la bicicleta.
        
        if self.en_bicicleta:
        # Si el jugador está en bicicleta.
            
            self.en_bicicleta = False
            # Establece la bandera de que el jugador está en bicicleta a False.
            
            if self.bicicleta:
            # Si hay una bicicleta asignada al jugador.
                
                self.bicicleta.ocupada = False
                # Marca la bicicleta como no ocupada.
                
                self.bicicleta = None
                # Desasigna la bicicleta del jugador.

    def dibujar(self, surface):
    # Método para dibujar el jugador en la pantalla.
        
        if self.en_bicicleta:
        # Si el jugador está en bicicleta.
            
            # Dibuja el jugador "montado"
            # Dibujamos la bicicleta abajo
            if self.bicicleta:
            # Si hay una bicicleta asignada.
                
                self.bicicleta.dibujar(surface)
                # Dibuja la bicicleta.
            
            # Dibujo jugador pequeño encima
            pygame.draw.rect(surface, self.color, (self.rect.x, self.rect.y, self.rect.w//2, self.rect.h//2))
            # Dibuja una versión más pequeña del jugador (simulando que está montado).
        
        else:
        # Si el jugador no está en bicicleta.
            
            pygame.draw.rect(surface, self.color, self.rect)
            # Dibuja al jugador como un rectángulo de tamaño normal.

        # Dibujar balas
        for bala in self.balas:
        # Itera sobre la lista de balas del jugador.
            
            bala.dibujar(surface)
            # Dibuja cada bala.

        # Dibujar nombre sobre jugador
        texto_nombre = FUENTE_PEQUE.render(self.nombre, True, BLANCO)
        # Renderiza el nombre del jugador.
        
        surface.blit(texto_nombre, (self.rect.x, self.rect.y - 20))
        # Dibuja el nombre del jugador justo encima de su posición.

        barra_ancho = self.rect.width
        # Establece el ancho de la barra de vida igual al ancho del jugador.

        barra_alto = 8
        # Altura fija de la barra de vida (8 píxeles).

        x = self.rect.x
        # Coordenada x donde comienza la barra (alineada con el jugador).

        y = self.rect.y + self.rect.height + 5
        # Coordenada y justo debajo del jugador (5 píxeles por debajo de su sprite).

        porcentaje = max (0, self.vida ) / 100
        # Calcula el porcentaje de vida actual (entre 0.0 y 1.0), evita negativos.

        ancho_vida = int (barra_ancho * porcentaje)
        # Calcula el ancho proporcional de la barra verde según la vida restante.

        pygame.draw.rect (surface, (100, 0, 0), (x, y, barra_ancho, barra_alto))
        # Dibuja una barra de fondo roja (barra completa vacía).

        pygame.draw.rect (surface, (0, 255, 0), (x, y, ancho_vida, barra_alto))
        # Dibuja la parte verde encima, representando la vida actual.

        texto_vida = FUENTE_PEQUE.render (f'{self.vida} HP', True, BLANCO)
        # Renderiza el texto que muestra la cantidad exacta de vida en números.

        surface.blit (texto_vida, (x + (barra_ancho - texto_vida.get_width()) // 2, y -18))
        # Dibuja el texto centrado horizontalmente sobre la barra, un poco más arriba.

#Funciones de pantalla
def pantalla_inicio_sesion():
# Define la función para la pantalla de inicio de sesión.
    
    input_usuario = InputBox(ANCHO//2 - 100, ALTO//2 - 70, 200, 35)
    # Crea un campo de entrada para el nombre de usuario.
    
    input_password = InputBox(ANCHO//2 - 100, ALTO//2, 200, 35)
    # Crea un campo de entrada para la contraseña.
    
    input_password.oculto = True
    # Establece el campo de contraseña como oculto (mostrará asteriscos).
    
    boton_confirmar = Boton(ANCHO//2 - 60, ALTO//2 + 80, 120, 40, "Confirmar")
    # Crea un botón para confirmar el inicio de sesión.
    
    mensaje_error = ""
    # Inicializa una cadena vacía para mostrar mensajes de error.

    while True:
    # Bucle principal de la pantalla de inicio de sesión.
        
        PANTALLA.fill(NEGRO)
        # Rellena la pantalla con color negro (borra el contenido anterior).
        
        # Texto
        titulo = FUENTE.render("Inicio de sesión", True, BLANCO)
        # Renderiza el título "INICIO DE SESIÓN".
        PANTALLA.blit(titulo, (ANCHO//2 - titulo.get_width()//2, ALTO//2 - 130))
        # Dibuja el título centrado en la parte superior.

        etiqueta_usuario = FUENTE.render("Usuario:", True, BLANCO)
        # Renderiza la etiqueta "Usuario:".
        PANTALLA.blit(etiqueta_usuario, (ANCHO//2 - 180, ALTO//2 - 65))
        # Dibuja la etiqueta de usuario.

        etiqueta_password = FUENTE.render("Contraseña:", True, BLANCO)
        # Renderiza la etiqueta "Contraseña:".
        PANTALLA.blit(etiqueta_password, (ANCHO//2 - 210, ALTO//2 + 5))
        # Dibuja la etiqueta de contraseña.

        input_usuario.dibujar(PANTALLA)
        # Dibuja el campo de entrada de usuario.
        
        input_password.dibujar(PANTALLA)
        # Dibuja el campo de entrada de contraseña.
        
        boton_confirmar.dibujar(PANTALLA)
        # Dibuja el botón de confirmar.

        if mensaje_error:
        # Si hay un mensaje de error.
            
            texto_error = FUENTE.render(mensaje_error, True, (255, 0, 0))
            # Renderiza el mensaje de error en rojo.
            
            PANTALLA.blit(texto_error, (ANCHO//2 - texto_error.get_width()//2, ALTO//2 + 130))
            # Dibuja el mensaje de error centrado.

        for event in pygame.event.get():
        # Itera sobre todos los eventos de Pygame.
            
            if event.type == pygame.QUIT:
            # Si el usuario cierra la ventana.
                
                pygame.quit()
                # Cierra Pygame.
                sys.exit()
                # Sale del programa.

            res = input_usuario.manejar_evento(event)
            # Maneja los eventos para el campo de usuario.
            
            if res == "enter":
            # Si el usuario presiona Enter en el campo de usuario.
                
                input_password.activo = True
                # Activa el campo de contraseña.
                
                input_usuario.activo = False
                # Desactiva el campo de usuario.

            res = input_password.manejar_evento(event)
            # Maneja los eventos para el campo de contraseña.
            
            if res == "enter":
            # Si el usuario presiona Enter en el campo de contraseña.
                
                # Intentar confirmar
                if input_usuario.texto == "Luffy" and input_password.texto == "1234":
                # Verifica si el usuario y contraseña coinciden.
                    
                    return input_usuario.texto
                    # Retorna el nombre de usuario si las credenciales son correctas.
                
                else:
                # Si las credenciales son incorrectas.
                    
                    mensaje_error = "Usuario o contraseña incorrectos"
                    # Establece el mensaje de error.

            if event.type == pygame.MOUSEBUTTONDOWN:
            # Si el evento es un click del ratón.
                
                if boton_confirmar.esta_click(event.pos):
                # Si se clickea el botón de confirmar.
                    
                    if input_usuario.texto == "Luffy" and input_password.texto == "1234":
                    # Verifica las credenciales.
                        
                        return input_usuario.texto
                        # Retorna el nombre de usuario.
                    
                    else:
                    # Si las credenciales son incorrectas.
                        
                        mensaje_error = "Usuario o contraseña incorrectos"
                        # Establece el mensaje de error.

        pygame.display.flip()
        # Actualiza toda la pantalla para mostrar los cambios.
        
        RELOJ.tick(FPS)
        # Limita la velocidad de fotogramas a 60 FPS.

def pantalla_menu(usuario):
# Define la función para la pantalla del menú principal.

    botones = []
    # Inicializa una lista para almacenar los botones del menú.

    opciones = ["Jugar", "Opciones", "Créditos", "Salir"]
    # Define las opciones del menú.

    for i, texto in enumerate(opciones):
    # Itera sobre las opciones del menú.

        botones.append(Boton(ANCHO//2 - 100, 150 + i*70, 200, 50, texto))
        # Crea y añade un botón para cada opción, posicionándolos verticalmente.

    while True:
    # Bucle principal de la pantalla del menú.

        PANTALLA.fill(NEGRO)
        # Rellena la pantalla con color negro.

        titulo = FUENTE.render(f"Bienvenido, {usuario}", True, BLANCO)
        # Renderiza un mensaje de bienvenida con el nombre de usuario.

        PANTALLA.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 50))
        # Dibuja el mensaje de bienvenida.

        for boton in botones:
        # Itera sobre los botones del menú.

            boton.dibujar(PANTALLA)
            # Dibuja cada botón.

        for event in pygame.event.get():
        # Itera sobre los eventos.

            if event.type == pygame.QUIT:
            # Si el usuario cierra la ventana.

                pygame.quit()
                # Cierra Pygame.
                sys.exit()
                # Sale del programa.

            if event.type == pygame.MOUSEBUTTONDOWN:
            # Si se clickea el ratón.

                pos = event.pos
                # Obtiene la posición del click del ratón.

                for boton in botones:
                # Itera sobre los botones.

                    if boton.esta_click(pos):
                    # Si el botón fue clickeado.

                        if boton.texto == "Jugar":
                        # Si el botón es "Jugar".

                            return "jugar"
                            # Retorna la cadena "jugar".

                        elif boton.texto == "Opciones":
                        # Si el botón es "Opciones".

                            pantalla_de_opc()
                            # Llama a la función de la pantalla de opciones.

                        elif boton.texto == "Créditos":
                        # Si el botón es "Créditos".

                            pantalla_creditos()
                            # Llama a la función de la pantalla de créditos.

                        elif boton.texto == "Salir":
                        # Si el botón es "Salir".

                            pygame.quit()
                            # Cierra Pygame.
                            sys.exit()
                            # Sale del programa.

        pygame.display.flip()
        # Actualiza toda la pantalla.

        RELOJ.tick(FPS)
        # Limita los FPS.

def pantalla_creditos():
# Define la función para la pantalla de créditos.

    creditos = ["Benjamin Contreras", "Yordi Guarda", "Marcelo Compai", "Brayan Oyarzo", "Matias Carreño"]
    # Lista de nombres de los créditos.

    while True:
    # Bucle principal de la pantalla de créditos.

        PANTALLA.fill(NEGRO)
        # Rellena la pantalla con color negro.

        titulo = FUENTE.render("Créditos", True, BLANCO)
        # Renderiza el título "Créditos".

        PANTALLA.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 50))
        # Dibuja el título centrado.

        for i, nombre in enumerate(creditos):
        # Itera sobre la lista de créditos.

            texto = FUENTE.render(nombre, True, BLANCO)
            # Renderiza cada nombre.

            PANTALLA.blit(texto, (ANCHO//2 - texto.get_width()//2, 130 + i*40))
            # Dibuja cada nombre, espaciándolos verticalmente.

        # Botón para volver
        boton_volver = Boton(ANCHO//2 - 60, ALTO - 80, 120, 40, "Volver")
        # Crea un botón para volver al menú anterior.
        boton_volver.dibujar(PANTALLA)
        # Dibuja el botón de volver.

        for event in pygame.event.get():
        # Itera sobre los eventos.

            if event.type == pygame.QUIT:
            # Si el usuario cierra la ventana.

                pygame.quit()
                # Cierra Pygame.
                sys.exit()
                # Sale del programa.

            if event.type == pygame.MOUSEBUTTONDOWN:
            # Si se clickea el ratón.

                if boton_volver.esta_click(event.pos):
                # Si se clickea el botón de volver.

                    return
                    # Sale de la función (vuelve a la pantalla anterior).

        pygame.display.flip()
        # Actualiza toda la pantalla.

        RELOJ.tick(FPS)
        # Limita los FPS.

def pantalla_de_opc():
# Define la función para la pantalla de opciones del juego.

    global PANTALLA
    # Permite modificar la variable global PANTALLA para cambiar entre pantalla completa y ventana.

    opciones = ["Pantalla completa: No", "Ver estadísticas", "Volver al menú"]
    # Lista de opciones que se mostrarán en la pantalla (texto de los botones).

    fullscreen = False
    # Variable booleana que indica si está activa la pantalla completa.

    botones = []
    # Lista donde se almacenarán los objetos de tipo Boton.

    for i, texto in enumerate(opciones):
        # Itera sobre las opciones con sus índices para crear los botones.

        botones.append(Boton (ANCHO // 2 - 140, 200 + i * 80, 280, 50, texto))
        # Crea un botón con el texto correspondiente, espaciados verticalmente.

    while True:
        # Bucle principal de la pantalla de opciones.

        PANTALLA.fill (NEGRO)
        # Limpia la pantalla con color negro.

        titulo = FUENTE.render ("Opciones", True, BLANCO)
        # Renderiza el texto del título "Opciones".

        PANTALLA.blit (titulo, (ANCHO // 2 - titulo.get_width () // 2, 100))
        # Dibuja el título centrado horizontalmente en la parte superior.

        for i, boton in enumerate (botones):
            # Itera sobre todos los botones y los dibuja en pantalla.

            boton.dibujar (PANTALLA)
            # Dibuja el botón actual.

        for event in pygame.event.get():
            # Captura todos los eventos generados por el usuario.

            if event.type == pygame. QUIT:
                # Si el usuario cierra la ventana:

                pygame.quit()
                # Cierra Pygame.

                sys.exit()
                # Termina el programa completamente.

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Si el usuario hace clic con el mouse:

                pos = event.pos
                # Guarda la posición donde se hizo clic.

                if botones[0].esta_click (pos):
                    # Si el clic fue sobre el botón de pantalla completa:

                    fullscreen = not fullscreen
                    # Cambia el valor de fullscreen entre True y False (activa o desactiva pantalla completa).

                    if fullscreen:
                    # Si fullscreen es True:

                        PANTALLA = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN)
                        # Cambia la pantalla al modo pantalla completa.

                        botones[0].texto = "Pantalla completa: Sí"
                        # Actualiza el texto del botón para reflejar el estado actual.

                    else:
                    # Si fullscreen es False:

                        PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
                        # Cambia la pantalla al modo ventana.

                        botones[0].texto = "Pantalla completa: No"
                        # Actualiza el texto del botón para reflejar el estado actual.

                    globals()['PANTALLA'] = PANTALLA
                    # Actualiza la referencia global para que el nuevo modo de pantalla sea reconocido por todo el juego.

                elif botones[1].esta_click (pos):
                # Si se hace clic sobre el botón "Ver estadísticas":

                    jugador_fake = JugadorPVP (0, 0, AZUL, {})
                    # Crea una instancia falsa de jugador para mostrar estadísticas ficticias.

                    jugador_fake.nombre = "Test"
                    # Asigna un nombre de prueba.

                    jugador_fake.vida = 85
                    # Asigna una cantidad de vida ficticia.

                    jugador_fake.fuerza = 11
                    # Asigna una cantidad de fuerza ficticia.

                    jugador_fake.defensa = 6
                    # Asigna una cantidad de defensa ficticia.

                    jugador_fake.color = AZUL
                    # Asigna el color azul como color del jugador de prueba.

                    pantalla_estadisticas (jugador_fake)
                    # Llama a la pantalla de estadísticas pasando al jugador de prueba.

                    if fullscreen:
                        # Si se activó pantalla completa:

                        PANTALLA = pygame.display.set_mode ((ANCHO, ALTO), pygame.FULLSCREEN)
                        # Cambia a modo pantalla completa.

                    else:
                        # Si se desactivó pantalla completa:

                        PANTALLA = pygame.display.set_mode ((ANCHO, ALTO))
                        # Vuelve al modo ventana.

                    globals()['PANTALLA'] = PANTALLA
                    # Actualiza la referencia global para que los cambios tengan efecto en todo el juego.

                if botones[2].esta_click(pos):
                    # Si el clic fue sobre el botón "Volver al menú":

                    return
                    # Sale de la función, volviendo al menú principal.

        pygame.display.flip()
        # Actualiza la pantalla para mostrar todos los cambios visuales.

        RELOJ.tick(FPS)
        # Controla el ciclo de refresco del juego, limitando los FPS.

def pantalla_personalizar(jugador):
# Define la función para la pantalla de personalización del jugador.

    input_nombre = InputBox(ANCHO//2 - 100, 150, 200, 35, jugador.nombre)
    # Crea un campo de entrada para el nombre del jugador, con su nombre actual.

    # Estadísticas iniciales
    vida = jugador.vida
    # Obtiene la vida actual del jugador.
    fuerza = jugador.fuerza
    # Obtiene la fuerza actual del jugador.
    defensa = jugador.defensa
    # Obtiene la defensa actual del jugador.

    puntos = 10  # puntos para distribuir
    # Define la cantidad de puntos que el jugador tiene para distribuir.

    botones_mas = []
    # Lista para los botones de aumentar estadísticas.
    botones_menos = []
    # Lista para los botones de disminuir estadísticas.

    def crear_botones_stat(y):
    # Función auxiliar para crear un par de botones (+ y -) para una estadística.

        return (Boton(ANCHO//2 + 110, y, 30, 30, "+"), Boton(ANCHO//2 + 150, y, 30, 30, "-"))
        # Retorna una tupla con los botones de "+" y "-".

    def pantalla_selector_color():
    # Define la función para mostrar una pantalla donde el jugador puede elegir su color.

        # Lista de colores disponibles con nombres
        colores = [
   
        ("Rojo", ROJO),
   
        ("Azul", AZUL),
   
        ("Verde", VERDE),
   
        ("Amarillo", (255, 255, 0)),
   
        ("Morado", (128, 0, 128)),
   
        ]
        # Cada color está representado por un nombre (texto) y su valor RGB.

        # Crear botones de colores con su texto
        botones_color = []
        # Lista que almacenará los botones de selección de color.

        for i, (nombre, color) in enumerate(colores):
            # Itera sobre los colores disponibles con su índice.

            boton = Boton(
   
                ANCHO//2 - 100,    # posición horizontal centrada
   
                150 + i*70,        # posición vertical con separación entre botones
   
                200,               # ancho del botón
   
                50,                # alto del botón
   
                nombre             # texto que muestra el nombre del color
   
            )
   
            botones_color.append((boton, color))
            # Añade el botón y su color asociado a la lista.
        boton_personalizado = Boton (ANCHO // 2 - 100, 150 + len(colores) * 70, 200, 50, "Color personalizado")

        while True:
            # Bucle principal de la pantalla de selección de color.

            PANTALLA.fill(NEGRO)
            # Rellena toda la pantalla de negro.

            # Título de la pantalla
            titulo = FUENTE.render("Selecciona tu color", True, BLANCO)
            # Renderiza el título principal en blanco.

            PANTALLA.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 50))
            # Dibuja el título centrado horizontalmente.

            # Dibujar cada botón de color
            for boton, color in botones_color:
   
                pygame.draw.rect(PANTALLA, color, boton.rect)  # relleno del color
                # Dibuja el botón con el color de fondo correspondiente.

                pygame.draw.rect(PANTALLA, BLANCO, boton.rect, 2)  # borde blanco
                # Dibuja el borde blanco alrededor del botón.

                texto = FUENTE.render(boton.texto, True, NEGRO if sum(color) > 400 else BLANCO)
                # Renderiza el nombre del color, elige negro o blanco según el contraste.

                PANTALLA.blit(texto, (
   
                    boton.rect.x + (boton.rect.w - texto.get_width())//2,
   
                    boton.rect.y + (boton.rect.h - texto.get_height())//2
   
                ))
                # Dibuja el texto centrado dentro del botón.

            # Manejar eventos del usuario
            for event in pygame.event.get():
 
                if event.type == pygame.QUIT:
                    # Si el usuario cierra la ventana.

                    pygame.quit()
     
                    sys.exit()
     
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Si se hace clic con el mouse.

                    pos = event.pos
                    # Obtiene la posición del clic.

                    if boton_personalizado.esta_click (pos):

                        return pantalla_color_personalizado()

                    for boton, color in botones_color:
     
                        if boton.esta_click(pos):
                        # Si el botón fue clickeado.

                            return color  # Retorna el color elegido
                            # Retorna el color seleccionado y termina la función.

            boton_personalizado.dibujar(PANTALLA)

            pygame.display.flip()
            # Actualiza la pantalla para mostrar todos los cambios.

            RELOJ.tick(FPS)
            # Controla los FPS de la pantalla de selección.

    def pantalla_color_personalizado ():
    # Define la función que permite al jugador introducir manualmente un color personalizado mediante valores RGB.

        input_r = InputBox (ANCHO // 2 - 150, 200, 80, 35)
        # Crea un campo de entrada para el valor R (rojo), ubicado a la izquierda del centro.

        input_g = InputBox (ANCHO // 2 - 40, 200, 80, 35)
        # Crea un campo de entrada para el valor G (verde), centrado horizontalmente.

        input_b = InputBox (ANCHO // 2 + 70, 200, 80, 35)
        # Crea un campo de entrada para el valor B (azul), ubicado a la derecha del centro.

        boton_confi = Boton (ANCHO // 2 - 60, 280, 120, 40, "Confirmar")
        # Crea un botón con el texto "Confirmar" para aceptar los valores RGB ingresados.

        mensaje_error = ""
        # Inicializa una variable para mostrar mensajes de error si los valores no son válidos.

        while True:
        # Bucle principal de la pantalla.

            PANTALLA.fill (NEGRO)
            # Limpia la pantalla rellenándola de color negro.

            titulo = FUENTE.render ("Introduce valores RGB (0 - 255)", True, BLANCO)
            # Renderiza el título explicativo.

            PANTALLA.blit (titulo, (ANCHO // 2 - titulo.get_width () // 2, 130))
            # Dibuja el título centrado en la parte superior de la pantalla.

            for input_box in [input_r, input_g, input_b]:
            # Itera sobre los tres campos de entrada.

                input_box.dibujar (PANTALLA)
                # Dibuja cada campo de entrada en pantalla.

            etiquetas = ["R", "G", "B"]
            # Lista con las etiquetas de los canales de color.

            for i, label, in enumerate(etiquetas):
            # Itera sobre las etiquetas junto con su índice.

                texto = FUENTE_PEQUE.render (label, True, BLANCO)
                # Renderiza cada etiqueta con fuente pequeña.

                PANTALLA.blit (texto, (ANCHO // 2 - 150 + i * 110 + 30, 180))
                # Dibuja cada etiqueta encima del campo correspondiente (R, G, B).

            boton_confi.dibujar(PANTALLA)
            # Dibuja el botón "Confirmar" en pantalla.

            if mensaje_error:
            # Si hay un mensaje de error que mostrar:

                error_texto = FUENTE_PEQUE.render (mensaje_error, True, ROJO)
                # Renderiza el mensaje en color rojo.

                PANTALLA.blit (error_texto, (ANCHO // 2 - error_texto.get_width () // 2, 330))
                # Dibuja el mensaje de error centrado horizontalmente.

            for event in pygame.event.get ():
            # Itera sobre todos los eventos de Pygame.

                if event.type == pygame.QUIT:
                # Si el usuario cierra la ventana:

                    pygame.quit()  
                    # Cierra Pygame.

                    sys.exit()
                    # Termina el programa.

                for box in [input_r, input_g, input_b]:
                # Itera sobre los campos de entrada para pasarles el evento.

                    box.manejar_evento (event)
                    # Actualiza el campo con el evento actual.

                if event.type == pygame.MOUSEBUTTONDOWN:
                # Si se hace clic con el mouse:

                    if boton_confi.esta_click (event.pos):
                    # Si el botón "Confirmar" fue clickeado:

                        try:
                        # Intenta ejecutar el bloque de código dentro del try:

                            r = int (input_r.texto)

                            g = int (input_g.texto)

                            b = int (input_b.texto)
                            # Intenta convertir los valores ingresados en enteros.

                            if all(0 <= val <= 255 for val in (r, g, b)):
                            # Verifica que todos los valores estén en el rango válido de 0 a 255.

                                return (r, g, b)
                                # Si todo es correcto, retorna el color como una tupla RGB.

                            else:

                                mensaje_error = "Valores deben estar entre 0 y 255"
                                # Muestra un mensaje si los valores están fuera de rango.

                        except:
                        # Si ocurre una excepción (por ejemplo, si se ingresó texto no numérico):

                            mensaje_error = "Por favor ingresa número validos"
                            # Muestra un mensaje si los valores no son numéricos válidos.

            pygame.display.flip ()
            # Actualiza la pantalla para mostrar todos los cambios realizados.

            RELOJ.tick (FPS)
            # Limita la tasa de refresco para que no sobrepase los FPS definidos.

    # Llamada a la función desde pantalla_personalizar()
    color_elegido = pantalla_selector_color()
    # Llama a la función y guarda el color elegido por el jugador.

    jugador.color = color_elegido
    # Asigna el color seleccionado al jugador personalizado.

    botones_mas.append(crear_botones_stat(220)[0])
    # Añade el botón "+" para la vida.

    botones_menos.append(crear_botones_stat(220)[1])
    # Añade el botón "-" para la vida.

    botones_mas.append(crear_botones_stat(270)[0])
    # Añade el botón "+" para la fuerza.

    botones_menos.append(crear_botones_stat(270)[1])
    # Añade el botón "-" para la fuerza.

    botones_mas.append(crear_botones_stat(320)[0])
    # Añade el botón "+" para la defensa.

    botones_menos.append(crear_botones_stat(320)[1])
    # Añade el botón "-" para la defensa.

    while True:
    # Bucle principal de la pantalla de personalización.

        PANTALLA.fill(NEGRO)
        # Rellena la pantalla con color negro.

        titulo = FUENTE.render("Personaliza tu personaje", True, BLANCO)
        # Renderiza el título de la pantalla.
        PANTALLA.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 80))
        # Dibuja el título.

        etiqueta_nombre = FUENTE.render("Nombre:", True, BLANCO)
        # Renderiza la etiqueta "Nombre:".

        PANTALLA.blit(etiqueta_nombre, (ANCHO//2 - 180, 150))
        # Dibuja la etiqueta de nombre.
        
        input_nombre.dibujar(PANTALLA)
        # Dibuja el campo de entrada de nombre.

        etiqueta_vida = FUENTE.render(f"Vida: {vida}", True, ROJO)
        # Renderiza la etiqueta de vida con el valor actual.

        etiqueta_fuerza = FUENTE.render(f"Fuerza: {fuerza}", True, AZUL)
        # Renderiza la etiqueta de fuerza.

        etiqueta_defensa = FUENTE.render(f"Defensa: {defensa}", True, VERDE)
        # Renderiza la etiqueta de defensa.

        PANTALLA.blit(etiqueta_vida, (ANCHO//2 - 180, 220))
        # Dibuja la etiqueta de vida.

        PANTALLA.blit(etiqueta_fuerza, (ANCHO//2 - 180, 270))
        # Dibuja la etiqueta de fuerza.

        PANTALLA.blit(etiqueta_defensa, (ANCHO//2 - 180, 320))
        # Dibuja la etiqueta de defensa.

        for b in botones_mas + botones_menos:
        # Itera sobre todos los botones de estadísticas.

            b.dibujar(PANTALLA)
            # Dibuja cada botón.

        # Mostrar puntos restantes
        puntos_texto = FUENTE.render(f"Puntos restantes: {puntos}", True, BLANCO)
        # Renderiza el texto de puntos restantes.
        PANTALLA.blit(puntos_texto, (ANCHO//2 - 70, 370))
        # Dibuja los puntos restantes.

        boton_listo = Boton(ANCHO//2 - 60, 420, 120, 40, "Listo")
        # Crea un botón "Listo".
        boton_listo.dibujar(PANTALLA)
        # Dibuja el botón "Listo".

        for event in pygame.event.get():
        # Itera sobre los eventos.

            if event.type == pygame.QUIT:
            # Si el usuario cierra la ventana.

                pygame.quit()
                # Cierra Pygame.
                sys.exit()
                # Sale del programa.

            res = input_nombre.manejar_evento(event)
            # Maneja los eventos para el campo de nombre.

            if event.type == pygame.MOUSEBUTTONDOWN:
            # Si se clickea el ratón.

                pos = event.pos
                # Obtiene la posición del click.

                #Vida
                if botones_mas[0].esta_click(pos) and puntos > 0:
                # Si se clickea el botón "+" de vida y quedan puntos.

                    vida += 1
                    # Aumenta la vida.

                    puntos -= 1
                    # Decrementa los puntos.

                # - Vida
                if botones_menos[0].esta_click(pos) and vida > 1:
                # Si se clickea el botón "-" de vida y la vida es mayor a 1.

                    vida -= 1
                    # Disminuye la vida.

                    puntos += 1
                    # Aumenta los puntos.

                # + Fuerza
                if botones_mas[1].esta_click(pos) and puntos > 0:
                # Si se clickea el botón "+" de fuerza y quedan puntos.

                    fuerza += 1
                    # Aumenta la fuerza.

                    puntos -= 1
                    # Decrementa los puntos.

                # - Fuerza
                if botones_menos[1].esta_click(pos) and fuerza > 1:
                # Si se clickea el botón "-" de fuerza y la fuerza es mayor a 1.

                    fuerza -= 1
                    # Disminuye la fuerza.

                    puntos += 1
                    # Aumenta los puntos.

                # + Defensa
                if botones_mas[2].esta_click(pos) and puntos > 0:
                # Si se clickea el botón "+" de defensa y quedan puntos.

                    defensa += 1
                    # Aumenta la defensa.

                    puntos -= 1
                    # Decrementa los puntos.

                # - Defensa
                if botones_menos[2].esta_click(pos) and defensa > 1:
                # Si se clickea el botón "-" de defensa y la defensa es mayor a 1.

                    defensa -= 1
                    # Disminuye la defensa.

                    puntos += 1
                    # Aumenta los puntos.

                if boton_listo.esta_click(pos):
                # Si se clickea el botón "Listo".

                    jugador.vida = vida
                    # Asigna la vida personalizada al jugador.

                    jugador.fuerza = fuerza
                    # Asigna la fuerza personalizada al jugador.

                    jugador.defensa = defensa
                    # Asigna la defensa personalizada al jugador.

                    jugador.nombre = input_nombre.texto if input_nombre.texto.strip() != "" else "Jugador"
                    # Asigna el nombre ingresado al jugador, o "Jugador" si el campo está vacío.

                    return
                    # Sale de la función.

        pygame.display.flip()
        # Actualiza toda la pantalla.

        RELOJ.tick(FPS)
        # Limita los FPS.

def pantalla_seleccionar_mapa():
# Define la función para la pantalla de selección de mapa.

    botones_mapa = []
    # Lista para almacenar los botones de los mapas.

    botones_mapa.append(Boton(ANCHO//4 - 100, ALTO//2, 180, 60, "Mapa 1"))
    # Crea el botón para "Mapa 1".

    botones_mapa.append(Boton(3*ANCHO//4 - 100, ALTO//2, 180, 60, "Mapa 2"))
    # Crea el botón para "Mapa 2".

    while True:
    # Bucle principal de la pantalla de selección de mapa.

        PANTALLA.fill(NEGRO)
        # Rellena la pantalla con color negro.

        titulo = FUENTE.render("Selecciona un mapa", True, BLANCO)
        # Renderiza el título.

        PANTALLA.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 150))
        # Dibuja el título.

        for boton in botones_mapa:
        # Itera sobre los botones de mapa.

            boton.dibujar(PANTALLA)
            # Dibuja cada botón.

        for event in pygame.event.get():
        # Itera sobre los eventos.

            if event.type == pygame.QUIT:
            # Si el usuario cierra la ventana.

                pygame.quit()
                # Cierra Pygame.
                sys.exit()
                # Sale del programa.

            if event.type == pygame.MOUSEBUTTONDOWN:
            # Si se clickea el ratón.

                pos = event.pos
                # Obtiene la posición del click.

                if botones_mapa[0].esta_click(pos):
                # Si se clickea el "Mapa 1".

                    return 1
                    # Retorna 1 para indicar el mapa 1.

                if botones_mapa[1].esta_click(pos):
                # Si se clickea el "Mapa 2".

                    return 2
                    # Retorna 2 para indicar el mapa 2.

        pygame.display.flip()
        # Actualiza toda la pantalla.

        RELOJ.tick(FPS)
        # Limita los FPS.

def pantalla_juego(jugador, mapa_num):
# Define la función principal de la pantalla de juego.

    # Crear jugadores PVP
    jugador1 = JugadorPVP(100, ALTO//4, AZUL, {'izquierda':pygame.K_a, 'derecha':pygame.K_d,
                                                'arriba':pygame.K_w, 'abajo':pygame.K_s, 'disparo':pygame.K_f, 'dash': pygame.K_LSHIFT})
    # Crea el Jugador 1 con su posición inicial, color azul y teclas de control.

    jugador2 = JugadorPVP(100, ALTO//4*3, ROJO, {'izquierda':pygame.K_LEFT, 'derecha':pygame.K_RIGHT,
                                                 'arriba':pygame.K_UP, 'abajo':pygame.K_DOWN, 'disparo':pygame.K_k, 'dash': pygame.K_RCTRL})
    # Crea el Jugador 2 con su posición inicial, color rojo y teclas de control.

    jugador1.nombre = jugador.nombre
    # Asigna el nombre personalizado del jugador de la pantalla de personalización al jugador 1.
    jugador1.vida = jugador.vida
    # Asigna la vida personalizada.
    jugador1.fuerza = jugador.fuerza
    # Asigna la fuerza personalizada.
    jugador1.defensa = jugador.defensa
    # Asigna la defensa personalizada.
    jugador1.color = jugador.color

    jugador2.nombre = "Jugador2"  # fijo para jugador 2
    # Establece el nombre fijo para el jugador 2.

    # Variables mapa 2
    mapa_colisiones = []
    # Inicializa una lista vacía para los obstáculos del mapa.

    bicicleta = None
    # Inicializa la bicicleta a None.

    if mapa_num == 2:
    # Si se seleccionó el mapa 2.

        # Crear obstáculos
        mapa_colisiones = [
        # Define una lista de objetos Rect que representarán los obstáculos.
            pygame.Rect(300, 100, 50, 400),
            # Primer obstáculo.
            pygame.Rect(600, 150, 50, 300)
            # Segundo obstáculo.
        ]

        bicicleta = Bicicleta(400, 300)
        # Crea una instancia de Bicicleta en una posición específica.

    while True:
    # Bucle principal del juego.

        RELOJ.tick(FPS)
        # Limita la velocidad de fotogramas del juego.

        for event in pygame.event.get():
        # Itera sobre los eventos.

            if event.type == pygame.QUIT:
            # Si el usuario cierra la ventana.

                pygame.quit()
                # Cierra Pygame.
                sys.exit()
                # Sale del programa.

            if event.type == pygame.KEYDOWN:
            # Si se presiona una tecla.

                if event.key == jugador1.teclas.get('dash'):
                # Si la tecla presionada corresponde al dash del jugador 1 (por ejemplo, LSHIFT).

                    jugador1.dash()
                    # Llama al método dash() del jugador 1, el cual lo desplaza rápidamente en la dirección actual
                    # si ha pasado suficiente tiempo desde el último dash (cooldown).

                if event.key == jugador2.teclas.get('dash'):
                # Si la tecla presionada corresponde al dash del jugador 2 (por ejemplo, RCTRL).

                    jugador2.dash()
                    # Ejecuta el desplazamiento rápido del jugador 2, siempre que respete el cooldown configurado.
                if event.key == jugador1.teclas['disparo']:
                # Si la tecla de disparo del jugador 1 es presionada.

                    jugador1.disparar()
                    # El jugador 1 dispara.

                if event.key == jugador2.teclas['disparo']:
                # Si la tecla de disparo del jugador 2 es presionada.

                    jugador2.disparar()
                    # El jugador 2 dispara.

                if event.key == pygame.K_ESCAPE:
                # Si se presiona la tecla ESC.

                    return
                    # Sale de la función (vuelve al menú principal).

                # Montar/desmontar bicicleta jugador1
                if event.key == pygame.K_e and mapa_num == 2:
                # Si la tecla 'E' es presionada y el mapa es el 2.

                    if jugador1.en_bicicleta:
                    # Si el jugador 1 ya está en bicicleta.

                        jugador1.desmontar_bicicleta()
                        # Desmonta la bicicleta.

                    else:
                    # Si el jugador 1 no está en bicicleta.

                        jugador1.montar_bicicleta(bicicleta)
                        # Intenta montar la bicicleta.

                # Montar/desmontar bicicleta jugador2
                if event.key == pygame.K_RETURN and mapa_num == 2:
                # Si la tecla ENTER es presionada y el mapa es el 2.

                    if jugador2.en_bicicleta:
                    # Si el jugador 2 ya está en bicicleta.

                        jugador2.desmontar_bicicleta()
                        # Desmonta la bicicleta.

                    else:
                    # Si el jugador 2 no está en bicicleta.

                        jugador2.montar_bicicleta(bicicleta)
                        # Intenta montar la bicicleta.

        keys = pygame.key.get_pressed()
        # Obtiene el estado actual de todas las teclas presionadas.

        jugador1.manejar_eventos(keys, mapa_colisiones)
        # Maneja los eventos de movimiento para el jugador 1.

        jugador2.manejar_eventos(keys, mapa_colisiones)
        # Maneja los eventos de movimiento para el jugador 2.

        jugador1.actualizar_balas(mapa_colisiones, jugador2)
        # Actualiza las balas del jugador 1 y maneja sus colisiones.

        jugador2.actualizar_balas(mapa_colisiones, jugador1)
        # Actualiza las balas del jugador 2.

        jugador1.regenerar_vida()
        # Llama al método de regeneración de vida del jugador 1.
        # Si han pasado más de 3 segundos desde que recibió daño y se cumple el cooldown,
        # se le restaura lentamente parte de su vida.

        jugador2.regenerar_vida()
        # Llama al método de regeneración de vida del jugador 2.
        # Este método funciona igual que el del jugador 1, evaluando si puede regenerar
        # 0.5 puntos de vida cada 0.5 segundos si no ha sido dañado recientemente.

        # Verificar si un jugador fue eliminado
        if jugador1.vida <= 0:
        # Si la vida del jugador 1 es menor o igual a 0, se considera que ha muerto.

            jugador1.vidas_restantes -= 1
            # Se reduce en 1 el contador de vidas restantes del jugador 1.

            if jugador1.vidas_restantes > 0:
            # Si aún le quedan vidas para reaparecer.

                jugador1.vida = 100
                # Se restaura su vida a 100 puntos.

                jugador1.rect.topleft = (100, ALTO // 4)
                # Se reposiciona al jugador 1 en su punto de inicio.

                jugador1.balas.clear()
                # Se eliminan todas las balas disparadas por el jugador 1.

                jugador1.desmontar_bicicleta()
                # Asegura que reaparezca sin estar montado en bicicleta.

            else:
            # Si ya no le quedan vidas disponibles.

                pantalla_victoria (jugador2.nombre)
                # Muestra la pantalla de victoria con el nombre del jugador 2.

                return
                # Termina la ejecución del juego (sale de pantalla_juego()).

        # Verificar si el jugador 2 fue eliminado
        if jugador2.vida <= 0:
        # Si la vida del jugador 2 es menor o igual a 0.
             
            jugador2.vidas_restantes -= 1
            # Resta una vida disponible al jugador 2.

            if jugador2.vidas_restantes > 0:
            # Si aún le quedan reapariciones.

                jugador2.vida = 100
                # Se le devuelve la vida completa.

                jugador2.rect.topleft = (100, ALTO // 4 * 3)
                # Se coloca nuevamente en su posición inicial.

                jugador2.balas.clear()
                # Limpia todas las balas que haya disparado.

                jugador2.desmontar_bicicleta()
                # Se asegura de que no reaparezca sobre la bicicleta.

            else:
            # Si ya no tiene vidas restantes.

                pantalla_victoria (jugador1.nombre)
                # Se muestra la pantalla de victoria con el nombre del jugador 1.

                return
                # Termina la función y vuelve al menú principal.

        # Dibujar
        if mapa_num == 1:
        # Si el mapa es el 1.

            PANTALLA.fill(NEGRO)  # mapa 1 en blanco
            # Rellena la pantalla con negro (parece un error en el comentario, debería ser sin obstáculos).

        else:
        # Si el mapa es el 2.

            PANTALLA.fill(NEGRO)
            # Rellena la pantalla con negro.

            # Obstáculos en negro
            for obstaculo in mapa_colisiones:
            # Itera sobre los obstáculos del mapa.

                pygame.draw.rect(PANTALLA, BLANCO, obstaculo)
                # Dibuja cada obstáculo como un rectángulo blanco.

        if bicicleta:
            # Verifica si el objeto bicicleta existe (no es None).
            # Esto evita errores si el mapa actual no tiene bicicleta disponible.

            bicicleta.dibujar(PANTALLA)
            # Llama al método para dibujar la bicicleta en pantalla.
            # Se renderiza su sprite en la posición actual sobre la superficie PANTALLA.

        # Dibujar jugadores y bicicleta
        jugador1.dibujar(PANTALLA)
        # Dibuja al jugador 1 (y su bicicleta si está montado).
        jugador2.dibujar(PANTALLA)
        # Dibuja al jugador 2 (y su bicicleta si está montado).

        vidas1 = FUENTE_PEQUE.render (f'vidas restantes: {jugador1.vidas_restantes}', True, BLANCO)
        # Renderiza el texto que muestra cuántas vidas le quedan al jugador 1, usando una fuente pequeña y color blanco.

        PANTALLA.blit (vidas1, (jugador1.rect.x, jugador1.rect.y - 40))
        # Dibuja el texto anterior en pantalla, justo sobre la cabeza del jugador 1 (40 píxeles más arriba de su posición).

        vidas2 = FUENTE_PEQUE.render (f'vidas restantes: {jugador2.vidas_restantes}', True, BLANCO)
        # Renderiza el texto que muestra cuántas vidas le quedan al jugador 2, también en color blanco.

        PANTALLA.blit (vidas2, (jugador2.rect.x, jugador2.rect.y - 40))
        # Dibuja el texto sobre la cabeza del jugador 2, en su posición respectiva.

        # Indicaciones para montar bici
        if mapa_num == 2:
        # Si el mapa es el 2.

            info1 = FUENTE_PEQUE.render("Jugador1: E para montar/desmontar bici", True, BLANCO)
            # Renderiza la instrucción para el jugador 1.

            info2 = FUENTE_PEQUE.render("Jugador2: ENTER para montar/desmontar bici", True, BLANCO)
            # Renderiza la instrucción para el jugador 2.

            PANTALLA.blit(info1, (10, ALTO - 50))
            # Dibuja la instrucción para el jugador 1.

            PANTALLA.blit(info2, (10, ALTO - 30))
            # Dibuja la instrucción para el jugador 2.

        pygame.display.flip()
        # Actualiza toda la pantalla para mostrar los elementos dibujados.

def pantalla_victoria(nombre_ganador):
# Define la función para mostrar la pantalla de victoria cuando un jugador gana.
# Toma como argumento el nombre del jugador ganador (nombre_ganador).
    
    boton_volver = Boton(ANCHO//2 - 80, ALTO//2 + 60, 160, 50, "Volver al menú")
    # Crea un botón centrado en la pantalla que permite volver al menú principal.

    while True:
    # Bucle principal de la pantalla de victoria.
    
        PANTALLA.fill(NEGRO)
        # Rellena toda la pantalla con color negro.

        titulo = FUENTE.render(f"¡{nombre_ganador} ha ganado!", True, VERDE)
        # Renderiza el texto de victoria con el nombre del jugador ganador en color verde.
    
        PANTALLA.blit(titulo, (ANCHO//2 - titulo.get_width()//2, ALTO//2 - 60))
        # Dibuja el texto de victoria centrado horizontalmente en la pantalla.

        boton_volver.dibujar(PANTALLA)
        # Dibuja el botón de "Volver al menú" en la pantalla.

        for event in pygame.event.get():
        # Itera sobre todos los eventos de Pygame.
    
            if event.type == pygame.QUIT:
            # Si el usuario intenta cerrar la ventana.
    
                pygame.quit()
                # Finaliza la ejecución de Pygame.
    
                sys.exit()
                # Cierra completamente el programa.

            if event.type == pygame.MOUSEBUTTONDOWN:
            # Si se detecta un clic del ratón.
    
                if boton_volver.esta_click(event.pos):
                # Verifica si se hizo clic sobre el botón de volver.
    
                    return  # vuelve al menú
                    # Sale de la función para regresar al menú principal.

        pygame.display.flip()
        # Actualiza la pantalla con todos los cambios realizados (botón y texto).
    
        RELOJ.tick(FPS)
        # Limita la velocidad de actualización de la pantalla a los FPS definidos.

def pantalla_estadisticas (jugador):
# Define la función que muestra una ventana con las estadísticas de un jugador dado.

    global PANTALLA
    # Se accede a la variable global PANTALLA para poder modificarla temporalmente.

    ancho_est = 600

    alto_est = 400
    # Define el tamaño de la nueva ventana donde se mostrarán las estadísticas.

    original_caption = pygame.display.get_caption ()
    # Guarda el título actual de la ventana para poder restaurarlo después.

    original_pantalla = PANTALLA
    # Guarda la superficie original de la pantalla para poder volver a ella al salir de esta función.

    estadisticas_pantalla = pygame.display.set_mode((ancho_est, alto_est))
    # Cambia el tamaño de la ventana al de la pantalla de estadísticas.

    pygame.display.set_caption ("Estadísticas del jugador")
    # Cambia el título de la ventana temporalmente.

    globals () ["PANTALLA"] = estadisticas_pantalla
    # Actualiza la variable global PANTALLA con la nueva superficie de estadísticas.

    boton_volver = Boton (ANCHO // 2 - 80, ALTO - 100, 160, 50, "Volver")
    # Crea un botón para volver a la pantalla anterior.

    while True:
    # Bucle principal de la pantalla de estadísticas.

        PANTALLA.fill (NEGRO)
        # Limpia la pantalla con color negro.

        titulo = FUENTE.render ("Estadísticas del jugador", True, BLANCO)
        # Renderiza el título de la pantalla.

        PANTALLA.blit (titulo, (ancho_est // 2 - titulo.get_width () // 2, 50))
        # Dibuja el título centrado en la parte superior.

        stats = [

            f"Nombre: {jugador.nombre}",
            f"Vida: {jugador.vida}",
            f"Fuerza: {jugador.fuerza}",
            f"Defensa: {jugador.defensa}",
            "Color:"

        ]
        # Crea una lista con las estadísticas a mostrar en pantalla.

        for i, texto in enumerate (stats):
        # Itera sobre cada estadística para dibujarla.

            render = FUENTE.render (texto, True, BLANCO)
            # Renderiza el texto de la estadística.

            PANTALLA.blit (render, (ancho_est // 2 - 100, 150 + i * 40))
            # Dibuja el texto en pantalla, con espaciado vertical entre cada línea.

        pygame.draw.rect (PANTALLA, jugador.color, pygame.Rect (ancho_est // 2 + 60, 150 + 4 * 40, 40, 40))
        # Dibuja un rectángulo del color del jugador, representando visualmente su color.

        pygame.draw.rect (PANTALLA, BLANCO, pygame.Rect (ancho_est // 2 + 60, 150 + 4 * 40, 40, 40), 2)
        # Dibuja un borde blanco alrededor del rectángulo de color.

        boton_volver.dibujar (PANTALLA)
        # Dibuja el botón de "Volver" en pantalla.

        for event in pygame.event.get ():
        # Itera sobre los eventos de Pygame.

            if event.type == pygame.QUIT:
            # Si el usuario cierra la ventana:

                PANTALLA = pygame.display.set_mode ((ANCHO, ALTO))
                # Restaura el tamaño original de la pantalla.

                pygame.display.set_caption (original_caption[0])
                # Restaura el título original de la ventana.

                globals ()["PANTALLA"] = PANTALLA
                # Actualiza la referencia global de PANTALLA.

                return
                # Sale de la función.

            if event.type == pygame.MOUSEBUTTONDOWN:
            # Si se hace clic con el mouse:

                if boton_volver.esta_click(event.pos):
                # Si se hace clic en el botón "Volver":

                    PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
                    # Restaura el tamaño original de la pantalla.

                    pygame.display.set_caption(original_caption[0])
                    # Restaura el título original de la ventana.

                    globals ()["PANTALLA"] = PANTALLA
                    # Actualiza la referencia global de PANTALLA.

                    return 
                    # Sale de la función.
                
        pygame.display.flip ()
        # Actualiza la pantalla con todos los elementos dibujados.

        RELOJ.tick (FPS)
        # Controla la velocidad de refresco de la pantalla.

def main():
# Define la función principal del juego que orquesta las pantallas.
    
    usuario = pantalla_inicio_sesion()
    # Llama a la pantalla de inicio de sesión y almacena el nombre de usuario retornado.
    
    while True:
    # Bucle principal del juego después del inicio de sesión.
        
        opcion = pantalla_menu(usuario)
        # Llama a la pantalla del menú y obtiene la opción seleccionada por el usuario.
        
        if opcion == "jugar":
        # Si la opción seleccionada es "jugar".

            jugador = JugadorPVP(0, 0, AZUL, {})
            # Crea una instancia de JugadorPVP (se usará para la personalización y luego para el juego).
            
            pantalla_personalizar(jugador)
            # Llama a la pantalla de personalización del jugador.
            
            mapa = pantalla_seleccionar_mapa()
            # Llama a la pantalla de selección de mapa y almacena el número de mapa.
            
            pantalla_juego(jugador, mapa)
            # Llama a la pantalla de juego, pasando el jugador personalizado y el mapa seleccionado.
        
        elif opcion == "opciones":
        # Si la opción seleccionada es "opciones".
            
            pass
            # Actualmente no hace nada (se podría implementar una pantalla de opciones aquí).

if __name__ == "__main__":
# Bloque que asegura que el código dentro solo se ejecute cuando el script se corre directamente.
    
    main()
    # Llama a la función principal del juego para iniciarlo.