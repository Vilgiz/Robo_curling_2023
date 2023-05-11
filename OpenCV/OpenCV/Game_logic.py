import math
import matplotlib.pyplot as plt
import matplotlib.patches  as patches 
import numpy as np



def get_sector_number(data):
    # Define params of field
    center = (207, 1148)
    radius1 = 260
    radius2 = 370
    radius3 = 50
    radius4 = 150
    num_sectors = 22
    
    # Devide field into sectors
    sector_size = 360 / num_sectors
    
    # Calculate, in which field circle is the point
    for i in range(len(data)):
        distance = math.sqrt((data[i][1]-center[0])**2 + (data[i][2]-center[1])**2)
        if distance > radius1 and distance < radius2:
            sector_type = 1
        elif  distance > radius3 and distance < radius4:
             sector_type = 2
        else:
             sector_type = 0
    
    # Calculate  angle of the point based on the circle center
        angle = math.degrees(math.atan2(data[i][2]-center[1], data[i][1]-center[0]))
        if angle<0: angle = 360 + angle
    
    # Find point's sector
        sector_number = int(angle // sector_size)
        data[i].append(sector_type)
        data[i].append(sector_number)
    
    centers = []
    buf = []
    for k in range(2):
        if k == 1: r = radius3 + (radius4-radius3)/2
        else: r = radius1 + (radius2-radius1)/2
        for j in range(num_sectors):

            # Вычисляем центр сектора
            sector_center_x = int(center[0] + r * np.cos(math.radians(sector_size*j + sector_size/2)))
            sector_center_y = int(center[1] + r * np.sin(math.radians(sector_size*j + sector_size/2)))
            
            # Добавляем координаты центра в массив
            buf.append([sector_center_x,sector_center_y])
        centers.append(buf)
    return (data,centers)

def near_field_check(radius, point_idx, data):
    point = data[point_idx]
    count_red = 0
    count_blue = 0
    for i in range(len(data)):
        if (data[i][0] != 0) and (i != point_idx):
            distance = math.sqrt((data[i][1] - point[1])**2 + (data[i][2] - point[2])**2)
            if distance <= radius:
                if data[i][0] == 1:
                    count_blue += 1
                elif data[i][0] == 2:
                    count_red += 1
    return [count_red, count_blue]

def solution_searching (solution_matrix, normal_priority, fast_priority, data):
    #Вычисляем матрицу возможных конечных точек и приоритеты к ним
     free_sectors =    [[1,1,1,1,1,1,1,1,1,1,1,
                         1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,
                         1,1,1,1,1,1,1,1,1,1,1]]
     data, centers = get_sector_number(data)

     for i in range(len(data)):
        if (data[i][0] == 1) and (data[i][3] != 0):
            surround = near_field_check(150, i, data)
            if surround [1] > 1:
                coef = surround [0] - surround [1]
                solution_matrix.append([fast_priority[data[i][3]-1][data[i][4]] + coef,'destroy',[data[i][1], data[i][2]]])
            else:
                solution_matrix.append([fast_priority[data[i][3]-1][data[i][4]] ,'fast',[data[i][1], data[i][2]]])
        if (data[i][0] != 0) and (data[i][3] == 1):
             free_sectors [0][data[i][4]] = 0
        if (data[i][0] != 0) and (data[i][3] == 2):
            for j in range(5):
                k = data[i][4] + j
                l = data[i][4] - j
                if l < 0: l = 22+l
                if k > 21: k = k-22
                free_sectors [1][k] = 0
                free_sectors [1][l] = 0
     normal_priority = [[x*y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(normal_priority, free_sectors)]
     #print (normal_priority)
     for i in range(2):
        for j in range(len (normal_priority[0])):
            if (normal_priority[i][j] !=0 ):
                solution_matrix.append([normal_priority[i][j], 'normal', centers[i][j]])
     
     solution_matrix = sorted(solution_matrix, key=lambda x: x[0], reverse=True)
     print(solution_matrix)
     return solution_matrix

def path_searching(start_x, stop_x, step, start_y, distance, solution_matrix, data):
    for k in range(len(solution_matrix)):   
        x2, y2 = solution_matrix[k][2]
        for i in range (start_x, stop_x, step):
            x1, y1 = start_x + i, start_y
            a = y2 - y1
            b = x1 - x2
            c = x2 * y1 - x1 * y2
            count = 0
            # перебираем все точки из массива data
            for point in data:
                point_x = point[1]
                point_y = point[2]
                # вычисляем расстояние от точки до прямой
                if ((point_y < 100 + y2)and(solution_matrix[k][1] == 'normal')or(point_y < -55 + y2)and(solution_matrix[k][1] != 'normal')) and (point != solution_matrix[k][2]):
                    distance_to_line = abs(a * point_x + b * point_y + c) / math.sqrt(a ** 2 + b ** 2)
                    if distance_to_line < distance:
                        count +=1 
            if count == 0: 
                return [[x1, y1],[x2, y2]]
    return []

###################################################################################################################

def brain(data):
    normal_priority = [[2,2,2,2,4,1,4,2,2,2,2,
                        1,1,1,1,0,0,0,1,1,1,1],
                       [7,7,7,8,8,8,8,8,7,7,7,
                        6,6,6,7,7,9,7,7,6,6,6]]
    
    fast_priority = [[2,2,2,2,1,1,1,2,2,2,2,
                        2,2,2,3,4,8,4,3,2,2,2],
                       [10,10,10,10,10,10,10,10,10,10,10,
                        10,10,10,10,10,10,10,10,10,10,10]]
    solution_matrix = []
    solution_matrix = solution_searching(solution_matrix, normal_priority, fast_priority, data)
    #print (solution_matrix)
    path = path_searching(150, 650, 50, 10, 120, solution_matrix, data)
    return (path)
    

def draw_plt(data, path):
    # Data processing
    colors = ['none', 'blue', 'red']
    x = [point[1] for point in data]
    y = [point[2] for point in data]
    c = [colors[point[0]] for point in data]

    # Define params of field
    center = (207, 1148)
    radius = [370, 260, 150, 50]
    num_sectors = 22
    angles = np.linspace(0, 360, num_sectors+1)

    # Plot field, rocks, sectors and points
    fig, ax = plt.subplots(figsize=(8, 8))
    for i in range(4):
        circle = plt.Circle(center, radius[i], color='blue' if i < 2 else 'red', fill=False)
        ax.add_artist(circle)
    for j in range(num_sectors):
        sector = patches.Wedge(center, radius[0], angles[j], angles[j+1], fill=False, color='black', lw=0.5)
        ax.add_artist(sector)
    for k in range(len(x)):
        rock = plt.Circle((x[k],y[k]), 55, color=c[k], alpha=0.4)
        ax.add_artist(rock) 
    ax.scatter(x, y, c='black', s=20, alpha=1)

    plt.plot ([path[0][0],path[1][0]],[path[0][1],path[1][1]])
    plt.axis('scaled')
    plt.show()

