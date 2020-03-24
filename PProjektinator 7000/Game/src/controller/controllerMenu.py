from src.controller.controller import Controller
from src.model.modelMenu import ModelMenu
from src.view.viewMenu import ViewMenu
from src.enum.command import Command
import pygame as py


class ControllerMenu(Controller):

    #przetwarzanie danych wejściowych
    def processInput(self):
        for event in py.event.get():

            #naciśnięcie X okna
            if event.type == py.QUIT:
                self._command = Command.EXIT

            #kliknięcie myszką
            if event.type == py.MOUSEBUTTONDOWN:
                for control in self._controls:
                    #sprawdzanie czy nad daną kontrolką jest kursor
                    if control.getIsFocused():
                        self._command = control.getCommand()
            else:
                self._command = Command.CONTINUE
            

    #w menu nie ma potrzeby przekazywania modelu do widoku
    def communicateMV(self, model, view):
        pass

    def getControls(self, view):
        self._controls = view.getControls()

    def giveCommand(self, model):
        model.setCommand(self._command)