import pygame  # Importa la biblioteca Pygame para trabajar con gráficos y multimedia
pygame.init()  # Inicializa todos los módulos de Pygame
font = pygame.font.Font(None, 30)  # Crea un objeto de fuente para renderizar texto con tamaño 30 píxeles

def debug(info, y=10, x=10):  # Define la función debug, que toma texto (info) y coordenadas opcionales (x, y)
    display_surface = pygame.display.get_surface()  # Obtiene la superficie de la ventana donde se dibujará el contenido
    debug_surf = font.render(str(info), True, 'White')  # Crea una superficie con el texto de 'info' en color blanco y suavizado
    debug_rect = debug_surf.get_rect(topleft=(x, y))  # Obtiene el rectángulo del texto para posicionarlo en las coordenadas (x, y)
    pygame.draw.rect(display_surface, 'Black', debug_rect)  # Dibuja un rectángulo negro como fondo del texto en la pantalla
    display_surface.blit(debug_surf, debug_rect)  # Dibuja la superficie de texto sobre la pantalla en la posición del rectángulo