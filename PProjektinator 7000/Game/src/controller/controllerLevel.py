from src.controller.controller import Controller
from src.model.modelMenu import ModelMenu
from src.view.viewMenu import ViewMenu
from src.enum.command import Command
import pygame as py


class ControllerLevel(Controller):

    def __init__(self):
        super().__init__()

    #przetwarzanie danych wejściowych
    def process_input(self):
        for event in py.event.get():

            #naciśnięcie X okna
            if event.type == py.QUIT:
                self._command = Command.EXIT

            #naciśnięcie klawisza klawiatury
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    self._command = Command.EXIT
                #skakanie
                elif event.key == py.K_SPACE:
                    self._command = Command.JUMP 
                #kucanie
                elif event.key == py.K_s:
                    self._command = Command.CROUCH
                #atak
                elif event.key == py.K_f:
                    self._command = Command.ATTACK
                #rozpoczęcie telekinezy
                elif event.key == py.K_r:
                    print("The force is strong with this one.\n")
                    self._command == Command.TELEKINESIS
                #poruszanie się lewo/prawo
                elif event.key == py.K_a:
                    self._command = Command.GO_LEFT
                elif event.key == py.K_d:
                    self._command = Command.GO_RIGHT                     

    #metoda pozwalająca przekazać model do widoku w celu jego wyrenderowania
    def communicateMV(self, model, view):
        view.set_player(model.get_player())
        view.set_all_sprites(model.get_all_sprites())

    def get_controls(self, view):
        self._controls = view.get_controls()

    def give_command(self, model):
        model.set_command(self._command)

