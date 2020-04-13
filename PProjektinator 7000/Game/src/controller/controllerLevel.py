from src.controller.controller import Controller
from src.model.modelMenu import ModelMenu
from src.view.viewMenu import ViewMenu
from src.enum.command import Command
from src.enum.optionKey import OptionKey
import pygame as py


class ControllerLevel(Controller):

    def __init__(self):
        super().__init__()
        self._command = 0;

        #klawisze do sterowania
        self._go_right = ord('d')
        self._go_left = ord('a')
        self._jump = ord(' ')

        # strzelono - trzeba ponownie nacisnąć przycisk
        self._we_already_shooted = 0

        #odczytanie sterowania z pliku opcji
        self.read_steering_from_file()

    #przetwarzanie danych wejściowych
    def process_input(self):
        self._command &= ~Command.ATTACK
        for event in py.event.get():
            self._command = self._command & 0x7F;
            #wyłączenie strzelania

            #naciśnięcie X okna
            if event.type == py.QUIT:
                self._command = Command.EXIT

            #naciśnięcie klawisza klawiatury
            elif event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    self._command = Command.EXIT
                #skakanie
                elif event.key == self._jump:
                    self._command += Command.JUMP
                    self._command &= ~Command.CROUCH
                #kucanie
                elif event.key == py.K_s:
                    self._command += Command.CROUCH
                    self._command &= ~Command.JUMP
                #atak
                elif event.key == py.K_f:
                    if self._we_already_shooted == 0:
                        self._command += Command.ATTACK
                        self._we_already_shooted = 1
                #rozpoczęcie telekinezy
                elif event.key == py.K_r:
                    print("The force is strong with this one.\n")
                    self._command = Command.TELEKINESIS
                #poruszanie się lewo/prawo
                elif event.key == self._go_left:
                    self._command += Command.GO_LEFT
                    self._command &= ~Command.GO_RIGHT
                elif event.key == self._go_right:
                    self._command += Command.GO_RIGHT
                    self._command &= ~Command.GO_LEFT

            elif event.type == py.KEYUP:
                if event.key == self._go_left:
                    self._command &= ~Command.GO_LEFT
                elif event.key == self._go_right:
                    self._command &= ~Command.GO_RIGHT
                elif event.key == self._jump:
                    self._command &= ~Command.JUMP
                elif event.key == py.K_f:
                    # zwolniony przycisk -> można znowu strzelić
                    self._we_already_shooted = 0
                elif event.key == py.K_s:
                    self._command &= ~Command.CROUCH
                elif event.key == py.K_r:
                    self._command &= ~Command.TELEKINESIS
                    print("The force is NOT strong with this one.\n")

    #metoda pozwalająca przekazać model do widoku w celu jego wyrenderowania
    def communicateMV(self, model, view):
        view.set_player(model.get_player())
        view.set_all_sprites(model.get_all_sprites())

    def get_controls(self, view):
        self._controls = view.get_controls()

    def give_command(self, model):
        model.set_command(self._command)

    def read_steering_from_file(self):
        file = open('.\\saves\\opszyns.txt', 'r')
        
        # odczyt kolejnych linii
        for line in file:
            splitted_line = line.strip().split()
            int_optionKey = int(splitted_line[0])
            # dodanie informacji do tablicy opcji
            if int_optionKey == OptionKey.KEY_GO_LEFT:
                self._go_left = int(splitted_line[1])
                #self._steering.append((int(splitted_line[1]), Command.GO_LEFT))                
            elif int_optionKey == OptionKey.KEY_GO_RIGHT:                
                self._go_right = int(splitted_line[1])
                #self._steering.append((int(splitted_line[1]), Command.JUMP))                
            elif int_optionKey == OptionKey.KEY_JUMP:
                self._jump = int(splitted_line[1])
                #self._steering.append((int(splitted_line[1]), Command.GO_RIGHT))

        file.close()
