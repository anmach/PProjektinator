from src.controller.controller import Controller
from src.model.modelMenu import ModelMenu
from src.view.viewMenu import ViewMenu
from src.enum.command import Command
import pygame as py


class ControllerLevel(Controller):

    def __init__(self):
        super().__init__()
        self._command = 0;

    #przetwarzanie danych wejściowych
    def process_input(self):
        for event in py.event.get():
            
            self._command = self._command & 0x7F;

            #naciśnięcie X okna
            if event.type == py.QUIT:
                self._command = Command.EXIT

            #naciśnięcie klawisza klawiatury
            elif event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    self._command = Command.EXIT
                #skakanie
                if event.key == py.K_SPACE:
                    self._command += Command.JUMP 
                #kucanie
                if event.key == py.K_s:
                    self._command += Command.CROUCH
                #atak
                if event.key == py.K_f:
                    self._command += Command.ATTACK
                #rozpoczęcie telekinezy
                if event.key == py.K_r:
                    print("The force is strong with this one.\n")
                    self._command += Command.TELEKINESIS
                #poruszanie się lewo/prawo
                if event.key == py.K_a:
                    self._command += Command.GO_LEFT
                if event.key == py.K_d:
                    self._command += Command.GO_RIGHT
            elif event.type == py.KEYUP:
                #poruszanie się lewo/prawo
                if event.key == py.K_a:
                    self._command -= Command.GO_LEFT
                if event.key == py.K_d:
                    self._command -= Command.GO_RIGHT
                if event.key == py.K_SPACE:
                    self._command -= Command.JUMP

    #metoda pozwalająca przekazać model do widoku w celu jego wyrenderowania
    def communicateMV(self, model, view):
        view.set_player(model.get_player())
        view.set_all_sprites(model.get_all_sprites())

    def get_controls(self, view):
        self._controls = view.get_controls()

    def give_command(self, model):
        model.set_command(self._command)

