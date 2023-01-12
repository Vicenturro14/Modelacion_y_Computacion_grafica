import numpy as np
import libraries.transformations_t2p1 as tr
from libraries.constants_t2p1 import PI

class Trees:
    """
    Clase para controlar las hojas de los árboles.
    """
    def __init__(self):
        # 1:Verano
        # 2:Otoño 
        # 3:Invierno
        # 4:Primavera 
        self.season = 1
        

class Camera:
    """
    Clase para controlar la cámara y tener fácil acceso a su información.
    """
    def __init__(self):
        self.theta = PI
        self.radio = 3
        self.pos = np.array([ 2, 0.0, 0.25 ])
        self.up = np.array([0.0, 0.0, 1.0])
        self.upperEye = False

    def getView(self):
        return tr.lookAt(self.pos, np.array([
            self.pos[0] + self.radio * np.cos(self.theta),
            self.pos[1] +self.radio * np.sin(self.theta),
            self.pos[2]]), self.up)

    def getOrtoView(self):
        return tr.lookAt(np.array([0,0,7]), np.array([0,0,0]),np.array([-1,0,0]))
    def changeView(self):
        self.upperEye = not self.upperEye
    
    def limits(self):
        if self.pos[0]>2.5:
            self.pos[0] = 2.5
        elif self.pos[0]<-2.5:
            self.pos[0] = -2.5
        elif self.pos[1]<-5:
            self.pos[1] = -5
        elif self.pos[1]>5:
            self.pos[1] =5
        
        
