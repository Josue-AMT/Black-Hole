"""
Simulación 3D Interactiva de Agujero Negro (Estilo Gargantua)
Optimizada para rendimiento y estabilidad.

Requisitos:
    pip install pygame PyOpenGL PyOpenGL_accelerate numpy

Controles:
    - Mouse (Arrastrar): Rotar cámara
    - Rueda Mouse: Zoom
    - ESC: Salir
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math
import sys
import time

# --- Configuración ---
ANCHO = 1280
ALTO = 720
TITULO = "Simulador Agujero Negro Gargantua - Optimizado"
FPS_OBJETIVO = 60

# Parámetros del Agujero Negro
MASA_AGUJERO = 1.0
RADIO_HORIZONTE = 2.0 * MASA_AGUJERO  # Radio de Schwarzschild
RADIO_DISCO_INTERNO = 3.0 * MASA_AGUJERO
RADIO_DISCO_EXTERNO = 10.0 * MASA_AGUJERO
NUM_ESTRELLAS = 1500  # Reducido para rendimiento inicial, escalable
RESOLUCION_DISCO = 100  # Anillos en el disco de acreción

class Camara:
    def __init__(self):
        self.pos = np.array([0.0, 5.0, 25.0], dtype=np.float32)
        self.objetivo = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.arriba = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        self.radio = 25.0
        self.theta = math.pi / 4  # Ángulo horizontal
        self.phi = math.pi / 6    # Ángulo vertical
        self.actualizar_vector_pos()

    def actualizar_vector_pos(self):
        x = self.radio * math.sin(self.phi) * math.cos(self.theta)
        y = self.radio * math.cos(self.phi)
        z = self.radio * math.sin(self.phi) * math.sin(self.theta)
        self.pos = self.objetivo + np.array([x, y, z], dtype=np.float32)

    def rotar(self, dx, dy):
        sensibilidad = 0.005
        self.theta -= dx * sensibilidad
        self.phi -= dy * sensibilidad
        # Limitar ángulo vertical para evitar giro completo
        self.phi = max(0.1, min(math.pi - 0.1, self.phi))
        self.actualizar_vector_pos()

    def zoom(self, delta):
        self.radio *= (1.0 - delta * 0.05)
        self.radio = max(5.0, min(100.0, self.radio))
        self.actualizar_vector_pos()

def generar_estrellas(num):
    """Genera coordenadas de estrellas aleatorias en una esfera lejana."""
    print(f"Generando {num} estrellas...")
    phi = np.random.uniform(0, np.pi, num)
    theta = np.random.uniform(0, 2 * np.pi, num)
    radio = 80.0  # Esfera lejana
    
    x = radio * np.sin(phi) * np.cos(theta)
    y = radio * np.cos(phi)
    z = radio * np.sin(phi) * np.sin(theta)
    
    # Colores aleatorios ligeramente variados (blanco/azulado/amarillento)
    colores = np.random.uniform(0.8, 1.0, (num, 3))
    return np.column_stack((x, y, z)), colores

def dibujar_horizonte_eventos():
    """Dibuja la esfera negra central."""
    glDisable(GL_LIGHTING)
    glColor3f(0.0, 0.0, 0.0)
    
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GL_SMOOTH)
    gluSphere(quadric, RADIO_HORIZONTE, 32, 32)
    gluDeleteQuadric(quadric)
    glEnable(GL_LIGHTING)

def dibujar_disco_acrecion(tiempo):
    """Dibuja el disco de acreción con textura procedural simple."""
    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    vertices = []
    colores = []
    
    # Generar anillos concéntricos
    for r in np.linspace(RADIO_DISCO_INTERNO, RADIO_DISCO_EXTERNO, RESOLUCION_DISCO):
        for theta in np.linspace(0, 2 * math.pi, 64):
            # Efecto espiral y ondulación
            offset_z = 0.1 * math.sin(3 * theta + tiempo * 2) * (1.0 - (r - RADIO_DISCO_INTERNO)/(RADIO_DISCO_EXTERNO - RADIO_DISCO_INTERNO))
            
            x = r * math.cos(theta)
            y = offset_z
            z = r * math.sin(theta)
            vertices.append((x, y, z))
            
            # Gradiente de color: Blanco/Azul (interno) -> Naranja/Rojo (externo)
            ratio = (r - RADIO_DISCO_INTERNO) / (RADIO_DISCO_EXTERNO - RADIO_DISCO_INTERNO)
            if ratio < 0.3:
                c = [1.0, 1.0, 1.0] # Blanco caliente
            elif ratio < 0.6:
                c = [1.0, 0.6, 0.2] # Naranja
            else:
                c = [0.8, 0.1, 0.1] # Rojo oscuro
            
            # Variación de brillo
            brillo = 0.8 + 0.2 * math.sin(theta * 10 + tiempo * 5)
            colores.append([c[0]*brillo, c[1]*brillo, c[2]*brillo, 0.9]) # Alpha 0.9

    # Dibujar como triángulos (fan o strip simplificado para demo)
    # Para mayor rendimiento en PyOpenGL sin shaders complejos, usamos puntos o líneas si falla GL_QUADS
    glBegin(GL_POINTS) 
    for i, v in enumerate(vertices):
        glColor4fv(colores[i])
        glVertex3fv(v)
    glEnd()
    
    # Opción alternativa más sólida: Triángulos conectando anillos
    # (Omitido para brevedad y estabilidad máxima en entornos variados, los puntos densos simulan bien el gas)
    
    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)

def main():
    pygame.init()
    pygame.display.set_mode((ANCHO, ALTO), DOUBLEBUF | OPENGL)
    pygame.display.set_caption(TITULO)
    
    # Configuración OpenGL
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_POINT_SMOOTH)
    glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
    glPointSize(2.0)
    
    # Proyección
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (ANCHO / ALTO), 0.1, 200.0)
    glMatrixMode(GL_MODELVIEW)
    
    camara = Camara()
    
    # Carga de recursos (con feedback)
    print("Inicializando motor de renderizado...")
    estrellas_pos, estrellas_col = generar_estrellas(NUM_ESTRELLAS)
    print("¡Listo! Iniciando bucle principal.")
    
    reloj = pygame.time.Clock()
    ejecutando = True
    tiempo_inicio = time.time()
    
    # Variables para interacción mouse
    ultimo_mouse_x, ultimo_mouse_y = 0, 0
    raton_presionado = False

    while ejecutando:
        dt = reloj.tick(FPS_OBJETIVO) / 1000.0
        tiempo_total = time.time() - tiempo_inicio
        
        # --- Gestión de Eventos ---
        for evento in pygame.event.get():
            if evento.type == QUIT:
                ejecutando = False
            elif evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                    ejecutando = False
            elif evento.type == MOUSEBUTTONDOWN:
                if evento.button == 1: # Click izquierdo
                    raton_presionado = True
                    ultimo_mouse_x, ultimo_mouse_y = evento.pos
                elif evento.button == 4: # Rueda arriba
                    camara.zoom(1)
                elif evento.button == 5: # Rueda abajo
                    camara.zoom(-1)
            elif evento.type == MOUSEBUTTONUP:
                if evento.button == 1:
                    raton_presionado = False
            elif evento.type == MOUSEMOTION:
                if raton_presionado:
                    x, y = evento.pos
                    dx = x - ultimo_mouse_x
                    dy = y - ultimo_mouse_y
                    camara.rotar(dx, dy)
                    ultimo_mouse_x, ultimo_mouse_y = x, y

        # --- Renderizado ---
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.0, 0.0, 0.0, 1.0) # Fondo negro espacio
        
        glLoadIdentity()
        gluLookAt(camara.pos[0], camara.pos[1], camara.pos[2],
                  camara.objetivo[0], camara.objetivo[1], camara.objetivo[2],
                  camara.arriba[0], camara.arriba[1], camara.arriba[2])
        
        # Rotar todo el sistema ligeramente para dinamismo
        glRotatef(tiempo_total * 2, 0, 1, 0)

        # 1. Dibujar Estrellas de fondo
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_POINTS)
        for i in range(len(estrellas_pos)):
            # Aplicar color individualmente sería lento en modo inmediato, usamos blanco por ahora para rendimiento
            # o podríamos usar VBOs en una versión avanzada.
            glVertex3fv(estrellas_pos[i])
        glEnd()

        # 2. Dibujar Horizonte de Eventos (Esfera Negra)
        dibujar_horizonte_eventos()
        
        # 3. Dibujar Disco de Acreción
        dibujar_disco_acrecion(tiempo_total)
        
        # Nota: La distorsión de lente gravitacional real (ray tracing) es muy costosa para CPU en tiempo real.
        # Esta simulación usa la representación artística estándar: el disco curvado visualmente y la esfera negra.
        # Para ver la distorsión de las estrellas de atrás, se requeriría un shader GLSL complejo o raytracing en GPU.
        # Aquí simulamos el efecto visual del disco rodeando la esfera.

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error crítico: {e}")
        print("Asegúrate de tener instalados: pip install pygame PyOpenGL PyOpenGL_accelerate numpy")
        input("Presiona Enter para salir...")
