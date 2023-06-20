import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os
from random import randint


class Field():
    def __init__(self):
        if os.path.isfile('settings.py'):
            self.__load_settings()
        else:
            self.__load_defaults()

        self.__geometry_init()

    def __load_settings(self):
        import settings as config
        self.center = config.center
        self.radius = config.radius
        self.num_sectors = config.num_sectors

    def __load_defaults(self):
        import settings as config
        self.center = config.center
        self.radius = config.radius
        self.num_sectors = config.num_sectors

    def __geometry_init(self):
        self.sector_size = 360 / self.num_sectors
        self.centers = []
        for k in [0, 1]:
            if k == 1:
                r = self.radius[3] + (self.radius[2]-self.radius[3])/2
            if k == 0:
                r = self.radius[1] + (self.radius[0]-self.radius[1])/2
            buf = []
            for j in range(self.num_sectors):
                sector_center_x = int(
                    self.center[0] + r * np.cos(math.radians(self.sector_size*j + self.sector_size/2)))
                sector_center_y = int(
                    self.center[1] + r * np.sin(math.radians(self.sector_size*j + self.sector_size/2)))
                buf.append([sector_center_x, sector_center_y])
            self.centers.append(buf)


""" class Rock():
    def __init__():
        pass   """


class Brain():
    def __init__(self):
        self.Field = Field()
        if os.path.isfile('settings.py'):
            self.__load_settings()
        else:
            self.__load_defaults()

    def __load_settings(self):
        import settings as config
        self.embedded_sectors = config.embedded_sectors
        self.fast_priority = config.fast_priority
        self.normal_priority = config.normal_priority
        self.min_x = config.min_x
        self.max_x = config.max_x
        self.step = config.step
        self.start_y = config.start_y
        self.safe_distance = config.safe_distance
        self.variability = config.variability
        self.hard_mode = config.hard_mode
        self.easy_mode = config.easy_mode
        self.destroy_rad = config.destroy_rad
        self.start_safe_rad = config.start_safe_rad
        self.error_limit = config.error_limit

    def __load_defaults(self):
        import settings as config
        self.embedded_sectors = config.embedded_sectors
        self.fast_priority = config.fast_priority
        self.normal_priority = config.normal_priority
        self.min_x = config.min_x
        self.max_x = config.max_x
        self.step = config.step
        self.start_y = config.start_y
        self.safe_distance = config.safe_distance
        self.variability = config.variability
        self.hard_mode = config.hard_mode
        self.easy_mode = config.easy_mode
        self.destroy_rad = config.destroy_rad
        self.start_safe_rad = config.start_safe_rad
        self.error_limit = config.error_limit

    def __field_scanning(self, data):
        for i in range(len(data)):
            distance = math.sqrt(
                (data[i][1]-self.Field.center[0])**2 + (data[i][2]-self.Field.center[1])**2)
            angle = math.degrees(math.atan2(
                data[i][2]-self.Field.center[1], data[i][1]-self.Field.center[0]))
            if angle < 0:
                angle = 360 + angle
            if distance > self.Field.radius[1] and distance < self.Field.radius[0]:
                sector_type = 1
            elif distance > self.Field.radius[3] and distance < self.Field.radius[2]+30:
                sector_type = 2
            elif distance < self.Field.radius[3]:
                sector_type = 3
            else:
                sector_type = 0
            #Камни в мешающей зоне
            # if (670> data[i][1] >270) and (850> data[i][2] >550):
            #     sector_type = 10

            sector_number = int(angle // self.Field.sector_size)
            data[i].append(sector_type)
            data[i].append(sector_number)

        return (data)

    def __near_field_check(self, radius, point_idx):
        point = self.data[point_idx]
        count_robot = 0
        count_human = 0
        for i in range(len(self.data)):
            if (self.data[i][0] != 0) and (i != point_idx):
                distance = math.sqrt(
                    (self.data[i][1] - point[1])**2 + (self.data[i][2] - point[2])**2)
                if distance <= radius:
                    if self.data[i][0] == 1:
                        count_human += 1
                    elif self.data[i][0] == 2:
                        count_robot += 1

        return [count_human, count_robot]

    def __variants_searching(self):
        free_sectors = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]#self.embedded_sectors
        data = self.__field_scanning(self.data)
        solution_matrix = []
        for i in range(len(data)):
            if (data[i][0] == 1) and (data[i][3] == 3):
                surround = self.__near_field_check(self.destroy_rad, i)
                coef = surround[0] - surround[1]
                solution_matrix.append(
                    [10 + coef, 2, [data[i][1], data[i][2]]])
            elif (data[i][0] == 1) and (data[i][3] != 0):
                # print(self.embedded_sectors)
                if self.embedded_sectors[data[i][3]-1][data[i][4]] == 1:
                    surround = self.__near_field_check(self.destroy_rad, i)
                    if surround[0] > 0:
                        coef = surround[0] - surround[1]
                        solution_matrix.append(
                            [self.fast_priority[data[i][3]-1][data[i][4]] + coef, 2, [data[i][1], data[i][2]]])
                    else:
                        k = randint(1,4)
                        if k == 3: result = 2
                        else: result = 1
                        solution_matrix.append(
                            [self.fast_priority[data[i][3]-1][data[i][4]], result, [data[i][1], data[i][2]]])
            if (data[i][0] != 0) and (data[i][3] == 1):
                free_sectors[0][data[i][4]] = 0
            elif (data[i][0] != 0) and (data[i][3] == 2):
                for j in range(3):
                    k = data[i][4] + j
                    l = data[i][4] - j
                    if l < 0:
                        l = 22+l
                    if k > 21:
                        k = k-22
                    free_sectors[1][k] = 0
                    free_sectors[1][l] = 0
        normal_priority = [[x*y for x, y in zip(row_a, row_b)]
                           for row_a, row_b in zip(self.normal_priority, free_sectors)]
        for i in range(2):
            for j in range(len(normal_priority[0])):
                if (normal_priority[i][j] != 0):
                    solution_matrix.append(
                        [normal_priority[i][j], 0, self.Field.centers[i][j]])
        solution_matrix = sorted(
            solution_matrix, key=lambda x: x[0], reverse=True)

        return (solution_matrix)

    def __path_searching(self):
        solution_matrix = self.__variants_searching()
        #print(solution_matrix)
        path = []
        for variant in solution_matrix:
            x2, y2 = variant[2]
            buf = []
            for i in range(self.min_x, self.max_x, self.step):
                x1, y1 = i, self.start_y
                a = y2 - y1
                b = x1 - x2
                c = x2 * y1 - x1 * y2
                collision = 0
                for point in self.data:
                    point_x = point[1]
                    point_y = point[2]
                    if ((point_y < 80 + y2) and (variant[1] == 0) or
                            (point_y < -55 + y2) and (variant[1] != 0)) and ([point_x, point_y] != variant[2]):
                        distance_to_line = abs(
                            a * point_x + b * point_y + c) / math.sqrt(a ** 2 + b ** 2)

                        if distance_to_line < self.safe_distance:
                            collision += 1
                if not collision:
                    buf.append([[x1, y1], [x2, y2], [variant[1]]])
            buf = sorted(buf, key=lambda x: abs(x[0][0]-x[1][0]))
            if buf:
                path.append(buf)
        # result = path[:min(len(path), self.variability)]

        return (path)

    def __safety_check(self, result):
        if (0 < result[0][0] < 800) and (0 < result[1][0] < 800) and (10 < result[0][1]):
            for point in self.data:
                if ((result[0][0]-self.start_safe_rad < point[1] < result[0][0]+self.start_safe_rad) and
                        (self.start_y - self.start_safe_rad < point[2] < self.start_y + self.start_safe_rad)):
                    return False
            return (True)
        else:
            return (False)

    def draw_plt(self):

        service_p = [[0, self.max_x+100], [0, self.Field.center[1]*2]]
        colors = ['white', 'blue', 'red']
        x = [point[1] for point in self.data]
        y = [point[2] for point in self.data]
        c = [colors[point[0]] for point in self.data]
        angles = np.linspace(0, 360, self.Field.num_sectors+1)

        fig, ax = plt.subplots(figsize=(8, 8))
        for i in range(4):
            circle = plt.Circle(
                self.Field.center, self.Field.radius[i], color='blue' if i < 2 else 'red', fill=False)
            ax.add_artist(circle)
        for j in range(self.Field.num_sectors):
            sector = patches.Wedge(
                self.Field.center, self.Field.radius[0], angles[j], angles[j+1], fill=False, color='black', lw=0.5)
            ax.add_artist(sector)
        for k in range(len(x)):
            rock = plt.Circle((x[k], y[k]), 55, color=c[k], alpha=0.4)
            ax.add_artist(rock)
        ax.scatter(x, y, c='black', s=20, alpha=1)
        ax.scatter(service_p[0], service_p[1], c='none', s=20, alpha=1)

        if self.result[2] == [2]:
            color = 'red'
        elif self.result[2] == [1]:
            color = 'yellow'
        else:
            color = 'green'
        plt.plot([self.result[0][0], self.result[1][0]], [
                 self.result[0][1], self.result[1][1]], color=color)
        plt.axis('scaled')
        plt.show()

    def solve(self):
        count = 0
        while True:
            count += 1
            variants = self.__path_searching()
            # print(variants)
            if len(variants) == 0:
                print('[ERROR]: no one variant is safety 1')
                return None
            else:
                if self.hard_mode:
                    result = variants[0][0]
                elif self.easy_mode:
                    i = randint(0, len(variants)-1)
                    result = variants[i][randint(0, len(variants[i])-1)]
                else:
                    i = randint(0, min(len(variants)-1, self.variability))
                    result = variants[i][randint(0, len(variants[i])-1)]

                if self.__safety_check(result):
                    self.result = result
                    return (result)
                    break
                if count > self.error_limit:
                    print('[ERROR]: no one variant is safety 2')
                    return None
                    # следующая итерация - придумать, что делать в таких случаях

    def take_data(self, Robot, Human):
        # тут для формата данных [[x,y],[x,y]...]
        self.data = [[2] + buf for buf in Robot] + [[1] + buf for buf in Human]

    def update_settings(self):
        self.__init__()


if __name__ == '__main__':
    brain = Brain()
    data1 = [[200, 800], [400, 550], [400, 1100], [400, 11], [620, -10]]
    data2 = [[150, 980], [400, 1400]]

    brain.take_data(Robot=data2, Human=data1)
    res = brain.solve()
    #print(res)
    brain.draw_plt()
