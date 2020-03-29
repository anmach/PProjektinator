from src.controller.controller import Controller
from src.model.modelMenu import ModelMenu
from src.view.viewMenu import ViewMenu
from src.enum.command import Command
import pygame as py


class controllerLevel(Controller):

    def __init__(self):
        super().__init__()

    #przetwarzanie danych wejściowych
    def process_input(self):
        for event in py.event.get():

            #naciśnięcie X okna
            if event.type == py.QUIT:
                self._command = Command.EXIT

            #naciśnięcie klawisza klawiatury
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._command = Command.EXIT
                #skakanie
                elif event.key == pygame.K_W:
                    self._command = Command.JUMP 
                #kucanie
                elif event.key == pygame.K_S:
                    self._command = Command.CROUCH
                #atak
                elif event.key == pygame.K_F:
                    self._command = Command.ATTACK
                #rozpoczęcie telekinezy
                elif event.key == pygame.K_R:
                    print("The force is strong with this one.\n")
                    self._command == Command.TELEKINESIS
                #poruszanie się lewo/prawo
                elif event.key == pygame.K_A:
                    self._command = Command.GO_LEFT
                elif event.key == pygame.K_D:
                    self._command = Command.GO_RIGHT                     

    def communicateMV(self, model, view):
        pass

    def get_controls(self, view):
        self._controls = view.get_controls()

    def give_command(self, model):
        model.set_command(self._command)

