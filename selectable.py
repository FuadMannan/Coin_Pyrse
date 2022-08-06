from abc import ABC, abstractmethod
from command import *


class Selectable(ABC):
    def __init__(self, description):
        self.description = description

    def display(self):
        return self.description

    @abstractmethod
    def select(self):
        pass


class Menu(Selectable):
    def __init__(self, description, selectable_list):
        super().__init__(description)
        self.items = selectable_list

    def select(self):
        print(f'{self.display()} Menu\n')
        i = 1
        for x in self.items:
            print(f'{i}) {x.display()}')
        print()
        choice = int(input('Selection: '))
        self.items[choice].select()


class MenuItem(Selectable):
    def __init__(self, description, command: MenuCommand):
        super().__init__(description)
        self.__command = command

    def select(self):
        self.__command.execute()
