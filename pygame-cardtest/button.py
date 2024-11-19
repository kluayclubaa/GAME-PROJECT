
import pygame
import sys
class Button:
    def __init__(self, x, y, normal_image_path, hover_image_path,resizex,resizey):
        
        self.normal_image = pygame.image.load(normal_image_path)
        self.hover_image = pygame.image.load(hover_image_path)
        self.resizx = resizex
        self.resizey = resizey

        
        
        self.rect = self.normal_image.get_rect(topleft=(x, y))
        
    def draw(self, screen):
       
        mouse_pos = pygame.mouse.get_pos()
        self.normal_image = pygame.transform.smoothscale(self.normal_image, (self.resizx, self.resizey))
        self.hover_image = pygame.transform.smoothscale(self.hover_image, (self.resizx, self.resizey))
        if self.rect.collidepoint(mouse_pos):

            screen.blit(self.normal_image, self.rect)
        else:
            screen.blit(self.hover_image, self.rect)

    def is_clicked(self, event):
   
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            return True
        return False