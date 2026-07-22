"""
Simulación de Agujero Negro tipo Gargantua (Interstellar)
Este código simula los efectos de lente gravitacional y el disco de acreción
característicos del agujero negro de la película Interstellar.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Circle
import warnings
warnings.filterwarnings('ignore')

# Configuración de la simulación
def create_black_hole_simulation(resolution=1000, black_hole_radius=0.3):
    """
    Crea una simulación visual de un agujero negro con disco de acreción.
    
    Parámetros:
    - resolution: Resolución de la imagen (pixels)
    - black_hole_radius: Radio aparente del horizonte de eventos
    """
    
    print("Generando simulación del agujero negro Gargantua...")
    print(f"Resolución: {resolution}x{resolution}")
    
    # Crear grid de coordenadas
    x = np.linspace(-2, 2, resolution)
    y = np.linspace(-2, 2, resolution)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)
    
    # Horizonte de eventos (círculo negro central)
    event_horizon = R < black_hole_radius
    
    # Disco de acreción interno (más brillante, más caliente)
    accretion_disk_inner = (R > black_hole_radius * 1.5) & (R < black_hole_radius * 3.5)
    
    # Disco de acreción externo (menos brillante, más frío)
    accretion_disk_outer = (R >= black_hole_radius * 3.5) & (R < black_hole_radius * 6)
    
    # Efecto de lente gravitacional (anillo de Einstein)
    einstein_ring = (R > black_hole_radius * 1.1) & (R < black_hole_radius * 1.8)
    
    # Crear imagen RGB
    image = np.zeros((resolution, resolution, 3))
    
    # Colores del disco de acreción (gradiente de temperatura)
    # Interior: blanco-azulado (muy caliente)
    # Medio: naranja-amarillo (caliente)
    # Exterior: rojo (menos caliente)
    
    # Fase angular para dar textura al disco
    theta = np.arctan2(Y, X)
    spiral_pattern = np.sin(3 * theta + 5 / (R + 0.1)) * np.exp(-(R - black_hole_radius * 2.5)**2 / 0.5)
    
    # Disco interno (blanco-azul)
    intensity_inner = np.clip(np.exp(-(R - black_hole_radius * 2)**2 / 0.3), 0, 1)
    intensity_inner *= (1 + spiral_pattern * 0.3)
    image[accretion_disk_inner, 0] = intensity_inner[accretion_disk_inner] * 1.0  # R
    image[accretion_disk_inner, 1] = intensity_inner[accretion_disk_inner] * 0.9  # G
    image[accretion_disk_inner, 2] = intensity_inner[accretion_disk_inner] * 0.7  # B
    
    # Disco externo (naranja-rojo)
    intensity_outer = np.clip(np.exp(-(R - black_hole_radius * 4.5)**2 / 1.0), 0, 1)
    intensity_outer *= (1 + spiral_pattern * 0.2)
    image[accretion_disk_outer, 0] = intensity_outer[accretion_disk_outer] * 1.0  # R
    image[accretion_disk_outer, 1] = intensity_outer[accretion_disk_outer] * 0.5  # G
    image[accretion_disk_outer, 2] = intensity_outer[accretion_disk_outer] * 0.2  # B
    
    # Anillo de Einstein (lente gravitacional)
    einstein_intensity = np.clip(np.exp(-(R - black_hole_radius * 1.4)**2 / 0.02), 0, 1)
    image[einstein_ring, 0] += einstein_intensity[einstein_ring] * 0.8
    image[einstein_ring, 1] += einstein_intensity[einstein_ring] * 0.8
    image[einstein_ring, 2] += einstein_intensity[einstein_ring] * 0.9
    
    # Horizonte de eventos (negro absoluto)
    image[event_horizon] = [0, 0, 0]
    
    # Añadir brillo general (glow) alrededor del agujero negro
    glow = np.exp(-(R - black_hole_radius)**2 / 0.1) * (R > black_hole_radius)
    glow *= 0.3
    image[:, :, 0] += glow * 0.5
    image[:, :, 1] += glow * 0.3
    image[:, :, 2] += glow * 0.2
    
    # Normalizar imagen
    image = np.clip(image, 0, 1)
    
    return image, R, black_hole_radius


def add_background_stars(image, num_stars=500):
    """Añade estrellas de fondo para mayor realismo."""
    resolution = image.shape[0]
    
    # Crear campo de estrellas
    star_x = np.random.randint(0, resolution, num_stars)
    star_y = np.random.randint(0, resolution, num_stars)
    star_brightness = np.random.random(num_stars) * 0.8 + 0.2
    star_sizes = np.random.randint(1, 3, num_stars)
    
    for i in range(num_stars):
        size = star_sizes[i]
        x, y = star_x[i], star_y[i]
        
        # Evitar poner estrellas sobre el disco brillante
        center = resolution // 2
        dist = np.sqrt((x - center)**2 + (y - center)**2)
        if dist > 400 or dist < 150:  # Fuera del disco o muy cerca del horizonte
            brightness = star_brightness[i]
            image[max(0, y-size):min(resolution, y+size), 
                  max(0, x-size):min(resolution, x+size)] += brightness
            image = np.clip(image, 0, 1)
    
    return image


def create_interstellar_style_image():
    """Crea una imagen estilo Interstellar con múltiples componentes."""
    
    # Generar simulación principal
    image, R, bh_radius = create_black_hole_simulation(resolution=1200, black_hole_radius=150/1200*2)
    
    # Añadir estrellas de fondo
    image = add_background_stars(image, num_stars=800)
    
    # Aplicar tono cinematográfico
    # Realzar rojos y naranjas para el estilo Interstellar
    image[:, :, 0] *= 1.1  # Realzar rojo
    image[:, :, 1] *= 0.95  # Reducir ligeramente verde
    image[:, :, 2] *= 0.85  # Reducir azul
    
    image = np.clip(image, 0, 1)
    
    return image


def main():
    """Función principal para generar y mostrar la simulación."""
    
    print("=" * 60)
    print("SIMULACIÓN DE AGUJERO NEGRO - TIPO GARGANTUA (INTERSTELLAR)")
    print("=" * 60)
    print()
    print("Características de la simulación:")
    print("- Horizonte de eventos (región negra central)")
    print("- Disco de acreción con gradiente de temperatura")
    print("- Efecto de lente gravitacional (anillo de Einstein)")
    print("- Espiral de materia cayendo al agujero")
    print("- Campo estelar de fondo")
    print()
    
    # Generar la simulación
    image = create_interstellar_style_image()
    
    # Crear figura
    fig, ax = plt.subplots(1, 1, figsize=(12, 12), facecolor='black')
    
    # Mostrar imagen
    ax.imshow(image, origin='lower', extent=[-2, 2, -2, 2])
    
    # Configurar apariencia
    ax.set_facecolor('black')
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect('equal')
    
    # Títulos y etiquetas
    ax.set_title('GARGANTUA - Simulación de Agujero Negro\n(Estilo Interstellar)', 
                 color='white', fontsize=16, pad=20)
    ax.set_xlabel('Coordenada X (unidades arbitrarias)', color='white', fontsize=12)
    ax.set_ylabel('Coordenada Y (unidades arbitrarias)', color='white', fontsize=12)
    
    # Colorear ticks
    ax.tick_params(colors='white', labelsize=10)
    
    # Añadir leyenda informativa
    info_text = "Características:\n• Horizonte de Eventos\n• Disco de Acreción\n• Lente Gravitacional\n• Corrimiento al Rojo"
    plt.figtext(0.02, 0.02, info_text, color='white', fontsize=9, 
                bbox=dict(facecolor='black', alpha=0.7, edgecolor='gray'))
    
    plt.tight_layout()
    
    # Guardar imagen
    output_file = 'gargantua_black_hole.png'
    plt.savefig(output_file, dpi=150, facecolor='black', edgecolor='none')
    print(f"✓ Imagen guardada como: {output_file}")
    
    # Mostrar
    print("\nMostrando simulación...")
    plt.show()
    
    print("\n¡Simulación completada!")


if __name__ == "__main__":
    main()
