import numpy as np

def identity():
    """
    Retorna la matriz identidad de dimensión 4.
    """
    return np.identity(4, dtype=np.float32)

def translate(tx, ty, tz):
    """
    Retorna la matriz que traslada tx, ty y tz unidades las coordenadas X, Y y Z, respectivamente.
    """
    return np.array([
        [ 1, 0, 0, tx],
        [ 0, 1, 0, ty],
        [ 0, 0, 1, tz],
        [ 0, 0, 0,  1]], dtype = np.float32)

def uniscale(s):
    """
    Retorna la matriz que escala los valores de las coordenadas X, Y y Z por el factor s.
    """
    return np.array([
        [ s, 0, 0, 0],
        [ 0, s, 0, 0],
        [ 0, 0, s, 0],
        [ 0, 0, 0, 1]], dtype = np.float32)
 

def scale(sx, sy, sz):
    """
    Retorna la matriz que escala los valores de las coordenadas X, Y y Z por los factores sx, sy y sz, respectivamente.
    """
    return np.array([
        [ sx,  0,  0, 0],
        [  0, sy,  0, 0],
        [  0,  0, sz, 0],
        [  0,  0,  0, 1]], dtype = np.float32)


def rotationX(theta):
    """
    Retorna la matriz que rota theta radianes las coordenadas X,Y y Z respecto al eje X.
    """
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)

    return np.array([
        [ 1,         0,          0, 0],
        [ 0, cos_theta, -sin_theta, 0],
        [ 0, sin_theta,  cos_theta, 0],
        [ 0,         0,          0, 1]], dtype = np.float32)


def rotationY(theta):
    """
    Retorna la matriz que rota theta radianes las coordenadas X,Y y Z respecto al eje Y.
    """
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)

    return np.array([
        [  cos_theta, 0, sin_theta, 0],
        [          0, 1,         0, 0],
        [ -sin_theta, 0, cos_theta, 0],
        [          0, 0,         0, 1]], dtype = np.float32)


def rotationZ(theta):
    """
    Retorna la matriz que rota theta radianes las coordenadas X,Y y Z respecto al eje Z.
    """
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)

    return np.array([
        [ cos_theta, -sin_theta, 0,0],
        [ sin_theta,  cos_theta, 0, 0],
        [         0,          0, 1, 0],
        [         0,          0, 0, 1]], dtype = np.float32)


def matmul(mats):
    """
    Retorna el resultado de la multiplicación de las matrices de la lista mats.
    """
    out = mats[0]
    for i in range(1, len(mats)):
        out = np.matmul(out, mats[i])

    return out


def frustum(left, right, bottom, top, near, far):
    r_l = right - left
    t_b = top - bottom
    f_n = far - near
    return np.array([

        [ 2 * near / r_l,              0, (right + left) / r_l,                     0 ],
        [              0, 2 * near / t_b, (top + bottom) / t_b,                     0 ],
        [              0,              0,  -(far + near) / f_n, -2 * near * far / f_n ],
        [              0,              0,                   -1,                     0 ]
        
        ], dtype = np.float32)


def perspective(fovy, aspect, near, far):
    halfHeight = np.tan(np.pi * fovy / 360) * near
    halfWidth = halfHeight * aspect
    return frustum(-halfWidth, halfWidth, -halfHeight, halfHeight, near, far)


def ortho(left, right, bottom, top, near, far):
    r_l = right - left
    t_b = top - bottom
    f_n = far - near
    return np.array([

        [ 2 / r_l,       0,       0, -(right + left) / r_l],
        [       0, 2 / t_b,       0, -(top + bottom) / t_b],
        [       0,       0,-2 / f_n,   -(far + near) / f_n],
        [       0,       0,       0,                     1]
        
        ], dtype = np.float32)


def lookAt(eye, at, up):

    forward = at - eye
    forward = forward / np.linalg.norm(forward)

    side = np.cross(forward, up)
    side = side / np.linalg.norm(side)

    newUp = np.cross(side, forward)
    newUp = newUp / np.linalg.norm(newUp)

    return np.array([

            [     side[0],     side[1],     side[2],   -np.dot(side, eye)],
            [    newUp[0],    newUp[1],    newUp[2],  -np.dot(newUp, eye)],
            [ -forward[0], -forward[1], -forward[2], np.dot(forward, eye)],
            [           0,           0,           0,                    1]
        
        ], dtype = np.float32)
