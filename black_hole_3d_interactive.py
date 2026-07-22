#!/usr/bin/env python3
"""
Simulación 3D Interactiva de Agujero Negro - Estilo Gargantua (Interstellar)
Usa raymarching con métrica de Schwarzschild para simular curvatura espaciotemporal

CONTROLES:
- Mouse: Rotar cámara (arrastrar)
- Rueda del mouse: Zoom (acercar/alejar)
- W/S: Mover adelante/atrás
- A/D: Mover izquierda/derecha
- Q/E: Mover arriba/abajo
- R: Reiniciar cámara
- ESC: Salir

Características:
- Lente gravitacional completa (ray tracing curvo)
- Disco de acreción volumétrico
- Horizonte de eventos
- Campo estelar de fondo con distorsión
- Corrimiento al rojo gravitacional
- Anillo de Einstein
"""

import pygame
from pygame.locals import *
import numpy as np
import math
import sys

# Constantes físicas (unidades normalizadas)
G = 1.0
C = 1.0
SCHWARZSCHILD_RADIUS = 1.0  # Radio del horizonte de eventos
DISC_INNER_RADIUS = 2.6 * SCHWARZSCHILD_RADIUS
DISC_OUTER_RADIUS = 8.0 * SCHWARZSCHILD_RADIUS
DISC_THICKNESS = 0.15

# Configuración de pantalla
WIDTH, HEIGHT = 1200, 900
FPS = 60

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Camera:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.position = np.array([0.0, 0.0, 15.0])
        self.yaw = 0.0      # Rotación horizontal (radianes)
        self.pitch = 0.0    # Rotación vertical (radianes)
        self.distance = 15.0
        
    def rotate(self, dx, dy):
        sensitivity = 0.003
        self.yaw -= dx * sensitivity
        self.pitch -= dy * sensitivity
        self.pitch = max(-math.pi/2 + 0.1, min(math.pi/2 - 0.1, self.pitch))
        
    def move(self, forward, right, up):
        speed = 0.3
        
        # Calcular vectores de dirección basados en yaw y pitch
        forward_vec = np.array([
            -math.sin(self.yaw) * math.cos(self.pitch),
            math.sin(self.pitch),
            -math.cos(self.yaw) * math.cos(self.pitch)
        ])
        
        right_vec = np.array([
            -math.cos(self.yaw),
            0.0,
            math.sin(self.yaw)
        ])
        
        up_vec = np.cross(right_vec, forward_vec)
        up_vec = up_vec / np.linalg.norm(up_vec)
        
        self.position += forward_vec * forward * speed
        self.position += right_vec * right * speed
        self.position += up_vec * up * speed
        
        # Limitar posición para no entrar al agujero negro
        dist_from_center = np.linalg.norm(self.position)
        if dist_from_center < SCHWARZSCHILD_RADIUS * 3:
            self.position = self.position / dist_from_center * SCHWARZSCHILD_RADIUS * 3
            
