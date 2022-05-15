# модуль для хранения функций игры

import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def fire_bullet(ai_settings, bulets, display, ship):
    """Выпускает пулю, если максимум ещё не достигнут"""
    if len(bulets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, display, ship)
        bulets.add(new_bullet)


def check_keydown_events(event, ai_settings, display, ship, bulets):
    """ идёт проверка на то,какая клавиша нажата:"""
    if event.key == pygame.K_RIGHT:
        # если клавиша ВПРАВО была нажата,то мы присваиваем переменной ship.moving_right значение True
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # если клавиша ВЛЕВО была нажата,то мы присваиваем переменной ship.moving_left значение True
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, bulets, display, ship)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        # если клавиша ВПРАВО была отпущена,то мы присваиваем переменной ship.moving_right значение False
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        # если клавиша ВЛЕВО была отпущена,то мы присваиваем переменной ship.moving_left значение False
        ship.moving_left = False


def check_events(ai_settings, display, stats, sb, play_button, ship, aliens, bullets):
    """Проверка событий"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # если клавиша нажата,то:
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, display, ship, bullets)
        # если клавиша отпущена,то:
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # возвращает кортеж с координатами x,y
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, display, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, display, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Запускает новую игру при нажатии кнопки Play"""
    # В переменная bool типа, если человек нажал на прямоугольник кнопки,то True
    button_cklicked = play_button.rect.collidepoint(mouse_x, mouse_y)

    # если игрок нажал на кнопку + обратное значение stats.game_active
    if button_cklicked and not stats.game_active:
        # сброс всех изменённых настроек
        ai_settings.initialize_dynamic_settings()

        # после запуска/перезапуска игры,мы делаем мышку невидимой
        pygame.mouse.set_visible(False)

        # сброс игровой статистики
        stats.reset_stats()
        # активируем игру
        stats.game_active = True

        #Сброс изображения текущего счёта, рекордного счёта, текущего уровня, оставшихся кораблей
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()


        # обнуление списков пришельцев и пуль
        aliens.empty()
        bullets.empty()

        # Создание флота и отцентровка пришельца
        create_fleet(ai_settings, display, aliens, ship)
        ship.center_ship()


def update_screen(ai_settings, display, stats, sb, ship, aliens, bullets, play_button):
    """Обновляет изображения на экране и отображает новый экран,
    при каждом проходе главного цикла перерисовывается экран"""
    display.fill(ai_settings.bg_color)

    # проход циклом по группе bullets и отрисовке каждого из его элементов
    for bullet in bullets:
        bullet.draw_bullet()

    # отрисовка корбля
    ship.blitme()

    # отрисовка пришельцев
    aliens.draw(display)

    # вывод счёта
    sb.show_score()

    # изначально game_active = False (кнопка рисется при значении True), если кнопку нажали,
    # то game_active = True (теперь из-за условия,кнопка будет рисоваться при False),
    # game_active = False,принмает значение,когда ship_hit(наступает проигрыш игрока)
    # чтобы понять,нужно просто подставить значения
    if not stats.game_active:
        play_button.draw_button()

    # обновление экрана
    pygame.display.flip()


def check_bullet_alien_collisions(ai_settings, display, stats, sb, ship, aliens, bullets):
    """Обработка коллизий (столкновений) пуль с пришельцами"""
    # проверка попадания в пришельцев
    # При обнаружении попадания удалить и пулю и пришельца
    # 2 аргумента True ,сообщают,нужно ли удалять оба объекта при коллизии (столкновении)
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # если случилось попадание,то :
    if collisions:
        # с каждой пулей связывается значение - список пришельцев,участвующих в коллизии
        # переберём словарь collisions и убедимся в том,
        # что очки начисляются за каждого подбитого пришельца
        for aliens in collisions.values():
            # повышаем число очков
            stats.score += ai_settings.alien_points * len(aliens)
        # создаёт новое изображение для обновления счёта
        sb.prep_score()
        check_high_score(stats, sb)

    # Если группа с пришельцами оказалась пустой,то мы очищаем группу bullets и создаём новый флот
    if len(aliens) == 0:
        # если флот уничтожен,то начинается следующий уровень

        # очищаем группу bullets
        bullets.empty()
        # увеличивает скорость пршельцев,пуль,корабля
        ai_settings.increase_speed()

        # увеличение уровня
        stats.level += 1
        sb.prep_level()

        # создаём новый флот
        create_fleet(ai_settings, display, aliens, ship)


