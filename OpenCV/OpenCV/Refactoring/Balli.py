import math

class Balli:
    def __init__(self, center, radius_white_Circle, radius_green_Circle, 
                radius_blue_Ring, radius_white_Ring):
        self.cx = center[0]
        self.cy = center[1]
        self.point = 0
        
        self.radius_white_Circle = radius_white_Circle
        self.radius_green_Circle = radius_green_Circle
        self.radius_blue_Ring = radius_blue_Ring
        self.radius_white_Ring = radius_white_Ring

    def Which_field(self, coord_pipt):

        distance_from_center = math.sqrt((coord_pipt[0] - self.cx)**2 + (coord_pipt[1] - self.cy)**2)

        if distance_from_center < self.radius_white_Circle:
            #print ("White-green Circle")
            self.point += 80
            return self.point
        elif distance_from_center > self.radius_white_Circle and distance_from_center < self.radius_green_Circle:
            #print ("Green Circle")
            self.point += 80
            return self.point
        elif distance_from_center > self.radius_green_Circle and distance_from_center < self.radius_white_Ring:
            #print ("White Ring")
            return self.point
        elif distance_from_center > self.radius_white_Ring and distance_from_center < self.radius_blue_Ring:
            self.point += 50
            #print ("Blue Ring")
            return self.point 
        else:
            #print("Out of range")
            return self.point

    def iteration_of_piptics(self, massiv, quantity):
        current_piptic = []
        while (len(massiv))-1 >= quantity:                     # ВНИМАНИЕ!!!!!! КОСТЫЛЬ РАЗМЕРОМ С МЛЕЧНЫЙ ПУТЬ!!!!!!!
            current_piptic = []                         
            for pip in massiv[quantity]:
                current_piptic.append(pip)
            return current_piptic
