import os.path

def getAssetPath(filename):
    """
    Función pata acceder a los archivos de la carpeta assets.
    (Sacada del auxiliar 6)
    """
    thisFilePath = os.path.abspath(__file__)
    thisFolderPath = os.path.dirname(thisFilePath)
    parentFolderPath = os.path.dirname(thisFolderPath)
    assetsDirectory = os.path.join(parentFolderPath, "assets")
    requestedPath = os.path.join(assetsDirectory, filename)
    return requestedPath
