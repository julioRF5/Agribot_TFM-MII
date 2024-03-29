# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import math
import numpy as np
import random

GENERATE_FILE = False
RECORD_WAYPOINTS = True

waypoints_path = "/home/juliorf/catkin_ws/src/julio_tfm/agribot-master/ROS_Waypoints_Processor/waypoints_files/waypoints.txt"

def y(x, m, b):
    return m*x + b

def record_waypoints(file_path, pos_list):
    file = open(file_path, "a+")
    file.write("{},{},{},{},{},{},{}\n".format(pos_list[0], pos_list[1], pos_list[2], pos_list[3], pos_list[4], pos_list[5], pos_list[6])) # x, y, z, Ox, Oy, Oz, Ow
    file.close()

def waypoints2semicircle(punto_inicio, punto_fin, semi_circ):    # semi_circ = 1 obtengo la derecha, sino la izqioerda
    # Calcular la distancia entre los dos puntos
    distancia = math.sqrt((punto_fin[0] - punto_inicio[0]) ** 2 + (punto_fin[1] - punto_inicio[1]) ** 2)

    # Calcular el radio de la semicircunferencia
    radio = distancia / 2

    # Calcular el centro de la semicircunferencia
    centro_x = (punto_inicio[0] + punto_fin[0]) / 2
    centro_y = (punto_inicio[1] + punto_fin[1]) / 2

    # Verificar si los puntos están en línea recta vertical u horizontal
    if punto_inicio[0] == punto_fin[0]:  # Línea vertical
        # Calcular el ángulo de inicio y fin de la semicircunferencia
        angulo_inicio = -math.pi / 2
        angulo_fin = math.pi / 2
    elif punto_inicio[1] == punto_fin[1]:  # Línea horizontal
        # Calcular el ángulo de inicio y fin de la semicircunferencia
        angulo_inicio = math.pi
        angulo_fin = 0
    else:
        raise ValueError("Los puntos no están en línea recta horizontal o vertical.")

    # Calcular la cantidad de waypoints necesarios
    cantidad_waypoints = 10 #int(abs(angulo_fin - angulo_inicio) * radio) + 1

    # Calcular los waypoints en la semicircunferencia
    waypoints = []
    angulo_actual = angulo_inicio
    for _ in range(cantidad_waypoints):
        x = centro_x + radio * math.cos(angulo_actual)
        y = centro_y + radio * math.sin(angulo_actual)
        waypoints.append((x, y, 0, 0, 0, 0, 1))     # x, y, z, Ox, Oy, Oz, Ow
        if semi_circ == 1:
            angulo_actual -= ( angulo_inicio - angulo_fin) / (cantidad_waypoints - 1)
        else:
            angulo_actual -= ( angulo_fin - angulo_inicio) / (cantidad_waypoints - 1)

    return waypoints


Row_Num = 6             # Numero de hileras                                                                 
hilera = 2              # Numero de plantas en paralelo por cada hilera
Max_BPR = 20            # Numero máximo de plantas grandes en cada hilera                        10
Row_lenght = 10         # Longitud de las hileras en metros                                                 5

Max_SPR = 0         # maximum Small plant in each row
Random_noise_magnitude = 1 # maximum random noise magitude in meters


SP_H = 0.110674
BP_H = 0.103018

Pose_X = 0.0
Pose_Y = 0.0
Pose_H = 0.0

Min_dis_plants = 0.1 # minimum distace between two plants in a row in m 
Max_dis_plants = 0.1 # maximum distace between two plants in a row in m

Sigma_Plant_dis = 0.02
Sigma_Weed_dis = 0.005

CropRow_Slope = 0  #pendiente de las hileras
CropRow_Offset = 0.1  # Separacion entre fila de una misma hilera

x_offset = -10.0
y_offset = -5.0

X_P  = np.zeros((2*Row_Num, Max_BPR))
X_W  = np.zeros((Row_Num, Max_SPR))
Y_P  = np.zeros((2*Row_Num, Max_BPR))
Y_W  = np.zeros((Row_Num, Max_SPR))

ii= 0

for j in range(Row_Num):

    for i in range(hilera):
        random.seed(2)
        X_P[i+ii] = np.linspace(x_offset, x_offset + Row_lenght, Max_BPR)
        X_W[i] = np.linspace(x_offset, x_offset + Row_lenght, Max_SPR)
        Y_P[i+ii] = [y(x, CropRow_Slope, i * CropRow_Offset + y_offset)  for x in X_P[i]] #JRF #+ abs(random.gauss(Pose_Y,Sigma_Plant_dis))
        Y_W[i] = [y(x, CropRow_Slope, i * CropRow_Offset + y_offset) + abs(random.gauss(Pose_Y,Sigma_Weed_dis)) for x in X_W[i]]
        plt.scatter(X_P[i+ii], Y_P[i+ii], c='g')
        # plt.scatter(X_W[i], Y_W[i], c='r')
        y_offset = i * CropRow_Offset + y_offset       #JRF   Guardo la posicion Y de la ultima fila de plantas puesta, para poder poner la soguiente fila justo a 1.5 metros

    ii = ii + 2
    y_offset = y_offset + 1.5       #JRF

