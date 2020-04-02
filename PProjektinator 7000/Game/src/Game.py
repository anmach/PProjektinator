from src.programModes.menu import Menu
import pygame as py


def main():
    print('\nInicjalizacja pygame.\n')
    result = py.init()
    if result[1] == 0:
        print("Inicjalizacja przebiegła pomyślnie.") 
    
        menu = Menu()
        menu.run()
    else:
        print("Liczba błędów: %i" %(result[1]))
        return

if __name__ == '__main__':
    main()
