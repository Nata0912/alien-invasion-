import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
  ''' Клас що пребставляє прибульців '''

  def __init__(self, ai_game):
    ''' Ініціалізувати прибульця та його початкові кординати'''
    super().__init__()
    self.screen = ai_game.screen
    self.settings = ai_game.settings

    self.image = pygame.image.load('img/alien.bmp')
    self.rect = self.image.get_rect()
    
    self.rect.x = self.rect.width
    self.rect.y = self.rect.height

    self.x = float(self.rect.x)


  def check_edges(self):
    ''' Повертає істину якщо приблуда знаходиться на краю екрану'''
    screen_rect = self.screen.get_rect()
    if self.rect.right >= screen_rect.right or self.rect.left <= 0:
      return True


  def update(self):
    '''  Керую переміщенням приблуди'''
    self.x += self.settings.alien_speed * self.settings.fleet_direction
    self.rect.x = self.x
  

  