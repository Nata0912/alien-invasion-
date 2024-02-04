import pygame
import sys
from time import sleep

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
  # """ Загальний Клас, що керує ресурсами та поведінкою гри."""
  # class AlienInvasion == = == class Game
  def __init__(self):
    """ Ініціалізувати гру, створити ресурси гри."""

    # Ініціалізація бібліотеки та її компонентів
    pygame.init()

    # Підключення налаштуваннь та
    self.settings = Settings()
    self.settings.initialize_settings()


    # Створити вікно  гри із заданими розмірами
    self.screen = pygame.display.set_mode(self.settings.screen_size, pygame.RESIZABLE)
    pygame.display.set_caption("Alien Invasion")


    self.ship = Ship(self)
    self.bullets = pygame.sprite.Group()
    self.aliens = pygame.sprite.Group()
    self._create_fleet()

    self.play_button = Button(self, "Play")
    self.stats = GameStats(self)
    self.sb = Scoreboard(self)


  def run_game(self):
    # ''' Головний цикл гри '''
    while True:
      self._check_events()

      if self.stats.game_active:
        self.ship.update()
        self._update_bullets()
        self._update_aliens()

      self._update_screen()
		

  def _check_events(self):
    # ''' Реагувати на події миші та клави '''
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
          self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
          self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
          self._fire_bullet()
          
      elif event.type == pygame.KEYUP:
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
          self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
          self.ship.moving_left = False

      elif event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        self._check_play_button(mouse_pos)
        

  def _check_play_button(self, mouse_pos):
    # ''' Розпочати нову гру коли користувач натисне кнопку play '''
    button_clicked = self.play_button.rect.collidepoint(mouse_pos)
    if button_clicked and not self.stats.game_active:
      # Повернути початкові налаштування швидкості
      self.settings.initialize_dynemic_settings()
      # Приховати курсор миші 
      pygame.mouse.set_visible(False)
      # Анулювати ігрову статистику
      self.stats.reset_stats()
      self.stats.game_active = True
      self.sb.prep_score()
      self.sb.prep_level()
      self.sb.prep_ships()

      # Позбутися прибульців та куль перед початком
      self.aliens.empty()
      self.bullets.empty()

      # Створити новий флот та відцентрувати корабель
      self._create_fleet()
      self.ship.center_ship()


  def _update_screen(self):
    #''' Оновити зображення на екрані '''
    # Задати колір колір екрану
    self.screen.fill((230, 230, 230))  
    
    # Відобразити корабель
    self.ship.blime() 

    # Відобразити кулі
    for bullet in self.bullets.sprites():
      bullet.draw_bullet()

    #  Відобразити рибульців
    self.aliens.draw(self.screen)

    # Намалювати інформацію про рахунок
    self.sb.show_score()

    # Намалювати кнопку якщот гра не активна
    if not self.stats.game_active:
      self.play_button.draw_button()

    # Оновити екран
    pygame.display.update() 


  def _fire_bullet(self):
    #''' Створити нову кулю та додати її в спрайт'''
    if len(self.bullets) < self.settings.bullets_allowed:
      new_bullet = Bullet(self)
      self.bullets.add(new_bullet)


  def _update_bullets(self):
   # ''' Курує відображенням куль'''
    # Відобразити кулю 
    self.bullets.update()

    # Позбутися куль що зникли 
    for bullet in self.bullets.copy():
      if bullet.rect.bottom <= 0:
        self.bullets.remove(bullet)

    # Якщо куля влучила в приблуду...
    self._check_bullet_alien_collisions()


  def _check_bullet_alien_collisions(self):
   # ''' Реагує на зіткнення куль з  приблудами '''
    # Перевірити чи є влучання, якщо є позбутися і кулі і приблуди
    collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

    if collisions:
      for aliens in collisions.values():
        self.stats.score += self.settings.alien_points * len(aliens)
      self.sb.prep_score()
      self.sb.check_high_score()

    # якщо прибульців немає(усіх відстріляли)...
    if not self.aliens:
      # Позбуваємося випущених куль і створюєм новий флот
      self.bullets.empty()
      self._create_fleet()
      self.settings.increase_speed()

      # збільшити рівень
      self.stats.level += 1
      self.sb.prep_level()


  def _create_fleet(self):
    #''' Створює флот прибульців'''
    # Створити пибульця
    alien = Alien(self)
    # Отримати розміри прибульця
    alien_width, alien_height = alien.rect.size
    # Розраховуєм доступний простір по ШИРИНІ
    aviable_space_x = self.settings.screen_width - (2 * alien_width)
    # Розраховуєм кількість прибульців в ряді
    number_aliens_x = aviable_space_x // (2 * alien_width)
    
    # Отримати розмір корабля 
    # (нам треба залишити цей простір вільним,
    #  щоб корабель міг рухатись)
    ship_height = self.ship.rect.height
    # Розраховуєм доступний простір по ВИСОТІ
    aviable_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
    # Кількість рядів приблуд, або ж кільсть приблуд у стопчику
    number_rows =  aviable_space_y // (2 * alien_height)

    # Створити флот приблуд
    for row_number in range(number_rows):
      for alien_number in range(number_aliens_x):
        self._create_alien(alien_number, row_number)


  def _create_alien(self, alien_number, row_number):
    #'''Створює прибульця та додає його в флот'''
    alien = Alien(self)
    alien_width, alien_height = alien.rect.size
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    self.aliens.add(alien)


  def _check_fleet_edges(self):
   # ''' Перевіряє чи якийсь із приблуд не досяг краю'''
    for alien in self.aliens.sprites():
      if alien.check_edges():
        self._change_fleet_direction()
        break


  def _check_aliens_bottom(self):
    #''' Перевіряє чи не досягля якась приблуда дна '''
    screen_rect = self.screen.get_rect()
    for alien in self.aliens.sprites():
      if alien.rect.bottom >= screen_rect.bottom:
      # Реагуєм так ніби корабкль підбито
        self._ship_hit()
        break


  def _change_fleet_direction(self):
    #''' Керує напрямком руху всього флоту'''
    for alien in self.aliens.sprites():
      alien.rect.y += self.settings.fleet_drop_speed
    self.settings.fleet_direction *= -1


  def _update_aliens(self):
    #'''Перевіряє чи не досягля якась проиблуда краю екрану, після оновлює позиції приблуд на екрані'''
    self._check_fleet_edges()
    self.aliens.update()

    #Перевіряєм чи не зіткнувся корабель з приблудами
    if pygame.sprite.spritecollideany(self.ship, self.aliens):
      self._ship_hit()

    self._check_aliens_bottom()
  

  def _ship_hit(self):
   # ''' Реагує на зіткнення приблуди з кораблем '''
    if self.stats.ships_left > 0:
      # Зменшити Кількість Життів та оновити табло
      self.stats.ships_left -= 1
      self.sb.prep_ships()
      # Очистити екран від приблуд і куль
      self.aliens.empty()
      self.bullets.empty()
      # Створити нову сесію (новий флот, корабель занову по йентрі екрану)
      self.ship.center_ship()
      self._create_fleet()
      # Пауза
      sleep(0.5)
    else:
      self.stats.game_active = False
      pygame.mouse.set_visible(True)

   



if __name__ == '__main__':
  ai = AlienInvasion()
  ai.run_game()