def update_bullets(aliens, bullets, stats, sb, ai_settings, display, ship):
    """Обновляет позиции пуль и удаление старых пуль"""

    # обновление пули
    bullets.update()

    # удаление пули после того,как она вышла за границу экрана
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    # удаление пули и пришельца при столкновении + создание нового флота после уничтожения старого
    check_bullet_alien_collisions(ai_settings, display, stats, sb, ship, aliens, bullets)


def get_number_aliens_x(ai_settings, alien_width):
    """Вычисляем кол-во пришельцев в ряду"""

    # вымеряем свободное пространство с отступами.
    # Мы просто делаем 2 отступа равных ширине пришельца(уменьшаем ширину экрана на 2 отступа ширины пришельца)
    available_space_x = ai_settings.display_width - 2 * alien_width
    # Здесь мы резервируем интервалы между пришельцами (один интервал = одной ширине пришельца)
    # Пространство для вывода пришельца = 2 ширины пришельца(одно для отрисовки самого пришель + отступ(отступ равен ширине пришельца))
    # Тоесть,чтобы посчитать,сколько можно вывести пришельцев,
    # мы должны раделить кол-во доступного места(available_space_x) на пространство для вывода (2*alien_width)
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, display, aliens, alien_number, row_number):
    """Создаёт пришельца и рамещает его в ряду"""
    alien = Alien(ai_settings, display)
    alien_width = alien.rect.width
    # Создание пришельца в ряду
    # Эта формула нужна для того,чтобы правильно нарисовать пришельца в ряду (чтобы понять,нужно просто подставить значения)
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    # правильное создание пришельца в новом ряду(аналогично оперции с alien.x)
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def get_number_rows(ai_settings, ship_height, alien_height):
    """Определям кол-во рядов с пришельцами помещающихся на экране"""
    # Вычисляем доступное вертикальное пространство
    available_space_y = (ai_settings.display_height - (3 * alien_height) - ship_height)

    # Вычисляем,сколько поместится в свободное пространство рядов(с учетом самого пришельца и отступа(отступ=длина пришельца))
    # int используется для того,чтобы исключить создание неполного ряда пришельцев
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_fleet(ai_settings, display, aliens, ship):
    """Создаёт флот пришельце"""
    # Создание пришельца и вычисление количества пришельце в ряду
    # Интервал между соседними пришельцами равен одной ширине пришельца

    alien = Alien(ai_settings, display)
    # В этой переменной сохранилось допустимое количество пришельцев в ряду
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    # в этой переменной записано кол-во рядов с пришельцами
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        # Создание ряда пришельцев
        # Запускается цикл начиная с 0 и до допустимого количества пришельцев в ряду
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, display, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """Реагирует на достижение пришельцем края границы"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Опускает весь флот и меняет направление флота"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, stats, display, sb, ship, aliens, bullets):
    """
    Проверяет,достиг ли флот края экрана,
    после чего Обновляет позиции всех пришельцев на флоте
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # проверка коллизии корабль-пришельцы
    # метод spritecollideany() переберает группу и пытается найти любой элемент группы,
    # вступивший в коллизию с ship
    # если коллизия обнаружено,то print("корабль подбит!!!!!!")

    if pygame.sprite.spritecollideany(ship, aliens):
        print("fuck")
        ship_hit(ai_settings, stats, display, sb, ship, aliens, bullets)

    # проверяет,есть ли хотя бы 1 пришелец,который добрался до края экрана
    check_aliens_bottom(ai_settings, stats, display, sb, ship, aliens, bullets)


def ship_hit(ai_settings, stats, display, sb, ship, aliens, bullets):
    """Обрабатывет столкновение корабля с пришельцем"""
    if stats.ships_left > 0:
        stats.ships_left -= 1
        #обновление информации о кораблях
        sb.prep_ships()
        # оичщаются нарисованные группы пришельцев и пули
        aliens.empty()
        bullets.empty()
        # создаётся новый флот
        create_fleet(ai_settings, display, aliens, ship)
        # вызывается метод,который ставит корабль в центр экрана
        ship.center_ship()
        # пауза
        sleep(0.5)
    else:
        stats.game_active = False
        # делаем указатель видимым
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, display,sb ,ship, aliens, bullets):
    """Проверят,добрались ли пришельцы до нижнего края экрана"""
    display_rect = display.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= display_rect.bottom:
            # происходит то же,что и при столкновении с кораблём
            ship_hit(ai_settings, stats, display, sb, ship, aliens, bullets)
            break


def check_high_score(stats, sb):
    """Проверяет, не появился ли новый рекорд"""
    if stats.score >= stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
