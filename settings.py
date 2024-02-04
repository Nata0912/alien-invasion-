import pygame

class Settings:
    # """ Параметри та налаштування гри"""

  def __init__(self):
    # """Ініціалізує постійні налаштування гри."""

    #  Screen 
    self.screen_size = self.screen_width, self.screen_height = 0, 0 
    self.bg_color = (230, 230, 230)

    # Ship
    self.ship_limit = 3

    # Bullet 
    self.bullet_width = 1
    self.bullet_height = 15
    self.bullet_color = (60, 60, 60)
    self.bullets_allowed = 3

    # Alien 
    self.fleet_drop_speed = 10

    # Як швидко гра має прискорюватися
    self.speedup_scale = 1.1

    # Як швидко хбільшується вартість приблуд
    self.score_scale = 1.5

    self.initialize_dynemic_settings()

  def initialize_settings(self):
    # отримуємо інформацію про дисплей
    infoObject = pygame.display.Info()
    # встановлюємо розміри екрану
    self.screen_size = self.screen_width, self.screen_height = infoObject.current_w, infoObject.current_h - 70

  def initialize_dynemic_settings(self):
    # ''' Ініціалізація змінних налаштувань'''
    self.ship_speed = 1.5
    self.bullet_speed = 3.0
    self.alien_speed = 1.0

    # fleet_direction -- напрямок руху флоту; 
    #  1 -- рух праворуч, 
    # -1 --рух ліворуч
    self.fleet_direction = 1

    self.alien_points = 50

  def increase_speed(self):
    # ''' Збільшення налаштувань швидкості '''
    self.ship_speed *= self.speedup_scale
    self.bullet_speed *= self.speedup_scale
    self.alien_speed *= self.speedup_scale

    self.alien_points = int(self.alien_points * self.score_scale)
