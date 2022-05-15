import pygame.font

from pygame.sprite import Group
from ship import Ship


class Scoreboard():
    '''Класс для вывода информации об очках игрока'''

    def __init__(self, ai_settings, display, stats):
        """Инициализирует атрибуты подсчёта очков"""

        self.display = display
        self.display_rect = display.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # Настройки шрифта для вывода счёта
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        # Подготовка исходного изображения текущего счёта
        self.prep_score()
        # Подготовка исходного изображения рекорда
        self.prep_high_score()
        # подготовка исходного изображения уровня
        self.prep_level()
        # подготовка вывод кол-ва оставшихся корблей
        self.prep_ships()

    def prep_score(self):
        """Преобразует текущий счёт в графическое изображение"""
        # функция round() округляет число (<число которое нужно округлить>,<сколько цифр после запятой>)
        rounded_score = round(self.stats.score, -1)
        # директива форматирования строки в python вставить запятые при преобразовании числового значения в строку
        # например,чтобы выводить не 1000000 , а 1,000,000
        score_str = "{:,}".format(rounded_score)

        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        # Вывод счёта в правой верхней части экрана
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.display_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Преобразует рекордный счёт в исходное изображение"""
        # округление до десятков
        high_score = round(self.stats.high_score, -1)
        # форматированеи щапятыми
        high_score_str = "{:,}".format(high_score)
        # превращение в картинку
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)

        self.high_score_rect = self.high_score_image.get_rect()
        # выравнивание рекорда
        self.high_score_rect.centerx = self.display_rect.centerx
        self.high_score_rect.top = self.display_rect.top

    def prep_level(self):
        """Преобразует уровень в графическое изображение"""
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        # выравниваение уровня снизу от текущего счёта
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Сообщает кол-во оставшихся кораблей"""
        self.ships = Group
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.display)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            # заполняем группу кораблей,которых нужно нарисовать,из оставшихся (кол-во оставшихся корблей изменяется оп ходу игры)
            self.ships.add(ship)

    def show_score(self):
        """Выводит счёт на экран + рекорд + текущий уровень """
        # вывод текущего счёта
        self.display.blit(self.score_image, self.score_rect)
        # вывод рекордного счёта
        self.display.blit(self.high_score_image, self.high_score_rect)
        # вывод уровня
        self.display.blit(self.level_image, self.level_rect)
        # вывод оставшихся кораблей(оставшихся жизней)
        # self.ships.draw(self, self.display)
