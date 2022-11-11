import glfw
from OpenGL.GL import *
from libraries.gpu_shape_t2p1 import GPUShape
import libraries.easy_shaders_t2p1 as es
import libraries.basic_shapes_t2p1 as bs
import libraries.transformations_t2p1 as tr
from libraries.constants_t2p1 import *
import libraries.controllers_t2p1 as con
from libraries.assets_path_t2p1 import *
import libraries.scene_graph_t2p1 as sg
import math
width = SCREEN_WIDTH
height = SCREEN_HEIGHT

# Se crean controladores 
camera = con.Camera()
controller = con.Trees()


def on_key(window, key, scancode, action, mods):
    """
    Función para incorporar el uso de teclas.
    """
    step = 1/5
    if action != glfw.PRESS:
        return

    if key == glfw.KEY_1:
        controller.season=1
    
    elif key == glfw.KEY_2:
        controller.season=2
    
    elif key == glfw.KEY_3:
        controller.season=3
    
    elif key == glfw.KEY_4:
        controller.season=4

    elif key == glfw.KEY_A:
        camera.theta += PI/16
    
    elif key == glfw.KEY_D:
        camera.theta -= PI/16

    elif key == glfw.KEY_S:
        camera.pos -= np.array([step*np.cos(camera.theta),step*np.sin(camera.theta),0])

    elif key == glfw.KEY_W:
        camera.pos += np.array([step*np.cos(camera.theta),step*np.sin(camera.theta),0])

    elif key == glfw.KEY_X:
        camera.pos += np.array([0,0,step])

    elif key == glfw.KEY_C:
        camera.pos -= np.array([0,0,step])
    
    elif key == glfw.KEY_SPACE:
        camera.changeView()
        
    
