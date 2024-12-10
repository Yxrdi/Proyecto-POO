# Importa el módulo Pygame para gestionar gráficos, sonido y otros aspectos del juego
import pygame  
# Importa las configuraciones definidas en el archivo `settings.py` (como `TILESIZE` y `HITBOX_OFFSET`)
from settings import *  

# Define la clase `Tile`, que representa una "loseta" o "tile" en el juego (puede ser un objeto, parte del terreno, etc.)
class Tile(pygame.sprite.Sprite):
    # Constructor de la clase Tile, recibe la posición, grupos, tipo de sprite y una superficie opcional
    def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)  # Llama al constructor de la clase base `Sprite` para agregar este tile a los grupos de sprites
        
        self.sprite_type = sprite_type  # Define el tipo de sprite (por ejemplo, 'object', 'grass', etc.)
        
        # Se obtiene el desplazamiento en el eje Y para la hitbox a partir del tipo de sprite (de `HITBOX_OFFSET`)
        y_offset = HITBOX_OFFSET[sprite_type]
        
        # Asigna la superficie (imagen) del tile, que por defecto es un objeto vacío con tamaño TILESIZE x TILESIZE
        self.image = surface
        
        # Si el tipo de sprite es 'object', ajusta la posición en el eje Y para colocar el tile en la posición correcta
        if sprite_type == 'object':
            self.rect = self.image.get_rect(topleft = (pos[0], pos[1] - TILESIZE))  # Coloca la imagen en la posición ajustada
        else:
            self.rect = self.image.get_rect(topleft = pos)  # Para otros tipos de tiles, usa la posición sin modificar
        
        # Ajusta la hitbox del tile, que se infla (cambia su tamaño) en función del tipo de sprite (según `HITBOX_OFFSET`)
        self.hitbox = self.rect.inflate(0, y_offset)  # La hitbox tiene el mismo tamaño que el rectángulo, pero con un ajuste vertical (y_offset)
