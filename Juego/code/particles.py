import pygame  # Importa la biblioteca Pygame para gestionar gráficos, sonidos y otros aspectos del juego.
from support import import_folder  # Importa la función import_folder desde el archivo support, que probablemente carga imágenes desde una carpeta.
from random import choice  # Importa la función choice desde la biblioteca random para seleccionar un elemento al azar de una lista.

class AnimationPlayer:  # Define la clase AnimationPlayer que gestionará las animaciones del juego.
    def __init__(self):  # Constructor de la clase
        self.frames = {  # Diccionario que contiene las animaciones de distintas categorías (magia, ataques, muertes de monstruos, hojas)
            # magia
            'flame': import_folder('../graphics/particles/flame/frames'),  # Carga los cuadros de animación para "flame"
            'aura': import_folder('../graphics/particles/aura'),  # Carga los cuadros de animación para "aura"
            'heal': import_folder('../graphics/particles/heal/frames'),  # Carga los cuadros de animación para "heal"
            
            # ataques
            'claw': import_folder('../graphics/particles/claw'),  # Carga los cuadros de animación para "claw"
            'slash': import_folder('../graphics/particles/slash'),  # Carga los cuadros de animación para "slash"
            'sparkle': import_folder('../graphics/particles/sparkle'),  # Carga los cuadros de animación para "sparkle"
            'leaf_attack': import_folder('../graphics/particles/leaf_attack'),  # Carga los cuadros de animación para "leaf_attack"
            'thunder': import_folder('../graphics/particles/thunder'),  # Carga los cuadros de animación para "thunder"

            # muertes de monstruos
            'squid': import_folder('../graphics/particles/smoke_orange'),  # Carga los cuadros de animación para la muerte de un "squid"
            'raccoon': import_folder('../graphics/particles/raccoon'),  # Carga los cuadros de animación para la muerte de un "raccoon"
            'spirit': import_folder('../graphics/particles/nova'),  # Carga los cuadros de animación para la muerte de un "spirit"
            'bamboo': import_folder('../graphics/particles/bamboo'),  # Carga los cuadros de animación para la muerte de un "bamboo"
            
            # hojas
            'leaf': (  # Varias animaciones de hojas, algunas de ellas son versiones reflejadas
                import_folder('../graphics/particles/leaf1'),  # Carga los cuadros de animación para "leaf1"
                import_folder('../graphics/particles/leaf2'),  # Carga los cuadros de animación para "leaf2"
                import_folder('../graphics/particles/leaf3'),  # Carga los cuadros de animación para "leaf3"
                import_folder('../graphics/particles/leaf4'),  # Carga los cuadros de animación para "leaf4"
                import_folder('../graphics/particles/leaf5'),  # Carga los cuadros de animación para "leaf5"
                import_folder('../graphics/particles/leaf6'),  # Carga los cuadros de animación para "leaf6"
                self.reflect_images(import_folder('../graphics/particles/leaf1')),  # Carga los cuadros reflejados para "leaf1"
                self.reflect_images(import_folder('../graphics/particles/leaf2')),  # Carga los cuadros reflejados para "leaf2"
                self.reflect_images(import_folder('../graphics/particles/leaf3')),  # Carga los cuadros reflejados para "leaf3"
                self.reflect_images(import_folder('../graphics/particles/leaf4')),  # Carga los cuadros reflejados para "leaf4"
                self.reflect_images(import_folder('../graphics/particles/leaf5')),  # Carga los cuadros reflejados para "leaf5"
                self.reflect_images(import_folder('../graphics/particles/leaf6'))  # Carga los cuadros reflejados para "leaf6"
            )
        }

    def reflect_images(self, frames):  # Método para reflejar las imágenes horizontalmente (flip)
        new_frames = []  # Lista vacía para almacenar las imágenes reflejadas

        for frame in frames:  # Itera sobre todos los cuadros de animación
            flipped_frame = pygame.transform.flip(frame, True, False)  # Refleja la imagen horizontalmente
            new_frames.append(flipped_frame)  # Añade la imagen reflejada a la lista de nuevos cuadros
        return new_frames  # Devuelve la lista de imágenes reflejadas

    def create_grass_particles(self, pos, groups):  # Crea partículas de césped en una posición dada
        animation_frames = choice(self.frames['leaf'])  # Elige una animación de hojas aleatoriamente
        ParticleEffect(pos, animation_frames, groups)  # Crea el efecto de partículas usando la animación seleccionada

    def create_particles(self, animation_type, pos, groups):  # Crea partículas de cualquier tipo de animación
        animation_frames = self.frames[animation_type]  # Obtiene los cuadros de animación correspondientes al tipo de animación
        ParticleEffect(pos, animation_frames, groups)  # Crea el efecto de partículas usando los cuadros correspondientes


class ParticleEffect(pygame.sprite.Sprite):  # Define la clase ParticleEffect, que representa una partícula en el juego
    def __init__(self, pos, animation_frames, groups):  # Constructor de la clase
        super().__init__(groups)  # Inicializa la clase Sprite y la añade a los grupos proporcionados
        self.sprite_type = 'magic'  # Define el tipo de sprite como 'magic'
        self.frame_index = 0  # Índice del cuadro de animación actual
        self.animation_speed = 0.15  # Velocidad de la animación (0.15 segundos por cuadro)
        self.frames = animation_frames  # Asigna los cuadros de animación
        self.image = self.frames[self.frame_index]  # Asigna la imagen del primer cuadro de animación
        self.rect = self.image.get_rect(center=pos)  # Establece el rectángulo de colisión de la partícula en la posición dada

    def animate(self):  # Método para actualizar la animación de la partícula
        self.frame_index += self.animation_speed  # Incrementa el índice del cuadro según la velocidad de animación
        if self.frame_index >= len(self.frames):  # Si hemos llegado al final de los cuadros de animación
            self.kill()  # Elimina la partícula del grupo de sprites
        else:
            self.image = self.frames[int(self.frame_index)]  # Actualiza la imagen de la partícula al siguiente cuadro de animación

    def update(self):  # Método que se llama cada vez que se actualiza el sprite
        self.animate()  # Llama al método de animación para actualizar la partícula
