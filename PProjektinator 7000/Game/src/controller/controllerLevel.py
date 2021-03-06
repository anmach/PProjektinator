from src.controller.controller import Controller
from src.controller.controllerBCI import ControllerBCI
from src.model.modelMenu import ModelMenu
from src.view.viewMenu import ViewMenu
from src.enum.command import Command
from src.enum.optionKey import OptionKey
import pygame as py
import src.define as define


class ControllerLevel(Controller):

    def __init__(self):
        super().__init__()

        self._command = 0;

        #klawisze do sterowania
        self._key_go_right = ord('d')
        self._key_go_left = ord('a')
        self._key_jump = ord(' ')
        self._key_crouch = ord('s')
        self._key_attack = ord('f')
        self._key_telekinesis = ord('r')
        self._key_go_up = ord('w')
        self._key_pause = ord('p')

        self._blink_enable = 0
        self.telekinesis_on = 0

        #odczytanie sterowania z pliku opcji
        self.read_steering_from_file()

        if(self._blink_enable == 1):            
           self.__controlBCI = ControllerBCI('192.168.4.1')

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
                elif event.key == self._key_pause:
                    self._command |= Command.PAUSE
                #skakanie
                elif event.key == self._key_jump:
                    self._command += Command.JUMP
                    self._command &= ~Command.CROUCH
                #kucanie
                elif event.key == self._key_crouch:
                    self._command += Command.CROUCH
                    self._command &= ~Command.JUMP
                #atak
                elif event.key == self._key_attack:
                    self._command |= Command.ATTACK
                #rozpoczęcie telekinezy
                elif event.key == self._key_telekinesis:
                    self.telekinesis_on = 1
                    if(self._blink_enable == 1): 
                        self.__controlBCI.start_reading()
                    self._command = Command.TELEKINESIS
                #poruszanie się lewo/prawo
                elif event.key == self._key_go_left:
                    self._command += Command.GO_LEFT
                    self._command &= ~Command.GO_RIGHT
                elif event.key == self._key_go_right:
                    self._command += Command.GO_RIGHT
                    self._command &= ~Command.GO_LEFT
                elif event.key == self._key_go_up:
                    self._command += Command.GO_UP

            elif event.type == py.KEYUP:
                if event.key == self._key_go_left:
                    self._command &= ~Command.GO_LEFT
                elif event.key == self._key_go_right:
                    self._command &= ~Command.GO_RIGHT
                elif event.key == self._key_crouch:
                    self._command &= ~Command.CROUCH
                elif event.key == self._key_telekinesis:
                    self._command &= ~Command.TELEKINESIS
                    self.telekinesis_on = 0
                    if(self._blink_enable == 1): 
                        self.__controlBCI.stop_reading()
                elif event.key == self._key_go_up:
                    self._command &= ~Command.GO_UP

        if(self.telekinesis_on == 1 & self._blink_enable == 1):
            self._command = self.controlBCI.get_instruction()


    #metoda pozwalająca przekazać model do widoku w celu jego wyrenderowania
    def communicateMV(self, model, view):
        view.set_player(model.get_player())
        view.set_all_sprites(model.get_all_sprites())
        view.set_paused(model.is_paused())
        view.set_gameover(model.is_gamover())
        view.set_won(model.is_won())
        view.set_camera(model.get_camera())

    def get_controls(self, view):
        self._controls = view.get_controls()

    # ustawienie czy kwadraciki mają migać
    def set_blink(self, view):
        view.set_blink_enabled(self._blink_enable)

    def give_command(self, model):
        model.set_command(self._command)
        self._command &= ~Command.JUMP
        self._command &= ~Command.ATTACK
        self._command &= ~Command.PAUSE

    def read_steering_from_file(self):
        file = open(define.get_options_file_path(), 'r')
        
        # odczyt kolejnych linii
        for line in file:
            splitted_line = line.strip().split()
            int_optionKey = int(splitted_line[0])
            # dodanie informacji do tablicy opcji
            if int_optionKey == OptionKey.KEY_GO_LEFT:
                self._key_go_left = int(splitted_line[1])             
            elif int_optionKey == OptionKey.KEY_GO_RIGHT:                
                self._key_go_right = int(splitted_line[1])             
            elif int_optionKey == OptionKey.KEY_JUMP:
                self._key_jump = int(splitted_line[1])
            if int_optionKey == OptionKey.KEY_CROUCH:
                self._key_crouch = int(splitted_line[1])             
            elif int_optionKey == OptionKey.KEY_ATTACK:                
                self._key_attack = int(splitted_line[1])             
            elif int_optionKey == OptionKey.KEY_TELEKINESIS:
                self._key_telekinesis = int(splitted_line[1])
            elif int_optionKey == OptionKey.BLINKING_RECT:
                blink = int(splitted_line[1])
                if blink == 1:
                    self._blink_enable = 1
                else:
                    self._blink_enable = 0

        file.close()
