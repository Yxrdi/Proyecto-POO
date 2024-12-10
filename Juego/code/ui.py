import pygame
from settings import *  # Importa las configuraciones definidas en el archivo settings.py (por ejemplo, tamaños de la interfaz de usuario, colores, etc.)

# Define la clase `UI`, que gestiona la interfaz de usuario del juego, como barras de salud, energía, experiencia, etc.
class UI:
    def __init__(self):
        
        # general setup
        self.display_surface = pygame.display.get_surface()  # Obtiene la superficie donde se dibuja el juego (pantalla del juego)
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)  # Carga la fuente para el texto en la interfaz

        # setup de las barras de salud y energía
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)  # Rectángulo para la barra de salud
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)  # Rectángulo para la barra de energía

        # Convierte el diccionario de armas en imágenes
        self.weapon_graphics = []
        for weapon in weapon_data.values():  # Itera sobre las armas definidas en `weapon_data`
            path = weapon['graphic']  # Obtiene la ruta de la imagen del arma
            weapon = pygame.image.load(path).convert_alpha()  # Carga la imagen con transparencia
            self.weapon_graphics.append(weapon)  # Añade la imagen a la lista de armas

        # Convierte el diccionario de magia en imágenes
        self.magic_graphics = []
        for magic in magic_data.values():  # Itera sobre los hechizos definidos en `magic_data`
            magic = pygame.image.load(magic['graphic']).convert_alpha()  # Carga la imagen de magia
            self.magic_graphics.append(magic)  # Añade la imagen a la lista de magia

    def show_bar(self, current, max_amount, bg_rect, color):
        """
        Dibuja una barra de progreso (como salud o energía).
        """
        # Dibuja el fondo de la barra
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # Convierte la cantidad de la barra en píxeles
        ratio = current / max_amount  # Calcula la proporción de la barra (cuánto está lleno)
        current_width = bg_rect.width * ratio  # Calcula el ancho de la barra según el valor actual
        current_rect = bg_rect.copy()  # Copia el rectángulo de la barra
        current_rect.width = current_width  # Establece el ancho de la barra actual

        # Dibuja la barra llena
        pygame.draw.rect(self.display_surface, color, current_rect)  # Dibuja la barra de color (salud, energía, etc.)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)  # Dibuja el borde de la barra

    def show_exp(self, exp):
        """
        Muestra la experiencia actual del jugador.
        """
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)  # Crea la superficie de texto con la experiencia
        x = self.display_surface.get_size()[0] - 20  # Obtiene la posición X (esquina derecha)
        y = self.display_surface.get_size()[1] - 20  # Obtiene la posición Y (esquina inferior)
        text_rect = text_surf.get_rect(bottomright = (x, y))  # Define el rectángulo donde se mostrará el texto

        # Dibuja el fondo del cuadro de texto
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))  # Fondo del cuadro de experiencia
        self.display_surface.blit(text_surf, text_rect)  # Dibuja el texto de experiencia
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)  # Dibuja el borde del cuadro de texto

    def selection_box(self, left, top, has_switched):
        """
        Muestra el cuadro de selección para armas o magia.
        """
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)  # Crea el rectángulo para el cuadro de selección
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)  # Dibuja el fondo del cuadro de selección
        if has_switched:  # Si el jugador ha cambiado el arma/magia, resalta el borde
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)  # Dibuja borde activo
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)  # Dibuja el borde normal
        return bg_rect  # Devuelve el rectángulo de la selección

    def weapon_overlay(self, weapon_index, has_switched):
        """
        Dibuja el icono del arma seleccionada en la interfaz.
        """
        bg_rect = self.selection_box(10, 630, has_switched)  # Obtiene el rectángulo de selección para el arma
        weapon_surf = self.weapon_graphics[weapon_index]  # Obtiene la imagen del arma correspondiente
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)  # Coloca el arma en el centro del cuadro

        self.display_surface.blit(weapon_surf, weapon_rect)  # Dibuja el icono del arma en la pantalla

    def magic_overlay(self, magic_index, has_switched):
        """
        Dibuja el icono de la magia seleccionada en la interfaz.
        """
        bg_rect = self.selection_box(80, 635, has_switched)  # Obtiene el rectángulo de selección para la magia
        magic_surf = self.magic_graphics[magic_index]  # Obtiene la imagen de la magia correspondiente
        magic_rect = magic_surf.get_rect(center = bg_rect.center)  # Coloca la magia en el centro del cuadro

        self.display_surface.blit(magic_surf, magic_rect)  # Dibuja el icono de la magia en la pantalla

    def display(self, player):
        """
        Muestra todas las barras y la interfaz en la pantalla.
        """
        # Muestra la barra de salud
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        # Muestra la barra de energía
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)

        # Muestra la experiencia
        self.show_exp(player.exp)

        # Muestra el overlay del arma
        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
        # Muestra el overlay de la magia
        self.magic_overlay(player.magic_index, not player.can_switch_magic)
