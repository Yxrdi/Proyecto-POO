import pygame  # Importa la librería pygame para gestionar gráficos, sonidos y eventos.
from settings import *  # Importa configuraciones globales (como valores de constantes) desde el archivo 'settings'.
from random import randint  # Importa la función 'randint' para generar números aleatorios enteros dentro de un rango.

# Clase que maneja las habilidades mágicas del jugador
class MagicPlayer:
    def __init__(self, animation_player):
        # Inicializa el objeto MagicPlayer con un objeto de animación para gestionar las partículas.
        self.animation_player = animation_player
        # Define los sonidos para cada habilidad mágica
        self.sounds = {
            'heal': pygame.mixer.Sound('../audio/heal.wav'),  # Sonido de la habilidad 'heal' (curación)
            'flame': pygame.mixer.Sound('../audio/Fire.wav')  # Sonido de la habilidad 'flame' (fuego)
        }

    # Método para curar al jugador
    def heal(self, player, strength, cost, groups):
        # Verifica si el jugador tiene suficiente energía para realizar la curación
        if player.energy >= cost:
            # Reproduce el sonido de curación
            self.sounds['heal'].play()
            # Aumenta la salud del jugador en función de la fuerza de curación
            player.health += strength
            # Reduce la energía del jugador por el coste de la habilidad
            player.energy -= cost
            # Si la salud del jugador excede la salud máxima, ajusta la salud a la máxima
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            # Crea partículas de aura alrededor del jugador
            self.animation_player.create_particles('aura', player.rect.center, groups)
            # Crea partículas de curación alrededor del jugador
            self.animation_player.create_particles('heal', player.rect.center, groups)

    # Método para lanzar un ataque de fuego
    def flame(self, player, cost, groups):
        # Verifica si el jugador tiene suficiente energía para lanzar el ataque de fuego
        if player.energy >= cost:
            # Reduce la energía del jugador por el coste del ataque de fuego
            player.energy -= cost
            # Reproduce el sonido del ataque de fuego
            self.sounds['flame'].play()

            # Determina la dirección del ataque en función de la dirección en la que está mirando el jugador
            if player.status.split('_')[0] == 'right': 
                direction = pygame.math.Vector2(1, 0)  # Dirección horizontal hacia la derecha
            elif player.status.split('_')[0] == 'left': 
                direction = pygame.math.Vector2(-1, 0)  # Dirección horizontal hacia la izquierda
            elif player.status.split('_')[0] == 'up': 
                direction = pygame.math.Vector2(0, -1)  # Dirección vertical hacia arriba
            else: 
                direction = pygame.math.Vector2(0, 1)  # Dirección vertical hacia abajo

            # Crea partículas de fuego a lo largo de la dirección del ataque
            for i in range(1, 6):  # Crea 5 partículas de fuego
                if direction.x:  # Si el ataque es horizontal (derecha o izquierda)
                    offset_x = (direction.x * i) * TILESIZE  # Desplazamiento horizontal
                    x = player.rect.centerx + offset_x + randint(-TILESIZE // 3, TILESIZE // 3)  # Coordenada X aleatoria
                    y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)  # Coordenada Y aleatoria
                    # Crea partículas de fuego en las coordenadas calculadas
                    self.animation_player.create_particles('flame', (x, y), groups)
                else:  # Si el ataque es vertical (arriba o abajo)
                    offset_y = (direction.y * i) * TILESIZE  # Desplazamiento vertical
                    x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)  # Coordenada X aleatoria
                    y = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)  # Coordenada Y aleatoria
                    # Crea partículas de fuego en las coordenadas calculadas
                    self.animation_player.create_particles('flame', (x, y), groups)
