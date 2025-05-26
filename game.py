import pygame
import sys


class Game:
    def __init__(self, width_height, title="Untitled"):
        pygame.init()

        self.width, self.height = width_height
        self.title = title
        self.screen = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption(self.title)
        self.running = True
        self.observers = []

    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            for observer in self.observers:
                observer.handle_event(self.screen, event)

    def add_observer(self, observer):
        self.observers.append(observer)

    def draw(self):
        self.screen.fill((255, 255, 255))

        for observer in self.observers:
            observer.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()

        self.quit()

    def quit(self):
        pygame.quit()
        sys.exit()