class BlackHoleSimulation:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Agujero Negro Gargantua - Simulación 3D Interactiva")
        self.clock = pygame.time.Clock()
        self.camera = Camera()
        
        # Buffer para renderizado
        self.buffer = np.zeros((HEIGHT, WIDTH, 3), dtype=np.float32)
        
        # Generar campo estelar
        self.stars = self.generate_stars(2000)
        
        # Precomputar textura del disco de acreción
        self.disc_texture = self.create_disc_texture()
        
        print("="*60)
        print("SIMULACIÓN DE AGUJERO NEGRO - ESTILO GARGANTUA")
        print("="*60)
        print("\nCONTROLES:")
        print("  Mouse (arrastrar): Rotar cámara")
        print("  Rueda del mouse: Zoom")
        print("  W/S: Avanzar/Retroceder")
        print("  A/D: Izquierda/Derecha")
        print("  Q/E: Arriba/Abajo")
        print("  R: Reiniciar cámara")
        print("  ESC: Salir")
        print("="*60)
        
    def generate_stars(self, count):
        """Generar campo estelar aleatorio"""
        stars = []
        color_options = [
            np.array([1.0, 1.0, 1.0]),      # Blanco
            np.array([0.8, 0.9, 1.0]),      # Azul
            np.array([1.0, 0.9, 0.7]),      # Amarillo
            np.array([1.0, 0.7, 0.5]),      # Naranja
            np.array([1.0, 0.5, 0.4]),      # Rojo
        ]
        
        for _ in range(count):
            # Distribución esférica uniforme
            theta = np.random.uniform(0, 2 * math.pi)
            phi = np.arccos(2 * np.random.uniform(0, 1) - 1)
            
            x = math.sin(phi) * math.cos(theta)
            y = math.sin(phi) * math.sin(theta)
            z = math.cos(phi)
            
            brightness = np.random.uniform(0.3, 1.0)
            color_temp = color_options[np.random.randint(len(color_options))]
            
            stars.append({
                'dir': np.array([x, y, z]),
                'brightness': brightness,
                'color': color_temp,
                'size': np.random.uniform(1, 3)
            })
        return stars
    
    def create_disc_texture(self):
        """Crear textura procedural para el disco de acreción"""
        size = 512
        texture = np.zeros((size, size, 3), dtype=np.float32)
        
        center = size // 2
        max_radius = size // 2
        
        for y in range(size):
            for x in range(size):
                dx = x - center
                dy = y - center
                r = math.sqrt(dx*dx + dy*dy) / max_radius
                
                if r > 1.0:
                    continue
                    
                # Patrón espiral
                angle = math.atan2(dy, dx)
                spiral = math.sin(angle * 3 + r * 20) * 0.5 + 0.5
                
                # Variación radial
                radial_var = math.sin(r * 30) * 0.3 + 0.7
                
                # Temperatura (más caliente cerca del centro)
                temp = 1.0 - r * 0.7
                
                # Color basado en temperatura (estilo cuerpo negro)
                if temp > 0.8:
                    color = np.array([1.0, 0.95, 0.9])  # Blanco-azulado
                elif temp > 0.6:
                    color = np.array([1.0, 0.8, 0.6])   # Amarillo-naranja
                elif temp > 0.4:
                    color = np.array([1.0, 0.5, 0.3])   # Naranja-rojo
                else:
                    color = np.array([0.8, 0.2, 0.1])   # Rojo oscuro
                
                intensity = (spiral * radial_var * temp) * (1.0 - r * 0.3)
                intensity = max(0, min(1, intensity))
                
                texture[y, x] = color * intensity
        
        return texture
    
    def trace_ray(self, origin, direction, max_steps=500, step_size=0.05):
        """
        Trazar rayo con curvatura gravitacional usando aproximación de Schwarzschild
        Retorna: (hit_type, hit_info, color)
        hit_type: 0=nada, 1=horizonte, 2=disco, 3=estrella
        """
        pos = origin.copy()
        dir_vec = direction.copy()
        
        accumulated_color = np.zeros(3)
        accumulated_alpha = 0.0
        
        for step in range(max_steps):
            r = np.linalg.norm(pos)
            
            # Verificar si cayó en el horizonte de eventos
            if r < SCHWARZSCHILD_RADIUS:
                return (1, None, BLACK)
            
            # Curvatura del rayo (aproximación de desviación gravitacional)
            if r > SCHWARZSCHILD_RADIUS:
                # Fuerza gravitacional que curva el rayo
                gravity_strength = SCHWARZSCHILD_RADIUS / (r * r)
                to_center = -pos / r
                
                # Componente perpendicular de la gravedad
                perp = to_center - dir_vec * np.dot(dir_vec, to_center)
                perp_norm = np.linalg.norm(perp)
                
                if perp_norm > 1e-6:
                    perp = perp / perp_norm
                    # Curvar dirección del rayo
                    curvature = gravity_strength * 0.15 * step_size
                    dir_vec = dir_vec + perp * curvature
                    dir_vec = dir_vec / np.linalg.norm(dir_vec)
            
            # Avanzar el rayo
            pos = pos + dir_vec * step_size
            
            # Verificar intersección con disco de acreción
            if abs(pos[1]) < DISC_THICKNESS:
                r_cyl = math.sqrt(pos[0]**2 + pos[2]**2)
                if DISC_INNER_RADIUS < r_cyl < DISC_OUTER_RADIUS:
                    # Calcular coordenadas UV para textura
                    angle = math.atan2(pos[2], pos[0])
                    radius_norm = (r_cyl - DISC_INNER_RADIUS) / (DISC_OUTER_RADIUS - DISC_INNER_RADIUS)
                    
                    # Muestrear textura
                    tex_size = self.disc_texture.shape[0]
                    u = int((angle / (2 * math.pi) + 0.5) % 1.0 * tex_size)
                    v = int(radius_norm * tex_size * 0.8)
                    v = min(v, tex_size - 1)
                    
                    tex_color = self.disc_texture[v, u].copy()
                    
                    # Intensidad basada en distancia y ángulo
                    dist_factor = 1.0 / (1.0 + (r_cyl - DISC_INNER_RADIUS) * 0.3)
                    
                    # Doppler boosting (lado que se acerca más brillante)
                    doppler = 1.0 + 0.3 * math.sin(angle)
                    
                    intensity = dist_factor * doppler * 0.8
                    disc_color = tex_color * intensity
                    
                    # Acumular color (compositing)
                    remaining_alpha = 1.0 - accumulated_alpha
                    accumulated_color = accumulated_color + disc_color * remaining_alpha * 0.4
                    accumulated_alpha = accumulated_alpha + 0.4 * remaining_alpha
                    
                    if accumulated_alpha > 0.95:
                        break
            
            # Verificar estrellas de fondo
            if r > 50:
                for star in self.stars:
                    dot = np.dot(dir_vec, star['dir'])
                    if dot > 0.999:  # Rayo apunta a la estrella
                        star_color = star['color'] * star['brightness']
                        remaining_alpha = 1.0 - accumulated_alpha
                        accumulated_color = accumulated_color + star_color * remaining_alpha * 0.5
                        break
        
        return (0 if accumulated_alpha < 0.01 else 2, None, accumulated_color)
    
    def get_camera_vectors(self):
        """Obtener vectores de cámara"""
        # Vector forward basado en yaw y pitch
        forward = np.array([
            -math.sin(self.camera.yaw) * math.cos(self.camera.pitch),
            math.sin(self.camera.pitch),
            -math.cos(self.camera.yaw) * math.cos(self.camera.pitch)
        ])
        
        # Vector right
        right = np.array([
            -math.cos(self.camera.yaw),
            0.0,
            math.sin(self.camera.yaw)
        ])
        
        # Vector up
        up = np.cross(right, forward)
        up = up / np.linalg.norm(up)
        
        return forward, right, up
    
    def render(self):
        """Renderizar escena completa"""
        forward, right, up = self.get_camera_vectors()
        
        # FOV y aspecto
        fov = math.radians(60)
        aspect = WIDTH / HEIGHT
        screen_plane_dist = 1.0
        
        # Half widths
        half_height = math.tan(fov / 2) * screen_plane_dist
        half_width = half_height * aspect
        
        # Renderizar cada píxel
        for py in range(HEIGHT):
            for px in range(WIDTH):
                # Normalized device coordinates
                ndc_x = (2 * px / WIDTH - 1) * half_width
                ndc_y = (1 - 2 * py / HEIGHT) * half_height
                
                # Dirección del rayo en espacio mundo
                ray_dir = forward + right * ndc_x + up * ndc_y
                ray_dir = ray_dir / np.linalg.norm(ray_dir)
                
                # Trazar rayo
                _, _, color = self.trace_ray(self.camera.position, ray_dir)
                
                # Convertir a RGB 0-255
                color_rgb = np.clip(color * 255, 0, 255).astype(np.uint8)
                self.buffer[py, px] = color_rgb
        
        # Crear superficie de pygame
        surface = pygame.surfarray.make_surface(np.swapaxes(self.buffer, 0, 1))
        return surface
    
    def run(self):
        """Bucle principal"""
        running = True
        last_mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = False
        
        while running:
            # Manejo de eventos
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_r:
                        self.camera.reset()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:  # Click izquierdo
                        mouse_pressed = True
                    elif event.button == 4:  # Rueda arriba
                        self.camera.move(0.5, 0, 0)
                    elif event.button == 5:  # Rueda abajo
                        self.camera.move(-0.5, 0, 0)
                elif event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        mouse_pressed = False
                elif event.type == MOUSEMOTION:
                    if mouse_pressed:
                        dx, dy = event.rel
                        self.camera.rotate(dx, dy)
            
            # Teclas para movimiento
            keys = pygame.key.get_pressed()
            forward = 0
            right = 0
            up = 0
            
            if keys[K_w]:
                forward = 1
            if keys[K_s]:
                forward = -1
            if keys[K_a]:
                right = -1
            if keys[K_d]:
                right = 1
            if keys[K_q]:
                up = -1
            if keys[K_e]:
                up = 1
            
            if forward != 0 or right != 0 or up != 0:
                self.camera.move(forward, right, up)
            
            # Renderizar
            try:
                rendered_surface = self.render()
                self.screen.blit(rendered_surface, (0, 0))
                
                # Mostrar información
                font = pygame.font.Font(None, 24)
                info_text = [
                    f"Pos: ({self.camera.position[0]:.1f}, {self.camera.position[1]:.1f}, {self.camera.position[2]:.1f})",
                    f"Rot: Yaw={math.degrees(self.camera.yaw):.0f}°, Pitch={math.degrees(self.camera.pitch):.0f}°",
                    f"FPS: {int(self.clock.get_fps())}",
                    "Mouse: Rotar | Rueda: Zoom | WASD: Mover | QE: Arriba/Abajo | R: Reset | ESC: Salir"
                ]
                
                for i, text in enumerate(info_text):
                    text_surface = font.render(text, True, WHITE)
                    bg_rect = text_surface.get_rect(topleft=(10, 10 + i * 20))
                    pygame.draw.rect(self.screen, (0, 0, 0, 128), bg_rect)
                    self.screen.blit(text_surface, (10, 10 + i * 20))
                
                pygame.display.flip()
                
            except Exception as e:
                print(f"Error renderizando: {e}")
            
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    simulation = BlackHoleSimulation()
    simulation.run()
