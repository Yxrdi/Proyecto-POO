import pygame  # Importa la biblioteca Pygame para trabajar con gráficos y sonido
from math import sin  # Importa la función 'sin' para usar el seno en cálculos matemáticos

class Entity(pygame.sprite.Sprite):  # Define la clase Entity, que hereda de pygame.sprite.Sprite
    def __init__(self, groups):  # Inicializador de la clase Entity, recibe los grupos de sprites
        super().__init__(groups)  # Llama al inicializador de la clase base Sprite para agregar la entidad a los grupos
        self.frame_index = 0  # Inicializa el índice de fotogramas (para animación)
        self.animation_speed = 0.15  # Define la velocidad de la animación (cuánto avanza el índice por fotograma)
        self.direction = pygame.math.Vector2()  # Inicializa un vector de dirección para el movimiento

    def move(self, speed):  # Define el método de movimiento de la entidad, recibe la velocidad como parámetro
        if self.direction.magnitude() != 0:  # Si la magnitud del vector de dirección no es 0 (es decir, hay movimiento)
            self.direction = self.direction.normalize()  # Normaliza el vector de dirección para mantener la velocidad constante

        self.hitbox.x += self.direction.x * speed  # Actualiza la posición de la hitbox en el eje X según la dirección y la velocidad
        self.collision('horizontal')  # Comprueba las colisiones horizontales con otros objetos
        self.hitbox.y += self.direction.y * speed  # Actualiza la posición de la hitbox en el eje Y según la dirección y la velocidad
        self.collision('vertical')  # Comprueba las colisiones verticales con otros objetos
        self.rect.center = self.hitbox.center  # Actualiza el centro del rectángulo de la entidad para que coincida con la hitbox

    def collision(self, direction):  # Define el método de colisiones, que recibe la dirección ('horizontal' o 'vertical')
        if direction == 'horizontal':  # Si la dirección es 'horizontal'
            for sprite in self.obstacle_sprites:  # Recorre todos los sprites en los que hay obstáculos
                if sprite.hitbox.colliderect(self.hitbox):  # Si hay colisión entre la hitbox del sprite y la hitbox de la entidad
                    if self.direction.x > 0:  # Si el movimiento es hacia la derecha
                        self.hitbox.right = sprite.hitbox.left  # Detiene el movimiento de la entidad ajustando su hitbox al borde izquierdo del obstáculo
                    if self.direction.x < 0:  # Si el movimiento es hacia la izquierda
                        self.hitbox.left = sprite.hitbox.right  # Detiene el movimiento de la entidad ajustando su hitbox al borde derecho del obstáculo

        if direction == 'vertical':  # Si la dirección es 'vertical'
            for sprite in self.obstacle_sprites:  # Recorre todos los sprites en los que hay obstáculos
                if sprite.hitbox.colliderect(self.hitbox):  # Si hay colisión entre la hitbox del sprite y la hitbox de la entidad
                    if self.direction.y > 0:  # Si el movimiento es hacia abajo
                        self.hitbox.bottom = sprite.hitbox.top  # Detiene el movimiento de la entidad ajustando su hitbox al borde superior del obstáculo
                    if self.direction.y < 0:  # Si el movimiento es hacia arriba
                        self.hitbox.top = sprite.hitbox.bottom  # Detiene el movimiento de la entidad ajustando su hitbox al borde inferior del obstáculo

    def wave_value(self):  # Define una función que devuelve un valor basado en una onda sinusoidal
        value = sin(pygame.time.get_ticks())  # Calcula el seno del tiempo actual en milisegundos
        if value >= 0:  # Si el valor del seno es positivo
            return 255  # Devuelve 255 (completamente opaco)
        else:  # Si el valor del seno es negativo
            return 0  # Devuelve 0 (completamente transparente)
