import pygame, sys
from button import Button # esto sirve para importar la funcionalidad de los botoness

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menú")

BG = pygame.image.load("Imagenes/Background.png")

def get_font(size): #el get_font sirve para cargar una fuente especifica desde un carchivo
    return pygame.font.Font("Imagenes/font.ttf", size) #aqui devuelve un objeto tipo fond para usar texto en pantalla
                                                        #el size define que grande sera la fuente


def Jugar():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos() #sirve para detectar donde esta el mouse dentro de la ventana

        SCREEN.fill("black") #el fill sirve para colorear toda una ventana

        PLAY_TEXT = get_font(45).render("No se poner el juego", True, "White") #el get_font es para cargar una fuente de tamaño 45 el //.render es un metodo para las superficies de texto el true pone suavisado en el texto//
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260)) #esto es para crear un rectangulo asociado al texto rendericado y ponerlo en las coordenadas 640,260
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460), 
                            text_input="Salir", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()
    
def Opciones():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()  #sirve para detectar donde esta el mouse dentro de la ventana

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("Opciones de ventana.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="Atras", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("Menú", True, "#b68f40") # get_font para tener una fuente tamaño 100 # el .render renderiza el texto menu con suavizado
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100)) #aqui hago un rectangulo asociado al texto para posicionarlo en la mitad

        PLAY_BUTTON = Button(image=pygame.image.load("Imagenes/Play Rect.png"), pos=(640, 250), 
                            text_input="Jugar", font=get_font(75), base_color="#d7fcd4", hovering_color="White")# el hovering color es para que cuando se ponga el raton por encima cambie de color a blanco
        OPTIONS_BUTTON = Button(image=pygame.image.load("Imagenes/Options Rect.png"), pos=(640, 400), # el text_input define donde aparece el boton
                            text_input="Opciones", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("Imagenes/Quit Rect.png"), pos=(640, 550), 
                            text_input="Salir", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT) #esto dibuja el titulo menu en la pantalla

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:#dibuja los botones y cambia los colores si esta encima
            button.changeColor(MENU_MOUSE_POS) 
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    Jugar()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    Opciones()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()