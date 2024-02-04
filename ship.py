import pygame
from pygame.sprite import Sprite



class Ship(Sprite):
  # """ Клас для керування кораблем """

  def __init__(self, ai_game):
    super().__init__()
    self.settings = ai_game.settings
    self.screen = ai_game.screen
    self.screen_rect = ai_game.screen.get_rect()

    self.image = pygame.image.load('img/ship.bmp')
    self.rect = self.image.get_rect()

    self.rect.midbottom = self.screen_rect.midbottom

    self.moving_left, self.moving_right  = False, False

    self.x = float(self.rect.x)
  


  def update(self):
    if self.moving_left and self.rect.left > 0:
      self.x -= self.settings.ship_speed
    elif self.moving_right and self.rect.right < self.screen_rect.right:
      self.x += self.settings.ship_speed

    self.rect.x = self.x


  def blime(self):
    self.screen.blit(self.image, self.rect)


  def center_ship(self):
   # ''' Центрує корабель на ерані '''
    self.rect.midbottom = self.screen_rect.midbottom