def createHouse(pipeline,form=2,color=1):
    """
    Función que crea una casa y la entrega en un nodo.
    """
    # form=1:Casa no cúbica
    # form=2:Casa cúbica 

    # Primitivas
    # Paredes de casa cúbica
    cubeWalls = bs.createTextureCube(1,1)
    gpuCubeWalls = GPUShape().initBuffers()
    pipeline.setupVAO(gpuCubeWalls)
    gpuCubeWalls.fillBuffers(cubeWalls.vertexData, cubeWalls.indexData, GL_STATIC_DRAW)
    if color==2:
        gpuCubeWalls.texture = es.textureSimpleSetup(getAssetPath('pale_yellow_wall.jpg'),GL_REPEAT,GL_REPEAT,GL_LINEAR,GL_LINEAR)
    elif color==1:
        gpuCubeWalls.texture = es.textureSimpleSetup(getAssetPath('white_wall.jpg'),GL_REPEAT,GL_REPEAT,GL_LINEAR,GL_LINEAR)

    # Paredes casa no cúbica
    noCubeWalls = bs.createTextureHouseWalls()
    gpuNoCubeWalls = GPUShape().initBuffers()
    pipeline.setupVAO(gpuNoCubeWalls)
    gpuNoCubeWalls.fillBuffers(noCubeWalls.vertexData,noCubeWalls.indexData,GL_STATIC_DRAW)
    if color==2:
        gpuNoCubeWalls.texture = es.textureSimpleSetup(getAssetPath('pale_yellow_wall.jpg'),GL_REPEAT,GL_REPEAT,GL_LINEAR,GL_LINEAR)
    elif color==1:
        gpuNoCubeWalls.texture = es.textureSimpleSetup(getAssetPath('white_wall.jpg'),GL_REPEAT,GL_REPEAT,GL_LINEAR,GL_LINEAR)
        
    # Techo
    roof = bs.createTexturePiramide()
    gpuRoof = GPUShape().initBuffers()
    pipeline.setupVAO(gpuRoof)
    gpuRoof.fillBuffers(roof.vertexData,roof.indexData,GL_STATIC_DRAW)
    gpuRoof.texture = es.textureSimpleSetup(getAssetPath('roof.jpg'),GL_REPEAT,GL_REPEAT,GL_LINEAR,GL_LINEAR)

    # Techo casa no cúbica
    roof_part = bs.createTextureCube(1,1)
    gpuRoof_part = GPUShape().initBuffers()
    pipeline.setupVAO(gpuRoof_part)
    gpuRoof_part.fillBuffers(roof_part.vertexData,roof_part.indexData,GL_STATIC_DRAW)
    gpuRoof_part.texture = es.textureSimpleSetup(getAssetPath('roof.jpg'),GL_REPEAT,GL_REPEAT,GL_LINEAR,GL_LINEAR)

    # puerta
    door = bs.createTextureCube(1,1)
    gpuDoor = GPUShape().initBuffers()
    pipeline.setupVAO(gpuDoor)
    gpuDoor.fillBuffers(door.vertexData,door.indexData,GL_STATIC_DRAW)
    gpuDoor.texture = es.textureSimpleSetup(getAssetPath('door.jpg'),GL_REPEAT,GL_REPEAT,GL_LINEAR,GL_LINEAR)

    # Ventana 
    window = bs.createTextureCube(1,1)
    gpuWindow = GPUShape().initBuffers()
    pipeline.setupVAO(gpuWindow)
    gpuWindow.fillBuffers(window.vertexData,window.indexData,GL_STATIC_DRAW)
    gpuWindow.texture = es.textureSimpleSetup(getAssetPath('window.png'),GL_REPEAT,GL_REPEAT,GL_LINEAR,GL_LINEAR)

    # Nodos
    # Casa
    house = sg.SceneGraphNode('house')
    
    # Parades
    house_walls = sg.SceneGraphNode('house_walls')
    if form==2:
        house_walls.childs += [gpuCubeWalls]
    elif form == 1:
        house_walls.transform =tr.scale(1,2/3,1)
        house_walls.childs +=[gpuNoCubeWalls]
    house.childs += [house_walls]

    # Techo
    house_roof = sg.SceneGraphNode('house_roof')
    if form==2:     
        house_roof.transform = tr.matmul([
            tr.translate(0,0,3/4),
            tr.scale(6/5, 6/5, 1/2)])
        house_roof.childs += [gpuRoof]
        house.childs += [house_roof]
    elif form==1:
        for i in range(2):
            house_roof_part = sg.SceneGraphNode('roof_part'+str(i))
            house_roof_part.transform = tr.matmul([
                tr.translate(0.25-i/2,0,3/4),
                tr.rotationZ(i*PI),
                tr.rotationY(PI/4),
                tr.scale(0.75,2,1/20),
                tr.rotationZ(PI/2)])
            house_roof_part.childs+=[gpuRoof_part]
            house.childs+=[house_roof_part]
        
    # Puerta
    house_door = sg.SceneGraphNode('house_door')
    house_door.transform = tr.matmul([
        tr.translate(0.5,0,-2/6),
        tr.scale(1/30,1/6,1/3)])
    house_door.childs += [gpuDoor]
    house.childs += [house_door]

    # Ventana
    for i in range(4):
        house_window = sg.SceneGraphNode('house_window')
        if i==0:
            house_window.transform = tr.matmul([
                tr.translate(0.5,1/4,1/6),
                tr.scale(1/20,1/6,1/4)])
        elif i==1:
            house_window.transform = tr.matmul([
                tr.translate(0.5,-1/4,1/6),
                tr.scale(1/20,1/6,1/4)])
        elif i==2:
            if form ==2:
                house_window.transform = tr.matmul([
                    tr.rotationZ(PI/2),
                    tr.translate(0.5,-1/4,-1/6),
                    tr.scale(1/20,1/6,1/4)])
            else:
                house_window.transform = tr.matmul([
                    tr.translate(0,-1,-1/6),
                    tr.rotationZ(PI/2),
                    tr.scale(1/20,1/6,1/4)])
        else:
            if form ==2:
                house_window.transform = tr.matmul([
                    tr.rotationZ(-PI/2),
                    tr.translate(0.5,1/4,-1/6),
                    tr.scale(1/20,1/6,1/4)])
                
            else:
                house_window.transform = tr.matmul([
                    tr.translate(0,1,-1/6),
                    tr.rotationZ(-PI/2),
                    tr.scale(1/20,1/6,1/4)])
        house_window.childs += [gpuWindow]
        house.childs += [house_window]
    return house

