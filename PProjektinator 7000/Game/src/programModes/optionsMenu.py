from .programMode import ProgramMode
from src.model.modelOptions import ModelOptions
from src.view.viewOptions import ViewOptions
from src.controller.controllerOptions import ControllerOptions
from src.enum.command import Command
import pygame as py

class OptionsMenu(ProgramMode):
    def __init__(self, display):
        self._model = ModelOptions()
        self._view = ViewOptions(display, self._model.get_options())
        self._controller = ControllerOptions()

    def change_mode(self):
       pass
