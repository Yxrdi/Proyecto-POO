import pygame  # Importa la biblioteca Pygame para trabajar con gráficos y sonido
from settings import *  # Importa configuraciones globales desde el archivo settings.py
from entity import Entity  # Importa la clase base Entity, de la que Enemy heredará
from support import *  # Importa funciones de apoyo desde el archivo support.py (como importar gráficos)

class Enemy(Entity):  # Define la clase Enemy que hereda de la clase Entity
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, add_exp):
        # general setup
        super().__init__(groups)  # Llama al constructor de la clase base (Entity), pasando los grupos de sprites
        self.sprite_type = 'enemy'  # Establece el tipo de sprite como 'enemy'

        # graphics setup
        self.import_graphics(monster_name)  # Importa las animaciones gráficas para este enemigo
        self.status = 'idle'  # Establece el estado inicial como 'idle' (inactivo)
        self.image = self.animations[self.status][self.frame_index]  # Establece la imagen del enemigo según su estado actual

        # movement
        self.rect = self.image.get_rect(topleft=pos)  # Obtiene el rectángulo de la imagen y lo coloca en la posición dada
        self.hitbox = self.rect.inflate(0, -10)  # Ajusta el tamaño del rectángulo para la colisión
        self.obstacle_sprites = obstacle_sprites  # Define los sprites de obstáculos para la detección de colisiones

        # stats
        self.monster_name = monster_name  # Establece el nombre del monstruo
        monster_info = monster_data[self.monster_name]  # Obtiene los datos del monstruo desde un diccionario global
        self.health = monster_info['health']  # Establece la salud del monstruo
        self.exp = monster_info['exp']  # Establece la experiencia que se gana al matar al monstruo
        self.speed = monster_info['speed']  # Establece la velocidad de movimiento
        self.attack_damage = monster_info['damage']  # Establece el daño de ataque
        self.resistance = monster_info['resistance']  # Establece la resistencia del monstruo
        self.attack_radius = monster_info['attack_radius']  # Define el radio de ataque
        self.notice_radius = monster_info['notice_radius']  # Define el radio en el que el monstruo puede notar al jugador
        self.attack_type = monster_info['attack_type']  # Establece el tipo de ataque del monstruo

        # player interaction
        self.can_attack = True  # Define si el enemigo puede atacar
        self.attack_time = None  # Guarda el tiempo del último ataque
        self.attack_cooldown = 400  # Define el tiempo de espera entre ataques
        self.damage_player = damage_player  # Función que causa daño al jugador
        self.trigger_death_particles = trigger_death_particles  # Función que activa partículas al morir
        self.add_exp = add_exp  # Función que agrega experiencia al jugador

        # invincibility timer
        self.vulnerable = True  # Define si el enemigo es vulnerable a ataques
        self.hit_time = None  # Guarda el tiempo del último golpe recibido
        self.invincibility_duration = 300  # Duración de la invulnerabilidad en milisegundos

        # sounds
        self.death_sound = pygame.mixer.Sound('../audio/death.wav')  # Sonido de muerte del enemigo
        self.hit_sound = pygame.mixer.Sound('../audio/hit.wav')  # Sonido cuando el enemigo es golpeado
        self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])  # Sonido del ataque del monstruo
        self.death_sound.set_volume(0.6)  # Establece el volumen del sonido de muerte
        self.hit_sound.set_volume(0.6)  # Establece el volumen del sonido de golpe
        self.attack_sound.set_volume(0.6)  # Establece el volumen del sonido de ataque

    def import_graphics(self, name):
        self.animations = {'idle': [], 'move': [], 'attack': []}  # Inicializa un diccionario de animaciones
        main_path = f'../graphics/monsters/{name}/'  # Define la ruta de los gráficos del monstruo
        for animation in self.animations.keys():  # Recorre los tipos de animaciones ('idle', 'move', 'attack')
            self.animations[animation] = import_folder(main_path + animation)  # Importa los gráficos de cada animación

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)  # Obtiene el vector de la posición central del enemigo
        player_vec = pygame.math.Vector2(player.rect.center)  # Obtiene el vector de la posición central del jugador
        distance = (player_vec - enemy_vec).magnitude()  # Calcula la distancia entre el enemigo y el jugador

        if distance > 0:  # Si la distancia no es cero
            direction = (player_vec - enemy_vec).normalize()  # Normaliza el vector de dirección del enemigo hacia el jugador
        else:
            direction = pygame.math.Vector2()  # Si la distancia es cero, no hay dirección

        return (distance, direction)  # Devuelve la distancia y la dirección del enemigo hacia el jugador

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]  # Obtiene la distancia entre el enemigo y el jugador

        if distance <= self.attack_radius and self.can_attack:  # Si el jugador está dentro del radio de ataque y el enemigo puede atacar
            if self.status != 'attack':  # Si el enemigo no está en estado de ataque
                self.frame_index = 0  # Reinicia el índice de fotogramas para la animación de ataque
            self.status = 'attack'  # Cambia el estado a 'attack'
        elif distance <= self.notice_radius:  # Si el jugador está dentro del radio de notificación
            self.status = 'move'  # Cambia el estado a 'move' (moverse)
        else:
            self.status = 'idle'  # Si el jugador está fuera de rango, cambia el estado a 'idle' (inactivo)

    def actions(self, player):
        if self.status == 'attack':  # Si el estado es 'attack'
            self.attack_time = pygame.time.get_ticks()  # Registra el tiempo del ataque
            self.damage_player(self.attack_damage, self.attack_type)  # Causa daño al jugador
            self.attack_sound.play()  # Reproduce el sonido de ataque
        elif self.status == 'move':  # Si el estado es 'move'
            self.direction = self.get_player_distance_direction(player)[1]  # Obtiene la dirección hacia el jugador
        else:
            self.direction = pygame.math.Vector2()  # Si el estado es 'idle', no hay movimiento

    def animate(self):
        animation = self.animations[self.status]  # Obtiene la animación correspondiente al estado actual

        self.frame_index += self.animation_speed  # Avanza el índice de fotogramas de la animación
        if self.frame_index >= len(animation):  # Si el índice excede la longitud de la animación
            if self.status == 'attack':  # Si el estado es 'attack', deshabilita el ataque
                self.can_attack = False
            self.frame_index = 0  # Reinicia el índice de fotogramas

        self.image = animation[int(self.frame_index)]  # Actualiza la imagen del enemigo con el fotograma actual de la animación
        self.rect = self.image.get_rect(center=self.hitbox.center)  # Actualiza el rectángulo de colisión con la nueva imagen

        if not self.vulnerable:  # Si el enemigo no es vulnerable
            alpha = self.wave_value()  # Calcula la transparencia de la imagen
            self.image.set_alpha(alpha)  # Aplica la transparencia
        else:
            self.image.set_alpha(255)  # Si el enemigo es vulnerable, la imagen no es transparente

    def cooldowns(self):
        current_time = pygame.time.get_ticks()  # Obtiene el tiempo actual en milisegundos
        if not self.can_attack:  # Si el enemigo no puede atacar
            if current_time - self.attack_time >= self.attack_cooldown:  # Si ha pasado el tiempo de recarga
                self.can_attack = True  # Permite al enemigo atacar nuevamente

        if not self.vulnerable:  # Si el enemigo no es vulnerable
            if current_time - self.hit_time >= self.invincibility_duration:  # Si ha pasado el tiempo de invulnerabilidad
                self.vulnerable = True  # El enemigo vuelve a ser vulnerable

    def get_damage(self, player, attack_type):
        if self.vulnerable:  # Si el enemigo es vulnerable
            self.hit_sound.play()  # Reproduce el sonido de golpe
            self.direction = self.get_player_distance_direction(player)[1]  # Establece la dirección del enemigo hacia el jugador
            if attack_type == 'weapon':  # Si el ataque es de tipo 'weapon'
                self.health -= player.get_full_weapon_damage()  # Resta la salud del enemigo con el daño del arma
            else:  # Si el ataque es de tipo 'magic'
                self.health -= player.get_full_magic_damage()  # Resta la salud del enemigo con el daño mágico
            self.hit_time = pygame.time.get_ticks()  # Registra el tiempo del golpe
            self.vulnerable = False  # El enemigo deja de ser vulnerable

    def check_death(self):
        if self.health <= 0:  # Si la salud del enemigo llega a cero
            self.kill()  # Elimina al enemigo de los grupos de sprites
            self.trigger_death_particles(self.rect.center, self.monster_name)  # Activa las partículas de muerte
            self.add_exp(self.exp)  # Añade experiencia al jugador
            self.death_sound.play()  # Reproduce el sonido de muerte

    def hit_reaction(self):
        if not self.vulnerable:  # Si el enemigo no es vulnerable
            self.direction *= -self.resistance  # Reacciona al golpe, cambiando la dirección

    def update(self):
        self.hit_reaction()  # Reacciona al ser golpeado
        self.move(self.speed)  # Mueve al enemigo según su velocidad
        self.animate()  # Actualiza la animación del enemigo
        self.cooldowns()  # Controla los tiempos de recarga de ataques e invulnerabilidad
        self.check_death()  # Verifica si el enemigo ha muerto

    def enemy_update(self, player):
        self.get_status(player)  # Actualiza el estado del enemigo según la distancia al jugador
        self.actions(player)  # Realiza las acciones correspondientes al estado actual
