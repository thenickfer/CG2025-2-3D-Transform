from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from Objeto3D import *
from Transicao3D import Transicao3D

o1:Objeto3D
o2:Objeto3D
o3:Transicao3D
window_3_instanciada = False

def initObj1():
    global o1
    glClearColor(0.5, 0.5, 0.9, 1.0)
    glClearDepth(1.0)

    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    o1 = Objeto3D()
    o1.LoadFile('models/easy1.obj')

    DefineLuz()
    PosicUser()

def initObj2():
    global o2
    glClearColor(0.5, 0.5, 0.9, 1.0)
    glClearDepth(1.0)

    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    o2 = Objeto3D()
    o2.LoadFile('models/easy2.obj')

    DefineLuz()
    PosicUser()

def initObj3():
    global o3
    glClearColor(0.5, 0.5, 0.9, 1.0)
    glClearDepth(1.0)

    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    o3 = Transicao3D()
    o3.loadObj1('models/easy1.obj')
    o3.loadObj2('models/easy2.obj')
    o3.preprocess()

    DefineLuz()
    PosicUser()

def DefineLuz():
    # Define cores para um objeto dourado
    luz_ambiente = [0.4, 0.4, 0.4]
    luz_difusa = [0.7, 0.7, 0.7]
    luz_especular = [0.9, 0.9, 0.9]
    posicao_luz = [2.0, 3.0, 0.0]  # PosiÃ§Ã£o da Luz
    especularidade = [1.0, 1.0, 1.0]

    # ****************  Fonte de Luz 0

    glEnable(GL_COLOR_MATERIAL)

    #Habilita o uso de iluminaÃ§Ã£o
    glEnable(GL_LIGHTING)

    #Ativa o uso da luz ambiente
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, luz_ambiente)
    # Define os parametros da luz nÃºmero Zero
    glLightfv(GL_LIGHT0, GL_AMBIENT, luz_ambiente)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, luz_difusa)
    glLightfv(GL_LIGHT0, GL_SPECULAR, luz_especular)
    glLightfv(GL_LIGHT0, GL_POSITION, posicao_luz)
    glEnable(GL_LIGHT0)

    # Ativa o "Color Tracking"
    glEnable(GL_COLOR_MATERIAL)

    # Define a reflectancia do material
    glMaterialfv(GL_FRONT, GL_SPECULAR, especularidade)

    # Define a concentraÃ§Ã£oo do brilho.
    # Quanto maior o valor do Segundo parametro, mais
    # concentrado serÃ¡ o brilho. (Valores vÃ¡lidos: de 0 a 128)
    glMateriali(GL_FRONT, GL_SHININESS, 51)

def PosicUser():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Configura a matriz da projeção perspectiva (FOV, proporção da tela, distância do mínimo antes do clipping, distância máxima antes do clipping
    # https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/gluPerspective.xml
    gluPerspective(60, 16/9, 0.01, 50)  # Projecao perspectiva
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    #Especifica a matriz de transformação da visualização
    # As três primeiras variáveis especificam a posição do observador nos eixos x, y e z
    # As três próximas especificam o ponto de foco nos eixos x, y e z
    # As três últimas especificam o vetor up
    # https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/gluLookAt.xml
    gluLookAt(-2, 6, -8, 0, 0, 0, 0, 1.0, 0)

def DesenhaLadrilho():
    glColor3f(0.5, 0.5, 0.5)  # desenha QUAD preenchido
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    glVertex3f(-0.5, 0.0, -0.5)
    glVertex3f(-0.5, 0.0, 0.5)
    glVertex3f(0.5, 0.0, 0.5)
    glVertex3f(0.5, 0.0, -0.5)
    glEnd()

    glColor3f(1, 1, 1)  # desenha a borda da QUAD
    glBegin(GL_LINE_STRIP)
    glNormal3f(0, 1, 0)
    glVertex3f(-0.5, 0.0, -0.5)
    glVertex3f(-0.5, 0.0, 0.5)
    glVertex3f(0.5, 0.0, 0.5)
    glVertex3f(0.5, 0.0, -0.5)
    glEnd()

def DesenhaPiso():
    glPushMatrix()
    glTranslated(-20, -1, -10)
    for x in range(-20, 20):
        glPushMatrix()
        for z in range(-20, 20):
            DesenhaLadrilho()
            glTranslated(0, 0, 1)
        glPopMatrix()
        glTranslated(1, 0, 0)
    glPopMatrix()

def DesenhaCubo():
    glPushMatrix()
    glColor3f(1, 0, 0)
    glTranslated(0, 0.5, 0)
    glutSolidCube(1)

    glColor3f(0.5, 0.5, 0)
    glTranslated(0, 0.5, 0)
    glRotatef(90, -1, 0, 0)
    glRotatef(45, 0, 0, 1)
    glutSolidCone(1, 1, 4, 4)
    glPopMatrix()

def desenhaObj1():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)

    DesenhaPiso()
    #DesenhaCubo()    
    o1.Desenha()
    o1.DesenhaWireframe()
    o1.DesenhaVertices()

    glutSwapBuffers()
    pass

