from Balli import Balli

massiv_red = [[400, 1100], [300, 1100], [200, 1000], [100, 900]]
massiv_blue = [[3300, 1100], [2300, 1100], [1300, 1000], [3300, 400]]
center = (400, 1100)

radius_white_Circle = 50
radius_green_Circle = 150
radius_blue_Ring = 260
radius_white_Ring = 370

Red_scope = Balli(center, radius_white_Circle, radius_green_Circle, radius_blue_Ring, radius_white_Ring)
Blue_scope = Balli(center, radius_white_Circle, radius_green_Circle, radius_blue_Ring, radius_white_Ring)


for quantity in range (len(massiv_red)):                                           # ВНИМАНИЕ!!!!!! КОСТЫЛЬ РАЗМЕРОМ С МЛЕЧНЫЙ ПУТЬ!!!!!!! 
    Red_scope.Which_field(Blue_scope.iteration_of_piptics(massiv_red, quantity))
print(Red_scope.point)

for quantity in range (len(massiv_blue)):                                           # ВНИМАНИЕ!!!!!! КОСТЫЛЬ РАЗМЕРОМ С МЛЕЧНЫЙ ПУТЬ!!!!!!! 
    Blue_scope.Which_field(Blue_scope.iteration_of_piptics(massiv_blue, quantity))
print(Blue_scope.point)