plt.show()

reverse = False #recorrer hilera del reves (X negativo)

if RECORD_WAYPOINTS:
    with open(waypoints_path, "w") as archivo:
        archivo.write("")  #Escribe cadena vacia para borrar el contenido del fichero de texto.
        pos_inicial = [X_P[0][0]-5, Y_P[0][0], 0,0,0,0,1]
        record_waypoints(waypoints_path, pos_inicial) #Primera posicion de aproximación
        
    for i in range(2*Row_Num):
        for y in range(Max_BPR):
            if i%2 == 0:  #En cada hilera hay a su vez dos hileras más. Solo guardamos la posicion de todos los borocolis de una de las hileras (las pares)
                if reverse == False:
                    
                    pos_stright = [X_P[i][y], Y_P[i][y], 0,0,0,0,1]
                    record_waypoints(waypoints_path, pos_stright)
                    
                else:
                    pos_reverse = [X_P[i][(Max_BPR-1)-y], Y_P[i][y], 0,0,0,0,1]
                    print("voy a recorrer la hilera del reves, esta es mi posicion", pos_reverse)
                
                    record_waypoints(waypoints_path, pos_reverse)
                    
        if i%2 == 0:  #Guardamos posiciones de seguridad y posiciones para realizar la semicircunferencia
            if reverse:
                print("recorro hilera reverse")
                safe_pos_list_rev = [X_P[i][(Max_BPR-1)-y]-5, Y_P[i][y], 0,0,0,0,1]  #safe_pos_list_rev = [X_P[i][(Max_BPR-1)-y]-5, Y_P[i][y], 0,0,+1.57,0,1] (creo que esta mal en cualquier caso seria el 1.57 en la componente Z del quaternio)  # primera posicion de seguridad, se fija tb la orientacion para encarar la curva
                record_waypoints(waypoints_path, safe_pos_list_rev)
                   
                #position_list = [X_P[i][Max_BPR-1]-5, Y_P[i][x]+1.5, 0,0,0,0,0]
                #record_waypoints(waypoints_path, position_list)
                pto_inicio_rev = (X_P[i][(Max_BPR-1)-y]-5, Y_P[i][y])       # punto de inicio para calcular la semicircuferencia (es el ultimo brocoli de la hilera actual)
                pto_fin_rev = (X_P[i][(Max_BPR-1)-y]-5, Y_P[i][y] + 1.6)    # punto de fin para calcular la semicircuferencia (es el primer brocoli de la hilera siguiente)
                                                                    # Entre dos subhileras PARES hay 1.6 metros, el 1.5 que puse yo era entre la subhilera impar y la siguiente par
                wp_rev = waypoints2semicircle(pto_fin_rev, pto_inicio_rev, semi_circ= -1)

                for waypoint in wp_rev:
                    record_waypoints(waypoints_path, waypoint)
                    print(waypoint)
                    print("next wp")

            
                reverse = False
            else:
                print("recorro hilera stright")
                safe_pos_list_strht = [X_P[i][Max_BPR-1]+5, Y_P[i][y], 0,0,0,-0.7071068,0.7071068] #safe_pos_list_strht = [X_P[i][Max_BPR-1]+5, Y_P[i][y], 0,0,-1.57,0,1]
                record_waypoints(waypoints_path, safe_pos_list_strht)
                pto_ini_strht = [X_P[i][Max_BPR-1]+5, Y_P[i][y]]
                pto_fin_strht = [X_P[i][Max_BPR-1]+5, Y_P[i][y]+1.6]
                wp_strht = waypoints2semicircle(pto_ini_strht, pto_fin_strht, semi_circ= 1)
                
                for waypoint in wp_strht:
                    record_waypoints(waypoints_path, waypoint)
                    print(waypoint)
                    print("next wp stright")

                reverse = True
            
    if i == (2*Row_Num)-1:   #Es la ultima hilera. Llevo el robot a la posicion de partida
                    print("he llegado al final")
                    pos_partida = [-14.0, 0, 1.13,0,0,0.7071068,0.7071068]  # pos_partida = [-14.0, 0, 1.13,0,+1.57,0,1]
                    record_waypoints(waypoints_path, pos_partida)


