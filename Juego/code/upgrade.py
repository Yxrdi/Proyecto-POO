import pygame
from settings import *  # Importa configuraciones (como colores, tamaños, etc.)

# Clase principal para gestionar las actualizaciones o mejoras del jugador
class Upgrade:
    def __init__(self, player):
        # Inicializa la clase con el jugador
        self.display_surface = pygame.display.get_surface()  # Superficie de la pantalla para dibujar
        self.player = player  # Referencia al jugador
        self.attribute_nr = len(player.stats)  # Número de atributos del jugador
        self.attribute_names = list(player.stats.keys())  # Lista de nombres de los atributos
        self.max_values = list(player.max_stats.values())  # Valores máximos de los atributos
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)  # Fuente para el texto de la UI

        # Creación de los elementos (botones) para las mejoras
        self.height = self.display_surface.get_size()[1] * 0.8  # Altura de los elementos (80% de la altura de la pantalla)
        self.width = self.display_surface.get_size()[0] // 6  # Ancho de los elementos (1/6 del ancho de la pantalla)
        self.create_items()  # Llama a la función para crear los elementos (botones)

        # Sistema de selección de elementos
        self.selection_index = 0  # Índice del elemento seleccionado
        self.selection_time = None  # Tiempo en el que se realizó la selección
        self.can_move = True  # Determina si se puede mover la selección

    def input(self):
        # Gestión de entradas del usuario
        keys = pygame.key.get_pressed()  # Obtiene el estado de todas las teclas

        if self.can_move:
            # Si se puede mover la selección
            if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_nr - 1:
                self.selection_index += 1  # Mueve la selección a la derecha
                self.can_move = False  # Desactiva el movimiento temporalmente
                self.selection_time = pygame.time.get_ticks()  # Marca el tiempo de la selección
            elif keys[pygame.K_LEFT] and self.selection_index >= 1:
                self.selection_index -= 1  # Mueve la selección a la izquierda
                self.can_move = False  # Desactiva el movimiento temporalmente
                self.selection_time = pygame.time.get_ticks()  # Marca el tiempo de la selección

            if keys[pygame.K_SPACE]:
                # Si se presiona la tecla "Espacio"
                self.can_move = False  # Desactiva el movimiento
                self.selection_time = pygame.time.get_ticks()  # Marca el tiempo de la selección
                self.item_list[self.selection_index].trigger(self.player)  # Llama a la acción de mejora

    def selection_cooldown(self):
        # Enfriamiento de la selección para evitar selecciones rápidas
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:  # 300 ms de cooldown
                self.can_move = True  # Permite mover la selección nuevamente

    def create_items(self):
        # Crea los botones de mejora
        self.item_list = []  # Lista donde se guardarán los botones

        for item, index in enumerate(range(self.attribute_nr)):
            # Calcula la posición de cada botón (horizontal)
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attribute_nr  # Espaciado horizontal entre los botones
            left = (item * increment) + (increment - self.width) // 2  # Calcula la posición horizontal de cada botón

            # Posición vertical fija para todos los botones
            top = self.display_surface.get_size()[1] * 0.1  # 10% de la altura de la pantalla

            # Crea el objeto Item (un botón)
            item = Item(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)  # Agrega el botón a la lista de botones

    def display(self):
        # Dibuja los elementos en la pantalla
        self.input()  # Llama a la función para procesar las entradas
        self.selection_cooldown()  # Llama a la función de cooldown

        # Muestra cada uno de los elementos (botones)
        for index, item in enumerate(self.item_list):
            # Obtiene los datos del atributo correspondiente
            name = self.attribute_names[index]  # Nombre del atributo
            value = self.player.get_value_by_index(index)  # Valor actual del atributo
            max_value = self.max_values[index]  # Valor máximo del atributo
            cost = self.player.get_cost_by_index(index)  # Costo de la mejora

            # Dibuja el botón
            item.display(self.display_surface, self.selection_index, name, value, max_value, cost)

# Clase que representa un botón de mejora
class Item:
    def __init__(self, l, t, w, h, index, font):
        self.rect = pygame.Rect(l, t, w, h)  # Rectángulo que representa el área del botón
        self.index = index  # Índice del atributo asociado
        self.font = font  # Fuente para el texto del botón

    def display_names(self, surface, name, cost, selected):
        # Muestra los nombres (atributo) y el costo de la mejora
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR  # Color del texto, cambia si está seleccionado

        # Título (nombre del atributo)
        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(midtop=self.rect.midtop + pygame.math.Vector2(0, 20))  # Posición del nombre

        # Costo de la mejora
        cost_surf = self.font.render(f'{int(cost)}', False, color)
        cost_rect = cost_surf.get_rect(midbottom=self.rect.midbottom - pygame.math.Vector2(0, 20))  # Posición del costo

        # Dibuja el texto en la superficie
        surface.blit(title_surf, title_rect)
        surface.blit(cost_surf, cost_rect)

    def display_bar(self, surface, value, max_value, selected):
        # Dibuja la barra de progreso para el atributo
        top = self.rect.midtop + pygame.math.Vector2(0, 60)  # Posición superior de la barra
        bottom = self.rect.midbottom - pygame.math.Vector2(0, 60)  # Posición inferior de la barra
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR  # Color de la barra, cambia si está seleccionada

        # Calcula la altura de la barra proporcional al valor del atributo
        full_height = bottom[1] - top[1]
        relative_number = (value / max_value) * full_height
        value_rect = pygame.Rect(top[0] - 15, bottom[1] - relative_number, 30, 10)  # Rectángulo para la barra

        # Dibuja la barra
        pygame.draw.line(surface, color, top, bottom, 5)  # Barra de fondo
        pygame.draw.rect(surface, color, value_rect)  # Barra que indica el valor actual

    def trigger(self, player):
        # Activa la mejora para el atributo asociado
        upgrade_attribute = list(player.stats.keys())[self.index]  # Atributo correspondiente

        # Si el jugador tiene suficiente experiencia y el atributo no ha alcanzado su valor máximo
        if player.exp >= player.upgrade_cost[upgrade_attribute] and player.stats[upgrade_attribute] < player.max_stats[upgrade_attribute]:
            player.exp -= player.upgrade_cost[upgrade_attribute]  # Resta la experiencia
            player.stats[upgrade_attribute] *= 1.2  # Aumenta el valor del atributo en un 20%
            player.upgrade_cost[upgrade_attribute] *= 1.4  # Aumenta el costo de la siguiente mejora

        # Asegura que el valor del atributo no supere el valor máximo
        if player.stats[upgrade_attribute] > player.max_stats[upgrade_attribute]:
            player.stats[upgrade_attribute] = player.max_stats[upgrade_attribute]

    def display(self, surface, selection_num, name, value, max_value, cost):
        # Dibuja el botón con su nombre, barra de progreso y costo
        if self.index == selection_num:
            # Si el botón está seleccionado, cambia su color de fondo
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)  # Borde del botón
        else:
            # Si el botón no está seleccionado, usa colores por defecto
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)  # Borde del botón
        
        # Muestra el nombre del atributo y el costo
        self.display_names(surface, name, cost, self.index == selection_num)
        # Muestra la barra de progreso del atributo
        self.display_bar(surface, value, max_value, self.index == selection_num)
