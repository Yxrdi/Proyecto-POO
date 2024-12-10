import pygame 

# Clase que representa un arma del jugador en el juego, hereda de Sprite de Pygame
class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)  # Llama al constructor de la clase base Sprite, añadiendo el arma a los grupos proporcionados
        self.sprite_type = 'weapon'  # Define el tipo de sprite como 'weapon' para identificarlo en el juego
        direction = player.status.split('_')[0]  # Obtiene la dirección del jugador (derecha, izquierda, abajo, arriba)

        # Carga la imagen del arma en función de la dirección en que está el jugador
        full_path = f'../graphics/weapons/{player.weapon}/{direction}.png'  # Ruta a la imagen del arma
        self.image = pygame.image.load(full_path).convert_alpha()  # Carga la imagen y la convierte con transparencia

        # Determina la colocación del arma según la dirección del jugador
        # Basado en la dirección, coloca el arma en una posición relativa al jugador

        if direction == 'right':
            # Si la dirección es "derecha", coloca el arma en el lado derecho del jugador
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0, 16))
        elif direction == 'left':
            # Si la dirección es "izquierda", coloca el arma en el lado izquierdo del jugador
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0, 16))
        elif direction == 'down':
            # Si la dirección es "abajo", coloca el arma debajo del jugador
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10, 0))
        else:
            # Si la dirección es "arriba", coloca el arma arriba del jugador
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10, 0))
