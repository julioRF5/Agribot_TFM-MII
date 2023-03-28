import matplotlib.pyplot as plt
import math
import numpy as np
import random

GENERATE_FILE = True

def y(x, m, b):
    return m*x + b

Row_Num = 3
hilera = 2 #Numero de plantas en paralelo por cada hilera
Max_BPR = 5 # maximum Big plants in each row
Max_SPR = 0 # maximum Small plant in each row
Row_lenght = 5 # in meters
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

x_offset = 0.0
y_offset = 0.0

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
   
# print(X_P)
plt.show()

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
