class GameStats():
    """ Отслеживание статистики для игры """

    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()

        # запуск игры в неактивом состоянии
        self.game_active = False
        #рекорд игры
        self.high_score = 0

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры"""
        # оставшиеся корабли
        self.ships_left = self.ai_settings.ship_limit
        #очки игрока
        self.score = 0
        self.level = 0

