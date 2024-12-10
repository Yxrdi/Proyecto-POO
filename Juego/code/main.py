import pygame, sys  # Importa las bibliotecas pygame (para el juego) y sys (para el sistema operativo)
from settings import *  # Importa todas las configuraciones de settings.py
from level import Level  # Importa la clase Level desde el archivo level.py

class Game:  # Define la clase Game, que gestiona el ciclo del juego
    def __init__(self):  # Constructor de la clase
        # general setup
        pygame.init()  # Inicializa todos los módulos de Pygame
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))  # Crea la ventana del juego con el tamaño especificado en settings
        pygame.display.set_caption('Juego')  # Establece el título de la ventana
        self.clock = pygame.time.Clock()  # Crea un reloj para controlar los FPS

        self.level = Level()  # Crea una instancia del nivel (probablemente contiene la lógica del juego)

        # sound
        main_sound = pygame.mixer.Sound('../audio/main.ogg')  # Carga el archivo de sonido 'main.ogg'
        main_sound.set_volume(0.5)  # Establece el volumen del sonido a la mitad (50%)
        main_sound.play(loops=-1)  # Reproduce el sonido en bucle infinito

    def run(self):  # Método principal que ejecuta el bucle del juego
        while True:  # Bucle infinito del juego
            for event in pygame.event.get():  # Recorre todos los eventos generados por Pygame
                if event.type == pygame.QUIT:  # Si el evento es el cierre de la ventana
                    pygame.quit()  # Finaliza todos los módulos de Pygame
                    sys.exit()  # Termina el programa completamente
                if event.type == pygame.KEYDOWN:  # Si el evento es una tecla presionada
                    if event.key == pygame.K_m:  # Si la tecla presionada es 'M'
                        self.level.toggle_menu()  # Llama al método toggle_menu() en la instancia de Level

            self.screen.fill(WATER_COLOR)  # Rellena la pantalla con el color de fondo definido como WATER_COLOR
            self.level.run()  # Llama al método run() de la instancia de Level (para actualizar la lógica del nivel)
            pygame.display.update()  # Actualiza la pantalla para reflejar los cambios
            self.clock.tick(FPS)  # Controla la velocidad del juego según el FPS definido en settings.py

if __name__ == '__main__':  # Si el archivo se ejecuta directamente (no se importa como módulo)
    game = Game()  # Crea una nueva instancia de la clase Game
    game.run()  # Inicia el bucle principal del juego