def createTree(pipeline,season):
    """
    Función para crear un arbol y lo entrega en un nodo
    """
    # PRIMITIVAS
    # Tronco
    trunk = bs.createTexturePrisma(1/4, 20)
    gpuTrunk = GPUShape().initBuffers()
    pipeline.setupVAO(gpuTrunk)
    gpuTrunk.fillBuffers(trunk.vertexData, trunk.indexData, GL_STATIC_DRAW)
    gpuTrunk.texture = es.textureSimpleSetup(getAssetPath("tree_trunk.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    # Hojas
    leaves = bs.createTextureSphere(1,10)
    gpuLeaves = GPUShape().initBuffers()
    pipeline.setupVAO(gpuLeaves)
    gpuLeaves.fillBuffers(leaves.vertexData, leaves.indexData, GL_STATIC_DRAW)
    if season == 2:
        gpuLeaves.texture = es.textureSimpleSetup(getAssetPath("autumn_leaves.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    elif season == 4:
        gpuLeaves.texture = es.textureSimpleSetup(getAssetPath("flowers_leaves.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    else:
        gpuLeaves.texture = es.textureSimpleSetup(getAssetPath("green_leaves.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)


    # NODOS
    # Árbol 
    tree = sg.SceneGraphNode('tree')
    
    # Tronco del árbol
    tree_trunk = sg.SceneGraphNode('tree_trunk')
    tree_trunk.transform = tr.scale(1,1,1.5)
    tree_trunk.childs+=[gpuTrunk]
    tree.childs+=[tree_trunk]

    # Copa del árbol
    if season != 3:
        tree_leaves = sg.SceneGraphNode('tree_leaves')
        tree_leaves.transform = tr.matmul([tr.translate(0,0,1.5), tr.uniscale(7/8)])
        tree_leaves.childs+=[gpuLeaves]
        tree.childs+= [tree_leaves]

    # Rama pequeña
    little_branch = sg.SceneGraphNode('little_branch')
    
    # Tronco de rama pequeña
    little_branch_trunk = sg.SceneGraphNode('little_branch_trunk')
    little_branch_trunk.childs += [gpuTrunk]
    little_branch.childs += [little_branch_trunk]

    # Hojas de rama pequeña
    if season != 3:
        little_branch_leaves = sg.SceneGraphNode('little_branch_leaves')
        little_branch_leaves.transform = tr.matmul([tr.translate(0,0,1), tr.uniscale(7/8)])
        little_branch_leaves.childs += [gpuLeaves]
        little_branch.childs += [little_branch_leaves]

    # Rama grande
    tree_branch = sg.SceneGraphNode('tree_branch')
    
    # Rama sin hojas
    stick = sg.SceneGraphNode('stick')
    stick.transform = tr.scale(1/4, 1/4, 2/3)
    stick.childs += [gpuTrunk]
    tree_branch.childs += [stick]

    # Ramitas con hojas
    for i in range(3):
        branch_part = sg.SceneGraphNode('branch_part'+str(i))
        branch_part.transform = tr.matmul([
            tr.rotationZ(i*2*PI/3),
            tr.translate(0, 1/10,(i-1)/5),
            tr.rotationX(-PI/3),
            tr.uniscale(2/9)])
        branch_part.childs += [little_branch]
        tree_branch.childs += [branch_part]
    
    # Hojas de rama grande 
    if season != 3:
        branch_leaves = sg.SceneGraphNode('branch_leaves')
        branch_leaves.transform = tr.matmul([
            tr.translate(0,0,2/3),
            tr.uniscale(7/18)])
        branch_leaves.childs += [gpuLeaves]
        tree_branch.childs += [branch_leaves]
    
    # Se agragan las ramas al árbol
    for i in range(3):
        on_tree = sg.SceneGraphNode('tree_branch'+str(i))
        on_tree.transform = tr.matmul([
            tr.rotationZ(i*2*PI/3),
            tr.translate(0,np.sin(PI/3)*0.4,1/3*(1-i)+0.1),
            tr.rotationX(-PI/3),
            tr.uniscale(5/8)
        ])
        on_tree.childs += [tree_branch]
        tree.childs += [on_tree]
    
    return tree

def createBase(pipeline):
    """
    Función que crea la base de la escena. La base es la unión del pasto, las calles y las casas.
    """
    # Primitivas
    # Base
    grass = bs.createTextureCube(5,5)
    gpuGrass = GPUShape().initBuffers()
    pipeline.setupVAO(gpuGrass)
    gpuGrass.fillBuffers(grass.vertexData, grass.indexData,GL_STATIC_DRAW)
    gpuGrass.texture = es.textureSimpleSetup(getAssetPath('grass.jpg'), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    # Calle 
    road = bs.createTextureCube(1,1)
    gpuRoad = GPUShape().initBuffers()
    pipeline.setupVAO(gpuRoad)
    gpuRoad.fillBuffers(road.vertexData,road.indexData,GL_STATIC_DRAW)
    gpuRoad.texture = es.textureSimpleSetup(getAssetPath('road.jpg'), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    
    # Nodos
    # Base
    base = sg.SceneGraphNode('base')
    
    # Pasto
    grassNode = sg.SceneGraphNode('grass')
    grassNode.transform = tr.matmul([
            tr.uniscale(5),
            tr.scale(1,2,1/50)])
    grassNode.childs += [gpuGrass]
    base.childs += [grassNode]

    #Calles
    roads_transforms=[
        tr.matmul([
            tr.translate(5*7/16,5*7/16,1/50),
            tr.scale(1,9,1/10),
            tr.uniscale(5/8)]),
        tr.matmul([
            tr.translate(-5*7/16,0,1/50),
            tr.scale(1,16,1/10),
            tr.uniscale(5/8)]),
        tr.matmul([
            tr.translate(0,5*15/16,1/50),
            tr.rotationZ(PI/2),
            tr.scale(1,6,1/10),
            tr.uniscale(5/8)]),
        tr.matmul([
            tr.translate(0,-5/2,1/50),
            tr.rotationZ(-PI/4),
            tr.scale(1,7,1/10),
            tr.uniscale(5/8*math.sqrt(2))])]

    for i in range(4):
        roadi = sg.SceneGraphNode('road'+str(i))
        roadi.transform = roads_transforms[i]
        roadi.childs += [gpuRoad]
        base.childs += [roadi]
    
    # Casas
    house2= createHouse(pipeline,2)
    scaledHouse = sg.SceneGraphNode('scaledHouse')
    scaledHouse.transform= tr.uniscale(4/8)
    scaledHouse.childs+=[house2]
    for i in range(5):
        nodo=sg.SceneGraphNode("nodo"+str(i))
        nodo.transform = tr.matmul([
            tr.translate(-5/4,-0.5+i*7/8,0.3),
            tr.rotationZ(PI)])
        nodo.childs+=[scaledHouse]
        base.childs+=[nodo]
    
    nodoAux=sg.SceneGraphNode('nodoAux')
    nodoAux.transform =tr.matmul([
        tr.translate(5/4,-0.5+7/8,0.3)])
    nodoAux.childs+=[scaledHouse]
    base.childs+=[nodoAux]
    for i in range(3):
        nodoAux=sg.SceneGraphNode('nodoAux'+str(i))
        nodoAux.transform = tr.translate(5/4,-0.5+21/8+i*7/8,0.3)
        nodoAux.childs+=[scaledHouse]
        base.childs+=[nodoAux]
    for i in range(6):
        nodoAux=sg.SceneGraphNode('nodoAuxA'+str(i))
        nodoAux.transform = tr.translate(0,-0.5+i*7/8,0.3)
        nodoAux.childs+=[scaledHouse]
        base.childs+=[nodoAux]
    
    nodoAux=sg.SceneGraphNode('nodoAux11')
    nodoAux.transform =tr.matmul([
        tr.translate(-5/4+2/8,-0.5+35/8,0.2),
        tr.rotationZ(PI/2),
        tr.uniscale(1/2)])
    nodoAux.childs+=[scaledHouse]
    base.childs+=[nodoAux]

    nodoAux=sg.SceneGraphNode('nodoAux11')
    nodoAux.transform =tr.matmul([
        tr.translate(-5/4-2/8,-0.5+35/8,0.2),
        tr.rotationZ(PI/2),
        tr.uniscale(1/2)])
    nodoAux.childs+=[scaledHouse]
    base.childs+=[nodoAux]

    for i in range(2):
        nodoAux=sg.SceneGraphNode('nodoAuxi'+str(i))
        nodoAux.transform = tr.matmul([tr.translate(-5/4,-0.5-(i+1)*4/8,0.3),tr.scale(1,1/2,1),tr.rotationZ(PI)])
        nodoAux.childs+=[scaledHouse]
        base.childs+=[nodoAux]

    return base

def createScene(base,pipeline,season):
    
    scene = sg.SceneGraphNode('scene')

    scene.childs+=[base]

    tree = createTree(pipeline,season)
    # Se agregan los árboles a la escena final
    for i in range(3):
        for j in range(i+1):
            nodo_arbol=sg.SceneGraphNode('arbol0'+str(i)+'_'+str(j))
            nodo_arbol.transform=tr.matmul([
                tr.translate(-5/8 + i*5/4, -35/8 + j* 5/4 ,0.35),
                tr.uniscale(1/2)])
            nodo_arbol.childs+=[tree]
            scene.childs+=[nodo_arbol]

    for i in range(2):
        for j in range(i+1):
            nodo_arbol=sg.SceneGraphNode('arbol1'+str(i)+'_'+str(j))
            nodo_arbol.transform=tr.matmul([
                tr.translate(i*5/4, -30/8 + j* 5/4 ,0.35),
                tr.uniscale(1/2)])
            nodo_arbol.childs+=[tree]
            scene.childs+=[nodo_arbol]
    
    return scene


def main():
    
    if not glfw.init():
        glfw.set_window_should_close(window, True)
        return -1

    window = glfw.create_window(width, height, "Tarea 2 Parte 1: Modelando Edificios", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)
        return -1

    glfw.make_context_current(window)

    glfw.set_key_callback(window, on_key)
 
    pipeline = es.SimpleTextureModelViewProjectionShaderProgram()

    glUseProgram(pipeline.shaderProgram)

    glClearColor(0.0, 170/255, 228/255, 1.0)

    glEnable(GL_DEPTH_TEST)

    base = createBase(pipeline)

    while not glfw.window_should_close(window):
        glfw.poll_events()
    
        # Se crea la escena
        scene = createScene(base,pipeline,controller.season)
    
        # Cambio de cámara y perspectiva
        if camera.upperEye:
            camera.limits()
            view = camera.getView()
            projection = tr.perspective(45, float(width)/float(height), 0.1, 100)
        else:
            factor = 9/16
            view = camera.getOrtoView()
            projection = tr.ortho(-5,5,-5*factor,5*factor,0.1,100)

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        # Se dibuja la escena
        sg.drawSceneGraphNode(scene,pipeline,"model")
        glfw.swap_buffers(window)

    scene.clear()
    base.clear()
    glfw.terminate()

    return 0

if __name__ == "__main__":
    main()

