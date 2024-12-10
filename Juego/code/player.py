import pygame  # Importación de la biblioteca Pygame
from settings import *  # Importación de configuraciones globales desde el archivo 'settings'
from support import import_folder  # Función para importar gráficos desde carpetas
from entity import Entity  # Clase base para entidades, como el jugador o enemigos

class Player(Entity):  # Definición de la clase Player, que hereda de Entity
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):
        super().__init__(groups)  # Llamada al constructor de la clase base (Entity)
        self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()  # Carga la imagen del jugador
        self.rect = self.image.get_rect(topleft=pos)  # Crea el rectángulo que define la posición del jugador
        self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET['player'])  # Ajusta la hitbox (área de colisión)

        # Configuración de gráficos del jugador
        self.import_player_assets()  # Carga las animaciones del jugador
        self.status = 'down'  # Establece el estado inicial como mirando hacia abajo

        # Movimiento y control de ataque
        self.attacking = False  # Indica si el jugador está atacando
        self.attack_cooldown = 400  # Tiempo de recarga entre ataques
        self.attack_time = None  # Almacena el tiempo en que se realizó el último ataque
        self.obstacle_sprites = obstacle_sprites  # Lista de objetos que pueden bloquear al jugador

        # Configuración de armas
        self.create_attack = create_attack  # Función para crear el ataque
        self.destroy_attack = destroy_attack  # Función para destruir el ataque
        self.weapon_index = 0  # Índice del arma actual
        self.weapon = list(weapon_data.keys())[self.weapon_index]  # Arma inicial
        self.can_switch_weapon = True  # Indica si se puede cambiar de arma
        self.weapon_switch_time = None  # Almacena el tiempo del último cambio de arma
        self.switch_duration_cooldown = 200  # Tiempo de recarga para cambiar de arma

        # Configuración de magia
        self.create_magic = create_magic  # Función para crear magia
        self.magic_index = 0  # Índice de la magia actual
        self.magic = list(magic_data.keys())[self.magic_index]  # Magia inicial
        self.can_switch_magic = True  # Indica si se puede cambiar de magia
        self.magic_switch_time = None  # Almacena el tiempo del último cambio de magia

        # Estadísticas del jugador
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 5}  # Estadísticas base
        self.max_stats = {'health': 300, 'energy': 140, 'attack': 20, 'magic': 10, 'speed': 10}  # Estadísticas máximas
        self.upgrade_cost = {'health': 100, 'energy': 100, 'attack': 100, 'magic': 100, 'speed': 100}  # Costos de mejora
        self.health = self.stats['health'] * 0.5  # Salud inicial
        self.energy = self.stats['energy'] * 0.8  # Energía inicial
        self.exp = 5000  # Experiencia inicial
        self.speed = self.stats['speed']  # Velocidad inicial

        # Temporizador de daño (invulnerabilidad)
        self.vulnerable = True  # El jugador es vulnerable al daño
        self.hurt_time = None  # Almacena el tiempo en que el jugador fue golpeado
        self.invulnerability_duration = 500  # Duración de la invulnerabilidad después de ser golpeado

        # Carga de sonido del ataque con arma
        self.weapon_attack_sound = pygame.mixer.Sound('../audio/sword.wav')
        self.weapon_attack_sound.set_volume(0.4)  # Ajusta el volumen del sonido

    # Carga las animaciones del jugador (caminar, atacar, etc.)
    def import_player_assets(self):
        character_path = '../graphics/player/'  # Ruta donde se encuentran las animaciones
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],  # Animaciones para diferentes direcciones
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}

        # Carga todas las animaciones desde las carpetas correspondientes
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    # Detecta la entrada del usuario (movimiento, ataques, magia, etc.)
    def input(self):
        if not self.attacking:  # Solo se aceptan entradas si no está atacando
            keys = pygame.key.get_pressed()

            # Entrada para el movimiento
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            # Entrada para ataques (presionando la barra espaciadora)
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()  # Registra el tiempo del ataque
                self.create_attack()  # Crea el ataque
                self.weapon_attack_sound.play()  # Reproduce el sonido del ataque

            # Entrada para magia (presionando Ctrl izquierdo)
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(style, strength, cost)  # Crea la magia

            # Cambio de arma (presionando la tecla Q)
            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()  # Registra el tiempo del cambio de arma
                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0  # Vuelve al primer arma
                self.weapon = list(weapon_data.keys())[self.weapon_index]

            # Cambio de magia (presionando la tecla E)
            if keys[pygame.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()  # Registra el tiempo del cambio de magia
                if self.magic_index < len(list(magic_data.keys())) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0  # Vuelve a la primera magia
                self.magic = list(magic_data.keys())[self.magic_index]

    # Obtiene el estado del jugador (por ejemplo, movimiento o inactividad)
    def get_status(self):
        # Estado inactivo
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        # Estado de ataque
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    # Gestiona los tiempos de recarga de ataques, cambio de armas y magias
    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        # Enfriamiento después de un ataque
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()

        # Enfriamiento para cambiar de arma
        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        # Enfriamiento para cambiar de magia
        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        # Enfriamiento para invulnerabilidad
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    # Gestiona la animación del jugador (cambia las imágenes dependiendo del estado)
    def animate(self):
        animation = self.animations[self.status]

        # Se recorre el índice de la animación
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0  # Resetea al principio de la animación

        # Establece la imagen actual en base al índice de la animación
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # Efecto de parpadeo cuando es golpeado
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)  # Aplica el parpadeo
        else:
            self.image.set_alpha(255)  # Restablece la opacidad

    # Calcula el daño total del arma
    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    # Calcula el daño total de la magia
    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.magic]['strength']
        return base_damage + spell_damage

    # Obtiene un valor de las estadísticas en función del índice
    def get_value_by_index(self, index):
        return list(self.stats.values())[index]

    # Obtiene el costo de mejora de una estadística
    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]

    # Recupera energía con el tiempo
    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.01 * self.stats['magic']  # Recupera energía según la magia
        else:
            self.energy = self.stats['energy']  # Limita la energía al máximo

    # Método de actualización llamado en cada frame
    def update(self):
        self.input()  # Detecta la entrada del usuario
        self.cooldowns()  # Gestiona los tiempos de recarga
        self.get_status()  # Actualiza el estado del jugador
        self.animate()  # Actualiza la animación del jugador
        self.move(self.stats['speed'])  # Mueve al jugador según su velocidad
        self.energy_recovery()  # Recupera energía automáticamente
