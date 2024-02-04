import pygame.font  

class Button:
  def __init__(self, ai_game, msg):
    ''' Ініціалізація Атрибутів Кнопки'''
    self.screen = ai_game.screen
    self.screen_rect = self.screen.get_rect()

    # Задати розміри та властивості кнопки
    self.widt, self.height = 200, 50
    self.button_color = (0, 255, 0)
    self.text_color = (255, 255, 255)
    self.font = pygame.font.SysFont(None, 48)

    # Створити об'єкт rect кнопки та відцентрувати його
    self.rect = pygame.Rect(0, 0, self.widt, self.height)
    self.rect.center = self.screen_rect.center

    # Повідомлення на кнопці треба показати лише один раз
    self._prep_msg(msg)

  def _prep_msg(self, msg):
    ''' Перетворює текст на зображення та розміщає його по центру кнопки'''
    self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
    self.msg_image_rect = self.msg_image.get_rect()
    self.msg_image_rect.center = self.rect.center


  def draw_button(self):
    ''' Намалювати порожню кнопку а тоді -- повідомлення '''
    self.screen.fill(self.button_color, self.rect)
    self.screen.blit(self.msg_image, self.msg_image_rect)