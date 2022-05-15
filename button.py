#импорт шрифтов
import pygame.font

class Button():
    def __init__(self, ai_settings, display, msg):
        """Инициализируем атрибуты кнопок"""
        self.display = display
        self.display_rect = display.get_rect()

        #Назначение размеров и свойств кнопок
        self.width = 200
        self.height = 50
        self.button_color = (0, 225, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        #построение объекта rect кнопки и выравнивание по центру экрана
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center=self.display_rect.center

        #создание сообшения кнопки (создаётся только 1 раз)
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Преобразует msg в прямоугольник и выравнивает текст по центру"""

        #преобразует текст в изображение
        self.msg_image=self.font.render(msg, True, self.text_color, self.button_color)
        #преобразует изображение в прямоугльник
        self.msg_image_rect=self.msg_image.get_rect()
        #отцентровка текста
        self.msg_image_rect.center=self.rect.center

    def draw_button(self):
        #Отображение пустой кнопки и вывод сообщения
        self.display.fill(self.button_color, self.rect)
        self.display.blit(self.msg_image, self.msg_image_rect)

