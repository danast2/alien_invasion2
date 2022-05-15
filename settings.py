#класс с настройками игры
class Settings:
    def __init__(self):
        """Инициализирует статические настройки игры"""

        #атрибуты экрана
        self.display_width = 1200
        self.display_height = 800

        #цвет бэкграунда
        self.bg_color = (230,230,230)
        #название
        self.caption="Инопланетное вторжение"

        #Максимальное количетво кораблей
        self.ship_limit = 2

        self.bullet_width = 3
        self.bullet_hight = 15
        self.bullet_color = 60, 60, 60
        #максимально разрешённое количество пуль
        self.bullets_allowed=3

        #величина снижения флота пришельцев вниз (при достижении ими края)
        self.fleet_drop_speed = 100
        #Темп ускорения игры
        self.speedup_scale = 1.1

        #Темп роста стоимости пришельца
        self.score_scale = 1.5
        #функция вызывающая изменяемые настройки игры
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инициализирует настройки,изменяющиеся в ходе игры"""
        # атрибут скорости корабля
        self.ship_speed_factor = 1.5
        # атрибуты пули
        self.bullet_speed_factor = 3
        # скорость пришельца
        self.alien_speed_factor = 1

        # fleet_direction = 1 - обозначает направление вправо (-1 обозначает движение влево)
        self.fleet_direction = 1

        #Подсчёт очков(за 1 убитого пришельца)
        self.alien_points = 100

    def increase_speed(self):
        """Увеличивает настройки скорости и стоимости за убийство пришельца"""
        #увеличение скорости
        self.ship_speed_factor*=self.speedup_scale
        self.bullet_speed_factor*=self.speedup_scale
        self.alien_speed_factor*=self.speedup_scale

        #увеличение стоимости пришельца
        self.alien_points = int(self.alien_points*self.score_scale)
        print(self.alien_points)