if GENERATE_FILE:
    # Output files
    Headers_path = "CropRow_Headers.xml"
    Models_path = "CropRow_Models.xml"
    new_Headers = open(Headers_path,'w')
    new_Models = open(Models_path,'w')

    # Inputs files
    BP_HEADER_path = "BP_header.xml"
    BP_MODEL_path = 'BP_model.xml'
    SP_HEADER_path = "SP_header.xml"
    SP_MODEL_path = "SP_model.xml"

    BP_HEADER = open(BP_HEADER_path,'r')
    BP_MODEL = open(BP_MODEL_path,'r')
    SP_HEADER = open(SP_HEADER_path,'r')
    SP_MODEL = open(SP_MODEL_path,'r')

    BP_HEADER_content = BP_HEADER.read()
    BP_MODEL_content = BP_MODEL.read()
    SP_HEADER_content = SP_HEADER.read()
    SP_MODEL_content = SP_MODEL.read()

    # Pose = "\t\t\t\t<pose frame=''>" + str(Pose_X) + " " + str(Pose_Y) + " " + str(Pose_H) + " 0 -0 0</pose>\n"
    model_def = "\n\t\t</model>\n"
    scale = "\t\t\t\t<scale>1 1 1</scale>\n"
    BP_link_name = "\t\t\t\t<link name='link_0'>\n"
    SP_link_name = "\t\t\t<link name='link_0'>\n"


    # Big plants
    for i in range(2*Row_Num):
        for x in range(Max_BPR):
            BP_name = "\n\n\t\t\t<model name='big_plant_" + str(x+ i*Max_BPR) + "'>\n"
            new_Headers.write(BP_name)
            Pose = "\t\t\t\t<pose frame=''>" + str(X_P[i][x]) + " " + str(Y_P[i][x]) + " " + str(0) + " 0 -0 0</pose>\n"
            new_Headers.write(Pose)
            new_Headers.write(scale)
            new_Headers.write(BP_link_name)
            Pose = "\t\t\t\t\t<pose frame=''>" + str(X_P[i][x]) + " " + str(Y_P[i][x]) + " " + str(BP_H) + " 0 -0 0</pose>\n"
            new_Headers.write(Pose)
            new_Headers.write(BP_HEADER_content)

            new_Models.write(BP_name)
            new_Models.write(BP_MODEL_content)
            Pose = "\n\t\t\t<pose frame=''>" + str(X_P[i][x]) + " " + str(Y_P[i][x]) + " " + str(0) + " 0 -0 0</pose>\n"
            new_Models.write(Pose)
            new_Models.write(model_def)

      
        #  Small plants
        for x in range(Max_SPR):
            SP_name = "\n<model name='small_plant_" + str(x+i*Max_SPR) + "'>\n"
            new_Headers.write(SP_name)
            Pose = "<pose frame=''>" + str(X_W[i][x]) + " " + str(Y_W[i][x]) + " " + str(0) + " 0 -0 0</pose>\n"
            new_Headers.write(Pose)
            new_Headers.write(scale)
            new_Headers.write(SP_link_name)
            Pose = "<pose frame=''>" + str(X_W[i][x]) + " " + str(Y_W[i][x]) + " " + str(SP_H) + " 0 -0 0</pose>\n"
            new_Headers.write(Pose)
            new_Headers.write(SP_HEADER_content)

            new_Models.write(SP_name)
            new_Models.write(SP_MODEL_content)
            Pose = "\n<pose frame=''>" + str(X_W[i][x]) + " " + str(Y_W[i][x]) + " " + str(0) + " 0 -0 0</pose>\n"
            new_Models.write(Pose)
            new_Models.write(model_def)
    
    BP_HEADER.close()
    BP_MODEL.close()
    SP_HEADER.close()
    SP_MODEL .close()
    new_Headers.close()
    new_Models.close()

    # Output files
    P0_path = "farm_P0.xml"
    P1_path = "farm_P1.xml"
    P2_path = "farm_P2.xml"
    P3_path = "farm_P3.xml"
    farm_P0 = open(P0_path,'r')
    farm_P1 = open(P1_path,'r')
    farm_P2 = open(P2_path,'r')
    farm_P3 = open(P3_path,'r')
    farm_P0_content = farm_P0.read()
    farm_P1_content = farm_P1.read()
    farm_P2_content = farm_P2.read()
    farm_P3_content = farm_P3.read()

    Headers_path = 'CropRow_Headers.xml'
    Models_path = 'CropRow_Models.xml'
    new_Headers = open(Headers_path,'r')
    new_Models = open(Models_path,'r')
    new_Headers_read = new_Headers.read()
    new_Models_read = new_Models.read()
    
    Final_path = 'FarmWithCropRow.world'
    Final_World = open(Final_path,'w')

    Final_World.write(farm_P0_content)
    Final_World.write(farm_P1_content)
    Final_World.write(new_Headers_read)
    Final_World.write(farm_P2_content)
    Final_World.write(new_Models_read)
    Final_World.write(farm_P3_content)
    
    

    farm_P1.close()
    farm_P2.close()
    farm_P3.close()
    Final_World.close()
