from turtle import fd
import numpy as np
from libraries.constants_t2p1 import PI

class Shape:
    """
    Clase creada con el objetivo de tener fácil acceso al vertexData e indexData de las primitivas.
    """
    def __init__(self, vertexData, indexData):
        self.vertexData = vertexData
        self.indexData = indexData

def createTexturePiramide():
    """
    Función para crear una piramide de base cuadrada con texturas.
    """
    vertexData = [
        # Cara inferior cuadrada
        -0.5, -0.5, -0.5, 0, 1, 
         0.5, -0.5, -0.5, 1, 1, 
         0.5,  0.5, -0.5, 1, 0, 
        -0.5,  0.5, -0.5, 0, 0,
        # Cara triangular Y negativo
        -0.5, -0.5, -0.5,   0, 1,
         0.5, -0.5, -0.5,   1, 1,
         0.0,  0.0,  0.5, 0.5, 0,

        # Cara triangular Y positivo
        -0.5, 0.5, -0.5,   0, 1,
         0.5, 0.5, -0.5,   1, 1,
         0.0, 0.0,  0.5, 0.5, 0,

        # Cara triangular X positivo
        0.5, -0.5, -0.5,   0, 1,
        0.5,  0.5, -0.5,   1, 1,
        0.0,  0.0,  0.5, 0.5, 0,

        # Cara triangular X negativo
        -0.5, -0.5, -0.5,   0, 1,
        -0.5,  0.5, -0.5,   1, 1,
         0.0,  0.0,  0.5, 0.5, 0]

    indexData = [
        0,1,2,1,2,3, # Cara cuadrada
        4,5,6,
        7,8,9,
        10,11,12,
        13,14,15]
    return Shape(vertexData, indexData) 

def createTexturePrisma(R, n):
    """
    Función para crear un prisma de n lados con texturas.
    """
    delta_theta = 2*PI/n
    vertexData = [
        0, 0, -0.5, 1, 1,
        0, 0,  0.5, 0, 0]
    indexData = []
    for i in range(n):
        j = 4*i
        theta_0 = delta_theta*i
        theta_1 = theta_0 + delta_theta 
        x_0 = R*np.cos(theta_0)
        y_0 = R*np.sin(theta_0)
        x_1 = R*np.cos(theta_1)
        y_1 = R*np.sin(theta_1)
        
        vertexData += [
            x_0, y_0, -0.5, 0, 1,
            x_1, y_1, -0.5, 1, 1,
            x_0, y_0,  0.5, 0, 0,
            x_1, y_1,  0.5, 1, 0]

        indexData += [
              0, j+2, j+3,
            j+2, j+3, j+4,
            j+3, j+4, j+5,
            j+4, j+5,   1]


    return Shape(vertexData, indexData)

def createTextureHouseWalls():
    vertexData=[
        # Cara inferior
        -0.5, -1.5, -0.5, 1, 0, 
         0.5, -1.5, -0.5, 1, 1,
         0.5,  1.5, -0.5, 0, 1,
        -0.5,  1.5, -0.5, 0, 0, 

        # Cara Y-
        -0.5, -1.5, -0.5,   0,   1,
         0.5, -1.5, -0.5,   1,   1,
        -0.5, -1.5,  0.5,   0, 1/3,
         0.5, -1.5,  0.5,   1, 1/3,
           0, -1.5,    1, 1/2,   0,

        # Cara Y+
        -0.5,  1.5, -0.5,   1,   1,
         0.5,  1.5, -0.5,   0,   1,
        -0.5,  1.5,  0.5,   1, 1/3,
         0.5,  1.5,  0.5,   0, 1/3,
           0,  1.5,    1, 1/2,   0,

        # Cara X+ paralela
        0.5, -1.5, -0.5, 0, 1,
        0.5,  1.5, -0.5, 1, 1,
        0.5, -1.5,  0.5, 0, 0,
        0.5,  1.5,  0.5, 1, 0,
    
        # Cara X- paralela
        -0.5, -1.5, -0.5, 1, 1,
        -0.5,  1.5, -0.5, 0, 1,
        -0.5, -1.5,  0.5, 1, 0,
        -0.5,  1.5,  0.5, 0, 0,

        # Cara X+ oblicua
        0.5, -1.5, 0.5, 0, 1,
        0.5,  1.5, 0.5, 1, 1,
          0, -1.5,   1, 0, 0,
          0,  1.5,   1, 1, 0,
          
        # Cara X- oblicua
        -0.5, -1.5, 0.5, 1, 1,
        -0.5,  1.5, 0.5, 0, 1,
           0, -1.5,   1, 1, 0,
           0,  1.5,   1, 0, 0]

    indexData=[
         0,  1,  2,  2,  3,  0,
         4,  5,  7,  7,  4,  6,  6,  7,  8,
         9, 10, 12, 12,  9, 11, 11, 12, 13,
        14, 15, 16, 15, 16, 17,
        18, 19, 20, 19, 20, 21,
        22, 23, 24, 23, 24, 25,
        26, 27, 28, 27, 28, 29]

    return Shape(vertexData,indexData)