def desenhaObj2():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)

    DesenhaPiso()
    #DesenhaCubo()    
    o2.Desenha()
    o2.DesenhaWireframe()
    o2.DesenhaVertices()

    glutSwapBuffers()
    pass

def desenhaObj3():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)

    DesenhaPiso()
    #DesenhaCubo()    
    o3.update()

    glutSwapBuffers()
    pass

def teclado(key, x, y):
    if(key == b' '):
        if not window_3_instanciada:
            criaWin3()

    glutPostRedisplay()
    pass

def teste(key, x, y):
    global o3
    o3.update()

def criaWin3():
    global window_3, window_3_instanciada
    # Define o modelo de operacao da GLUT
    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
    # Especifica o tamnho inicial em pixels da janela GLUT
    glutInitWindowSize(400, 400)
    # Especifica a posição de início da janela
    glutInitWindowPosition(100, 100)
    # Cria a janela passando o título da mesma como argumento
    window_3 = glutCreateWindow(b'Computacao Grafica - 3D | 3')
    # Função responsável por fazer as inicializações
    initObj3()
    # Registra a funcao callback de redesenho da janela de visualizacao
    glutDisplayFunc(desenhaObj3)
    glutKeyboardFunc(teste)
    window_3_instanciada = True


def main():
    global window_1, window_2, window_3
    glutInit(sys.argv)

    # Define o modelo de operacao da GLUT
    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
    # Especifica o tamnho inicial em pixels da janela GLUT
    glutInitWindowSize(400, 400)
    # Especifica a posição de início da janela
    glutInitWindowPosition(100, 100)
    # Cria a janela passando o título da mesma como argumento
    window_1 = glutCreateWindow(b'Computacao Grafica - 3D | 1')
    # Função responsável por fazer as inicializações
    initObj1()
    # Registra a funcao callback de redesenho da janela de visualizacao
    glutDisplayFunc(desenhaObj1)
    glutKeyboardFunc(teclado)

    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
    # Especifica o tamnho inicial em pixels da janela GLUT
    glutInitWindowSize(400, 400)
    # Especifica a posição de início da janela
    glutInitWindowPosition(100, 100)
    # Cria a janela passando o título da mesma como argumento
    window_2 = glutCreateWindow(b'Computacao Grafica - 3D | 2')
    # Função responsável por fazer as inicializações
    initObj2()
    # Registra a funcao callback de redesenho da janela de visualizacao
    glutDisplayFunc(desenhaObj2)
    glutKeyboardFunc(teclado)
    

    try:
        # Inicia o processamento e aguarda interacoes do usuario
        glutMainLoop()
    except SystemExit:
        pass

if __name__ == '__main__':
    main()