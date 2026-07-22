# Simulación 3D Interactiva de Agujero Negro - Gargantua (Interstellar)

## Descripción
Simulación física realista de un agujero negro supermasivo estilo Gargantua de la película Interstellar. Implementa **ray tracing con curvatura espaciotemporal** basada en la métrica de Schwarzschild para mostrar efectos de lente gravitacional.

## Características Físicas
- ✅ **Horizonte de eventos**: Esfera negra central de la que nada puede escapar
- ✅ **Disco de acreción**: Materia orbitando con gradiente térmico (blanco → naranja → rojo)
- ✅ **Lente gravitacional**: Curvatura de la luz de estrellas distantes
- ✅ **Anillo de Einstein**: Imagen distorsionada del disco detrás del agujero
- ✅ **Corrimiento al rojo gravitacional**: La luz pierde energía cerca del horizonte
- ✅ **Doppler boosting**: El lado que se acerca aparece más brillante
- ✅ **Campo estelar dinámico**: 2000 estrellas con distorsión por gravedad

## Requisitos
```bash
pip install pygame numpy
```

## Ejecución
```bash
python black_hole_3d_interactive.py
```

## Controles

### Cámara
| Control | Acción |
|---------|--------|
| **Mouse (arrastrar)** | Rotar cámara alrededor del agujero |
| **Rueda del mouse** | Zoom (acercar/alejar) |
| **W / S** | Mover adelante / atrás |
| **A / D** | Mover izquierda / derecha |
| **Q / E** | Mover arriba / abajo |
| **R** | Reiniciar posición de cámara |
| **ESC** | Salir de la simulación |

## Parámetros Físicos (ajustables en el código)

```python
SCHWARZSCHILD_RADIUS = 1.0      # Radio del horizonte de eventos
DISC_INNER_RADIUS = 2.6         # Borde interno del disco (en radios de Schwarzschild)
DISC_OUTER_RADIUS = 8.0         # Borde externo del disco
DISC_THICKNESS = 0.15           # Grosor del disco
```

## Explicación Científica

### ¿Por qué se ve así?
En **Interstellar**, el físico Kip Thorne calculó cómo se vería un agujero negro real usando ecuaciones de relatividad general. Esta simulación replica esos efectos:

1. **Curvatura de luz**: Los rayos de luz no viajan en línea recta, siguen geodésicas curvas cerca del agujero negro
2. **Imagen múltiple**: Puedes ver el disco de acreción tanto por encima como por debajo porque la luz se curva
3. **Asimetría Doppler**: Un lado del disco es más brillante porque la materia se mueve hacia ti a velocidades relativistas
4. **Sombra negra**: El horizonte de eventos absorbe toda la luz, creando una "sombra" característica

### Algoritmo de Renderizado
- **Raymarching**: Se trazan rayos desde cada píxel de la pantalla
- **Integración de geodésicas**: Cada rayo se curva según la gravedad del agujero
- **Compositing volumétrico**: El disco de acreción se renderiza como medio participativo
- **Muestreo procedural**: Texturas generadas matemáticamente sin imágenes externas

## Notas de Rendimiento
- Resolución: 1200x900 píxeles
- FPS objetivo: 60 (depende de tu hardware)
- Optimización: Usa NumPy para cálculos vectorizados
- En sistemas lentos, reduce WIDTH y HEIGHT en las constantes

## Créditos
Inspirado en la visualización científica de **Interstellar** (2014), desarrollada por **Double Negative VFX** con asesoramiento del físico **Kip Thorne** (Premio Nobel 2017).
