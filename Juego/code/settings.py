# game setup
WIDTH    = 1280  # Ancho de la ventana del juego en píxeles
HEIGTH   = 720   # Altura de la ventana del juego en píxeles
FPS      = 60    # Número de cuadros por segundo (frames per second)
TILESIZE = 64    # Tamaño de cada celda del mapa en píxeles (relacionado con el tamaño de los tiles)
HITBOX_OFFSET = {  # Desplazamientos de la hitbox para diferentes tipos de entidades.
    'player': -26,   # Desplazamiento para la hitbox del jugador (ajuste para la precisión de colisiones)
    'object': -40,   # Desplazamiento para los objetos
    'grass': -10,    # Desplazamiento para la hierba
    'invisible': 0   # Sin desplazamiento para objetos invisibles (por ejemplo, zonas no interactivas)
}

# ui (Interfaz de usuario)
BAR_HEIGHT = 20  # Altura de las barras de la interfaz (por ejemplo, barras de salud/energía)
HEALTH_BAR_WIDTH = 200  # Ancho de la barra de salud en píxeles
ENERGY_BAR_WIDTH = 140  # Ancho de la barra de energía en píxeles
ITEM_BOX_SIZE = 80  # Tamaño de los cuadros que muestran los objetos en la UI
UI_FONT = '../graphics/font/joystix.ttf'  # Ruta a la fuente utilizada en la interfaz de usuario
UI_FONT_SIZE = 18  # Tamaño de la fuente para los textos de la interfaz de usuario

# general colors (Colores generales para la interfaz)
WATER_COLOR = '#71ddee'  # Color de fondo para las zonas de agua
UI_BG_COLOR = '#222222'  # Color de fondo de la interfaz de usuario
UI_BORDER_COLOR = '#111111'  # Color de los bordes de la interfaz
TEXT_COLOR = '#EEEEEE'  # Color del texto de la interfaz de usuario

# ui colors (Colores específicos para diferentes elementos de la UI)
HEALTH_COLOR = 'red'  # Color de la barra de salud
ENERGY_COLOR = 'blue'  # Color de la barra de energía
UI_BORDER_COLOR_ACTIVE = 'gold'  # Color de los bordes activos en la interfaz de usuario (cuando un elemento está seleccionado)

# upgrade menu (Menú de mejora de atributos)
TEXT_COLOR_SELECTED = '#111111'  # Color del texto cuando una opción está seleccionada en el menú de mejora
BAR_COLOR = '#EEEEEE'  # Color de las barras en el menú de mejora
BAR_COLOR_SELECTED = '#111111'  # Color de las barras cuando están seleccionadas en el menú de mejora
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'  # Color de fondo para las opciones seleccionadas en el menú de mejora

# weapons (Datos de las armas)
weapon_data = {  # Diccionario que contiene los datos de las armas disponibles en el juego
    'sword': {'cooldown': 100, 'damage': 15, 'graphic': '../graphics/weapons/sword/full.png'},  # Datos del arma 'sword'
    'lance': {'cooldown': 400, 'damage': 30, 'graphic': '../graphics/weapons/lance/full.png'},  # Datos del arma 'lance'
    'axe': {'cooldown': 300, 'damage': 20, 'graphic': '../graphics/weapons/axe/full.png'},  # Datos del arma 'axe'
    'rapier': {'cooldown': 50, 'damage': 8, 'graphic': '../graphics/weapons/rapier/full.png'},  # Datos del arma 'rapier'
    'sai': {'cooldown': 80, 'damage': 10, 'graphic': '../graphics/weapons/sai/full.png'}  # Datos del arma 'sai'
}

# magic (Datos de las magias)
magic_data = {  # Diccionario que contiene los datos de las magias disponibles en el juego
    'flame': {'strength': 5, 'cost': 20, 'graphic': '../graphics/particles/flame/fire.png'},  # Datos de la magia 'flame'
    'heal': {'strength': 20, 'cost': 10, 'graphic': '../graphics/particles/heal/heal.png'}  # Datos de la magia 'heal'
}

# enemy (Datos de los enemigos del juego)
monster_data = {  # Diccionario con los datos de los monstruos enemigos
    'squid': {  # Datos del enemigo 'squid' (calamar)
        'health': 100,  # Salud del enemigo
        'exp': 100,  # Experiencia otorgada al derrotar al enemigo
        'damage': 20,  # Daño que inflige el enemigo
        'attack_type': 'slash',  # Tipo de ataque (en este caso 'slash' = corte)
        'attack_sound': '../audio/attack/slash.wav',  # Ruta al sonido del ataque
        'speed': 3,  # Velocidad de movimiento del enemigo
        'resistance': 3,  # Resistencia a los daños del enemigo
        'attack_radius': 80,  # Radio de ataque del enemigo (rango en el que inflige daño)
        'notice_radius': 360  # Radio de detección del enemigo (rango en el que el enemigo puede detectar al jugador)
    },
    'raccoon': {  # Datos del enemigo 'raccoon' (mapache)
        'health': 300,
        'exp': 250,
        'damage': 40,
        'attack_type': 'claw',
        'attack_sound': '../audio/attack/claw.wav',
        'speed': 2,
        'resistance': 3,
        'attack_radius': 120,
        'notice_radius': 400
    },
    'spirit': {  # Datos del enemigo 'spirit' (espíritu)
        'health': 100,
        'exp': 110,
        'damage': 8,
        'attack_type': 'thunder',
        'attack_sound': '../audio/attack/fireball.wav',
        'speed': 4,
        'resistance': 3,
        'attack_radius': 60,
        'notice_radius': 350
    },
    'bamboo': {  # Datos del enemigo 'bamboo' (bambú)
        'health': 70,
        'exp': 120,
        'damage': 6,
        'attack_type': 'leaf_attack',
        'attack_sound': '../audio/attack/slash.wav',
        'speed': 3,
        'resistance': 3,
        'attack_radius': 50,
        'notice_radius': 300
    }
}