def createTextureCube(nx,ny):
    """
    Función para crear un cubo con texturas. 
    (Sacada del cubo rubik del auxiliar 6)
    """
    vertexData = [
        # Z positivo
        -0.5, -0.5,  0.5, 0, ny, 
         0.5, -0.5,  0.5,nx, ny, 
         0.5,  0.5,  0.5,nx,  0, 
        -0.5,  0.5,  0.5, 0,  0,  

        # Z negativo
        -0.5, -0.5, -0.5,  0, ny,
         0.5, -0.5, -0.5, nx, ny,
         0.5,  0.5, -0.5, nx,  0,
        -0.5,  0.5, -0.5,  0,  0, 

        # X positivo
        0.5, -0.5, -0.5, 0, ny, 
        0.5,  0.5, -0.5,nx, ny, 
        0.5,  0.5,  0.5,nx,  0, 
        0.5, -0.5,  0.5, 0,  0,  

        # X negativo
        -0.5, -0.5, -0.5,  0, ny,
        -0.5,  0.5, -0.5, nx, ny,
        -0.5,  0.5,  0.5, nx,  0,
        -0.5, -0.5,  0.5,  0,  0,

        # Y positivo
        -0.5,  0.5, -0.5,  0, ny,
         0.5,  0.5, -0.5, nx, ny,
         0.5,  0.5,  0.5, nx,  0,
        -0.5,  0.5,  0.5,  0,  0,

        # Y negativo
        -0.5, -0.5, -0.5, 0, ny,
         0.5, -0.5, -0.5,nx, ny,
         0.5, -0.5,  0.5, nx,  0,
        -0.5, -0.5,  0.5,  0,  0]

    indexData = [
        0, 1, 2, 2, 3, 0,  # Z+
        7, 6, 5, 5, 4, 7,  # Z-
        8, 9, 10, 10, 11, 8,  # X+
        15, 14, 13, 13, 12, 15,  # X-
        19, 18, 17, 17, 16, 19,  # Y+
        20, 21, 22, 22, 23, 20]  # Y-

    return Shape(vertexData, indexData)


def createTextureSphere(r,n):
    """
    Función que crea una primitiva de una aproximación de una esfera de radio R.
    A mayor n, mejor es la aproximación.
    """
    vertexData = []
    indexData = []
    delta_angulo = np.pi/n
    for i in range(n):
        for j in range(2*n):
            theta_0 = i * delta_angulo
            phi_0 = j * delta_angulo
            theta_1 = theta_0 + delta_angulo
            phi_1 = phi_0 + delta_angulo  
            k = 8*n*i + 4*j
            x_0 = r*np.sin(theta_0)*np.cos(phi_0)
            y_0 = r*np.sin(theta_0)*np.sin(phi_0)
            z_0 = r*np.cos(theta_0)
    
            x_1 = r*np.sin(theta_0)*np.cos(phi_1)
            y_1 = r*np.sin(theta_0)*np.sin(phi_1)
            z_1 = r*np.cos(theta_0)
    
            x_2 = r*np.sin(theta_1)*np.cos(phi_0)
            y_2 = r*np.sin(theta_1)*np.sin(phi_0)
            z_2 = r*np.cos(theta_1)
    
            x_3 = r*np.sin(theta_1)*np.cos(phi_1)
            y_3 = r*np.sin(theta_1)*np.sin(phi_1)
            z_3 = r*np.cos(theta_1)

            vertexData += [
                x_0, y_0, z_0,     j/(2*n),     i/n,
                x_1, y_1, z_1, (j+1)/(2*n),     i/n,
                x_2, y_2, z_2,     j/(2*n), (i+1)/n,
                x_3, y_3, z_3, (j+1)/(2*n), (i+1)/n]

            indexData += [
                  k, k+1, k+2,
                k+1, k+3, k+2]

    return Shape(vertexData, indexData)
