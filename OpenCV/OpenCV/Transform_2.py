from math import atan2, sin, cos, sqrt

def pos_transformation (x_table, y_table, c_point, p1, p2, ln, Red, Blue):
    # x_table, y_table - x � y ������ ���� � �� �����, � ��
    # c_point = (x,y) - ���������� ������ ���� � �� OpenCV, � ��� (�������)
    # p1 p2 - ����� ������ � ����� ������� || Ox �� �����. ���������� � �� OpenCV, ��� (�������)
    # ln = ����� ������� p1-p2 � ��
    x1 = p1[0]
    x2 = p2[0]
    y1 = p1[1]
    y2 = p2[1]
    angle = atan2(x2-x1,y2-y1)
    
    cf = ln / sqrt((x2-x1)**2 + (y2-y1)**2)
    
    x_cp = c_point[0]*cos(angle) - c_point[1]*sin(angle)
    y_cp = c_point[0]*sin(angle) + c_point[1]*cos(angle)
    
    x_cp *= cf
    y_cp *= cf
    
    x_shift = x_table - x_cp
    y_shift = y_table - y_cp
    

    rocks = [Blue, Red]
    data = []

    rocks = [Blue, Red]
    data = []
    

    for i in range (len(rocks)):
        for point in rocks[i]:
            x_p = point[0]
            y_p = point[1]
            x = x_shift + x_p*cos(angle) - y_p*sin(angle) 
            y = y_shift + x_p*sin(angle) + y_p*cos(angle)                                                        #�� ������ -> �� �����
            x *= cf
            y *= cf
            data.append([i+1, int(x),int(y)])
            
    return (data) 








    #for i in range(len(rocks)-1):
        #for point, point2 in rocks:
            #x_p = point
            #y_p = point2
            #x = x_shift + x_p*cos(angle) - y_p*sin(angle) 
            #y = y_shift + x_p*sin(angle) + y_p*cos(angle)                                                        #�� ������ -> �� �����
            #x *= cf
            #y *= cf
            #data.append([i+1, (int(x),int(y))])
        
    return (data)

#print(pos_transformation (300, 1500, [0,0],[40,20],[20, 20],red,blue))
