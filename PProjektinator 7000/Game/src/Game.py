from src.programModes.menu import Menu
import pygame as py


def main():
    print('\nInicjalizacja pygame.\n')
    result = py.init()
    if result[1] == 0:
        print("Inicjalizacja przebiegła pomyślnie.") 

        #muzyka
        playlist = list()
        playlist.append ( ".\\res\\music\\EpicTVTheme.mp3" )
        playlist.append (".\\res\\music\\Assasins.mp3")

        py.mixer.music.load ( playlist.pop() )  
        py.mixer.music.queue ( playlist.pop() )
        py.mixer.music.play(-1)
            
        menu = Menu()
        menu.run()
    else:
        print("Liczba błędów: %i" %(result[1]))
        return

if __name__ == '__main__':
    main()
