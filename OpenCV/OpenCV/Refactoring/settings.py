﻿# Параметры стола
center = (470, 1260)
radius = [390, 260, 150, 50]
num_sectors = 22
millimetrs = 300

# Настройки приоритетов закатывания
normal_priority = [[2, 2, 2, 2, 4, 5, 4, 2, 2, 2, 2,
                    1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
                   [7, 6, 6, 6, 6, 7, 6, 6, 6, 6, 7,
                    6, 6, 6, 6, 6, 7, 6, 6, 6, 6, 6]]

# normal_priority = [[2, 2, 2, 2, 4, 5, 4, 2, 2, 2, 2,
#                     1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
#                    [7, 7, 7, 8, 8, 10, 8, 8, 7, 7, 7,
#                     6, 6, 6, 7, 7, 9, 7, 7, 6, 6, 6]]

# Настройки приоритетов выбивания fast и destroy
fast_priority = [[6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
                  7, 7, 7, 8, 8, 8, 8, 8, 7, 7, 7],
                 [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
                 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]]

# fast_priority = [[2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2,
#                  2, 2, 2, 3, 4, 8, 4, 3, 2, 2, 2],
#                 [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
#                 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]]

variability = 2
hard_mode = True
easy_mode = False
destroy_rad = 150

# Возможность выключить некотоыре секторы из расчета (1-on, 0-off)
embedded_sectors = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

# Настройки ограничений бросков
min_x = 251
max_x = 749
step = 25
start_y = 100
safe_distance = 120
start_safe_rad = 85
error_limit = 15


# Параметры камней
# Задаем диапазоны цветов для красного и синего цветов
red_lower = [0, 80, 80]
red_upper = [15, 255, 255]
blue_lower = (20, 70, 200)  # (90, 70, 20)
blue_upper = (25, 180, 255)  # (120, 220, 100)
yell_lower = [15, 60, 100]  # (90, 70, 20)
yell_upper = [185, 255, 255]  # (120, 220, 100)

red_lower_RGB = [70, 0, 0]
red_upper_RGB = [255, 100, 100]  
yell_lower_RGB = [140, 100, 0]  
yell_upper_RGB = [255, 255, 160]  

# lower_green = (140, 100, 0)
# upper_green = (255, 255, 160)
# Задаем минимальный и максимальный радиусы
min_radius = 30
max_radius = 50

# Коэффициенты для преобразования Хаффа, поиск окружностей
min_dist = 100  # ! ПОМЕНЯТЬ СУКА, НЕ ОТЛАЖЕНО !
accuracy = 50  # ! ПОМЕНЯТЬ СУКА, НЕ ОТЛАЖЕНО !
sensitivity = 30  # ! ПОМЕНЯТЬ СУКА, НЕ ОТЛАЖЕНО !


test_lower = (0, 160, 160)
test_upper = (20, 255, 255)