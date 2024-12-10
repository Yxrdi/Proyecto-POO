import pygame  # Importa la biblioteca Pygame para gráficos, sonido, etc.
from settings import *  # Importa configuraciones, como el tamaño del tile, etc.
from tile import Tile  # Importa la clase Tile, que probablemente maneja la creación de tiles en el mapa.
from player import Player  # Importa la clase Player, que representa al jugador.
from debug import debug  # Importa el módulo de depuración (probablemente para mostrar información de depuración).
from support import *  # Importa funciones auxiliares, como la carga de gráficos o mapas.
from random import choice, randint  # Importa funciones para elegir un elemento aleatorio o generar números aleatorios.
from weapon import Weapon  # Importa la clase Weapon para manejar las armas del jugador.
from ui import UI  # Importa la clase UI para la interfaz de usuario.
from enemy import Enemy  # Importa la clase Enemy para manejar los enemigos.
from particles import AnimationPlayer  # Importa AnimationPlayer para crear y gestionar las animaciones de partículas.
from magic import MagicPlayer  # Importa MagicPlayer para manejar las habilidades mágicas.
from upgrade import Upgrade  # Importa la clase Upgrade para gestionar las mejoras del jugador.

class Level:
    def __init__(self):
        # Obtén la superficie de pantalla de Pygame
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False  # Define el estado del juego (pausado o no)

        # Configura los grupos de sprites
        self.visible_sprites = YSortCameraGroup()  # Grupo que maneja los sprites visibles y ordenados por altura
        self.obstacle_sprites = pygame.sprite.Group()  # Grupo de sprites de obstáculos

        # Configura los sprites de ataque
        self.current_attack = None  # No hay ataque por defecto
        self.attack_sprites = pygame.sprite.Group()  # Grupo de sprites de ataque
        self.attackable_sprites = pygame.sprite.Group()  # Grupo de sprites que pueden ser atacados

        # Configura los sprites del mapa
        self.create_map()

        # Interfaz de usuario
        self.ui = UI()  # Crea la interfaz de usuario
        self.upgrade = Upgrade(self.player)  # Crea el sistema de mejoras

        # Partículas
        self.animation_player = AnimationPlayer()  # Crea el jugador de animaciones para manejar las partículas
        self.magic_player = MagicPlayer(self.animation_player)  # Crea el jugador de magia, con animaciones para las habilidades mágicas

    def create_map(self):
        # Carga los datos del mapa en forma de listas (en formato CSV)
        layouts = {
            'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),  # Carga el mapa de bloques de suelo
            'grass': import_csv_layout('../map/map_Grass.csv'),  # Carga el mapa de césped
            'object': import_csv_layout('../map/map_Objects.csv'),  # Carga el mapa de objetos
            'entities': import_csv_layout('../map/map_Entities.csv')  # Carga el mapa de entidades (jugador, enemigos)
        }
        graphics = {
            'grass': import_folder('../graphics/Grass'),  # Carga las imágenes para los tiles de césped
            'objects': import_folder('../graphics/objects')  # Carga las imágenes para los objetos
        }

        # Procesa los datos del mapa y crea los tiles correspondientes
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':  # Si el valor no es '-1', es un tile válido
                        x = col_index * TILESIZE  # Calcula la posición X del tile
                        y = row_index * TILESIZE  # Calcula la posición Y del tile
                        if style == 'boundary':  # Si es un tile de borde, es un obstáculo invisible
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'grass':  # Si es un tile de césped, elige una imagen aleatoria de césped
                            random_grass_image = choice(graphics['grass'])
                            Tile(
                                (x, y),
                                [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites],
                                'grass',
                                random_grass_image)

                        if style == 'object':  # Si es un objeto, utiliza la imagen del objeto correspondiente
                            surf = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)

                        if style == 'entities':  # Si es una entidad (jugador o enemigo)
                            if col == '394':  # Si el código es '394', es el jugador
                                self.player = Player(
                                    (x, y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic)
                            else:  # Si el código es un número diferente, crea un enemigo
                                if col == '390': monster_name = 'bamboo'
                                elif col == '391': monster_name = 'spirit'
                                elif col == '392': monster_name = 'raccoon'
                                else: monster_name = 'squid'
                                Enemy(
                                    monster_name,
                                    (x, y),
                                    [self.visible_sprites, self.attackable_sprites],
                                    self.obstacle_sprites,
                                    self.damage_player,
                                    self.trigger_death_particles,
                                    self.add_exp)

    def create_attack(self):
        # Crea un ataque para el jugador
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):
        # Crea magia de acuerdo con el estilo, fuerza y costo
        if style == 'heal':  # Si es una habilidad de curación
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])

        if style == 'flame':  # Si es una habilidad de fuego
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        # Destruye el ataque actual
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        # Lógica para el ataque del jugador
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:  # Recorre los sprites de ataque
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:  # Si hay colisiones
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':  # Si la colisión es con césped
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for leaf in range(randint(3, 6)):  # Genera partículas de hierba
                                self.animation_player.create_grass_particles(pos - offset, [self.visible_sprites])
                            target_sprite.kill()  # Mata el sprite de hierba
                        else:  # Si la colisión es con otro tipo de entidad (enemigos)
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        # Aplica daño al jugador
        if self.player.vulnerable:  # Si el jugador es vulnerable
            self.player.health -= amount  # Reduce la salud del jugador
            self.player.vulnerable = False  # Hace que el jugador no sea vulnerable temporalmente
            self.player.hurt_time = pygame.time.get_ticks()  # Marca el tiempo del daño recibido
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])  # Crea partículas de daño

    def trigger_death_particles(self, pos, particle_type):
        # Llama a las partículas de muerte para un enemigo o entidad
        self.animation_player.create_particles(particle_type, pos, self.visible_sprites)

    def add_exp(self, amount):
        # Agrega experiencia al jugador
        self.player.exp += amount

    def toggle_menu(self):
        # Cambia el estado del menú (pausado o no)
        self.game_paused = not self.game_paused

    def run(self):
        # Ejecuta la lógica principal del nivel
        self.visible_sprites.custom_draw(self.player)  # Dibuja los sprites visibles
        self.ui.display(self.player)  # Muestra la interfaz de usuario

        if self.game_paused:  # Si el juego está pausado, muestra las opciones de mejora
            self.upgrade.display()
        else:  # Si no está pausado, actualiza los sprites y la lógica de ataque
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # Configuración inicial del grupo de cámara
        super().__init__()
        self.display_surface = pygame.display.get_surface()  # Obtiene la superficie de la pantalla
        self.half_width = self.display_surface.get_size()[0] // 2  # Mitad del ancho de la pantalla
        self.half_height = self.display_surface.get_size()[1] // 2  # Mitad de la altura de la pantalla
        self.offset = pygame.math.Vector2()  # Vector de desplazamiento para la cámara

        # Crea la superficie del suelo
        self.floor_surf = pygame.image.load('../graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        # Dibuja los sprites, ordenados por su posición en el eje Y
        self.offset.x = player.rect.centerx - self.half_width  # Calcula el desplazamiento en X para centrar la cámara
        self.offset.y = player.rect.centery - self.half_height  # Calcula el desplazamiento en Y para centrar la cámara

        # Dibuja el fondo (suelo)
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # Dibuja los sprites visibles (ordenados por su centro en el eje Y)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        # Actualiza los enemigos
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)  # Actualiza cada enemigo
