
import pygame
import sys
class Button:
    def __init__(self, x, y, normal_image_path, hover_image_path):
        """
        Initialize the Button object.

        :param x: X-coordinate of the button.
        :param y: Y-coordinate of the button.
        :param normal_image_path: Path to the normal state image.
        :param hover_image_path: Path to the hover state image.
        """
        self.normal_image = pygame.image.load(normal_image_path)
        self.hover_image = pygame.image.load(hover_image_path)
        self.rect = self.normal_image.get_rect(topleft=(x, y))

    def draw(self, screen):
        """
        Draw the button on the screen.

        :param screen: The Pygame screen to draw the button on.
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            screen.blit(self.hover_image, self.rect)
        else:
            screen.blit(self.normal_image, self.rect)

    def is_clicked(self, event):
        """
        Check if the button is clicked.

        :param event: Pygame event object.
        :return: True if clicked, False otherwise.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            return True
        return False