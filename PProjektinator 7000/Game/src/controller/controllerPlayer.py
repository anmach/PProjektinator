from src.controller.controller import Controller
from src.model.modelMenu import ModelMenu
from src.view.viewMenu import ViewMenu
from src.enum.command import Command
import pygame as py


class controllerPlayer(Controller):

    #przetwarzanie danych wejściowych
    def process_input(self):
        for event in py.event.get():

            #naciśnięcie X okna
            if event.type == py.QUIT:
                self._command = Command.EXIT

            #naciśnięcie klawisza klawiatury
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    print("Jump")
                    #TODO 
                if event.key == pygame.K_DOWN:
                    print("Crouch")
                    #TODO 
                if event.key == pygame.K_LEFT:
                    print("Go left")
                    #TODO
                if event.key == pygame.K_RIGHT:
                    print("Go right")
                    #TODO                          

    def communicateMV(self, model, view):
        pass

    def get_controls(self, view):
        pass

    def give_command(self, model):
        pass

