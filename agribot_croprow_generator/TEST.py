# -*- coding: utf-8 -*-
import math

punto_inicio = (15, -5)
punto_fin = (15, -3.3)
# Calcular la distancia entre los dos puntos
distancia = math.sqrt((punto_fin[0] - punto_inicio[0]) ** 2 + (punto_fin[1] - punto_inicio[1]) ** 2)
semi = 1  #(derecho)
# Calcular el radio de la semicircunferencia
radio = distancia / 2

# Calcular el centro de la semicircunferencia
centro_x = (punto_inicio[0] + punto_fin[0]) / 2
centro_y = (punto_inicio[1] + punto_fin[1]) / 2

# Verificar si los puntos están en línea recta vertical u horizontal
if punto_inicio[0] == punto_fin[0]:  # Línea vertical
    # Calcular el ángulo de inicio y fin de la semicircunferencia
    if semi == 1:
        angulo_inicio = -math.pi / 2
        angulo_fin = math.pi / 2
    else:
        print("aqui")
        angulo_inicio = math.pi / 2
        angulo_fin = -math.pi / 2
elif punto_inicio[1] == punto_fin[1]:  # Línea horizontal
    # Calcular el ángulo de inicio y fin de la semicircunferencia
    if semi == 1:    
        angulo_inicio = math.pi
        angulo_fin = 0
    else:
        print("otra vez aqui")
        angulo_inicio = 0
        angulo_fin = math.pi
else:
    raise ValueError("Los puntos no están en línea recta horizontal o vertical.")

# Calcular la cantidad de waypoints necesarios
cantidad_waypoints = 10 #int(abs(angulo_fin - angulo_inicio) * radio) + 1
print("cantidad waypoints",cantidad_waypoints)
# Calcular los waypoints en la semicircunferencia
waypoints = []
angulo_actual = angulo_inicio
for _ in range(cantidad_waypoints):
    x = centro_x + radio * math.cos(angulo_actual)
    y = centro_y + radio * math.sin(angulo_actual)
    waypoints.append((x, y))
    angulo_actual += (angulo_fin - angulo_inicio) / (cantidad_waypoints - 1)

for waypoint in waypoints:
    print(waypoint)


lista = [1, 2, 3]  # Crear una lista

# Usar la lista
for elemento in lista:
    print(elemento)
print( "nueva lista")
lista.clear()
lista = [5, 6, 7]
# Borrar la lista
for elemento in lista:
    print(elemento)