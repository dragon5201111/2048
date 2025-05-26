from abc import ABC, abstractmethod


class DrawableObserver(ABC):

    @abstractmethod
    def draw(self, surface):
        pass

    @abstractmethod
    def handle_event(self, surface, event):
        pass
