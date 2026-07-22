# Simulación 3D Interactiva de Agujero Negro - Gargantua (Interstellar)

## 🌌 Descripción

Esta simulación reproduce visualmente un agujero negro supermasivo similar a **Gargantua**, el agujero negro ficticio de la película *Interstellar* (2014). La simulación incorpora efectos de relatividad general para mostrar cómo la gravedad extrema curva el espacio-tiempo y distorsiona la luz de las estrellas y el disco de acreción.

La física implementada se basa en los cálculos realizados por el **Dr. Kip Thorne** (Premio Nobel de Física 2017), quien asesoró científicamente la película.

---

## ✨ Características Principales

### Efectos Físicos Implementados

1. **Lente Gravitacional Completa**
   - Los rayos de luz se curvan siguiendo la métrica de Schwarzschild
   - Las estrellas detrás del agujero negro aparecen distorsionadas
   - Formación del anillo de Einstein visible

2. **Horizonte de Eventos**
   - Región esférica negra central de la que nada puede escapar
   - Radio definido por el radio de Schwarzschild (Rs = 2GM/c²)

3. **Disco de Acreción Volumétrico**
   - Representación 3D del gas y polvo orbitando el agujero
   - Gradiente térmico realista:
     - **Interior**: Blanco-azul (~10⁷ K, más caliente)
     - **Medio**: Naranja intenso
     - **Exterior**: Rojo oscuro (~3000 K, más frío)
   - Espesor variable (más grueso en el interior)

4. **Anillo de Einstein**
   - Imagen distorsionada del disco de acreción visible sobre y bajo el horizonte
   - Resultado de la curvatura extrema de la luz

5. **Doppler Boosting (Efecto Relativista)**
   - Un lado del disco aparece más brillante
   - Causado por la rotación del disco a velocidades cercanas a la luz
   - El lado que se acerca al observador es más brillante (blue-shifted)
   - El lado que se aleja es más tenue (red-shifted)

6. **Campo Estelar de Fondo**
   - 2000 estrellas generadas proceduralmente
   - Cada estrella se distorsiona individualmente por la gravedad
   - Colores variados (blanco, amarillo, azul, rojo) según tipo espectral

7. **Textura Procedural Espiral**
   - Patrón de materia cayendo en espiral hacia el agujero
   - Generado matemáticamente sin necesidad de imágenes externas

---

## 🎮 Controles Interactivos

| Control | Acción |
|---------|--------|
| **Mouse (arrastrar)** | Rotar cámara libremente alrededor del agujero |
| **Rueda del mouse** | Zoom (acercar/alejar) |
| **W** | Avanzar hacia adelante |
| **S** | Retroceder |
| **A** | Moverse a la izquierda |
| **D** | Moverse a la derecha |
| **Q** | Moverse hacia arriba |
| **E** | Moverse hacia abajo |
| **R** | Reiniciar posición de la cámara |
| **ESC** | Salir de la simulación |

### Consejos de Visualización

- **Aleja la cámara** para ver el efecto completo de lente gravitacional
- **Rota lentamente** para observar cómo el anillo de Einstein se deforma
- **Acércate al horizonte** (con cuidado ¡no hay retorno!)
- **Posiciónate encima del disco** para ver la estructura espiral
- **Muevete lateralmente** para apreciar el Doppler boosting

---

## 📦 Requisitos

### Dependencias de Python

```bash
pip install numpy pygame PyOpenGL PyOpenGL_accelerate
```

### Paquetes necesarios:

- **Python 3.7+**: Lenguaje de programación
- **NumPy**: Cálculos numéricos y de matrices
- **Pygame**: Gestión de ventana y eventos
- **PyOpenGL**: Renderizado OpenGL 3D
- **PyOpenGL_accelerate**: Aceleración opcional de OpenGL

### Sistema Operativo

- **Linux**: Ubuntu, Debian, Fedora, etc. (con X11 o Wayland)
- **Windows**: 10/11 con drivers OpenGL actualizados
- **macOS**: Requiere instalación adicional de PyOpenGL

---

## 🚀 Instrucciones de Ejecución

### 1. Instalar dependencias

```bash
cd /workspace
pip install numpy pygame PyOpenGL PyOpenGL_accelerate
```

### 2. Ejecutar la simulación

```bash
python black_hole_3d_interactive.py
```

### 3. Explorar el agujero negro

Una vez abierta la ventana:
- Usa el mouse para rotar la vista
- Usa las teclas WASD + QE para moverte en 3D
- Observa cómo las estrellas se distorsionan cerca del horizonte
- Intenta ver el disco de acreción desde diferentes ángulos

---

## 🔬 Explicación Científica

### ¿Qué es un Agujero Negro?

Un agujero negro es una región del espacio-tiempo donde la gravedad es tan intensa que nada, ni siquiera la luz, puede escapar. Se forma cuando una estrella masiva colapsa bajo su propia gravedad.

### Componentes del Agujero Negro

1. **Singularidad**: Punto central de densidad infinita (no visible en la simulación)
2. **Horizonte de Eventos**: Límite teórico de no retorno
3. **Disco de Acreción**: Materia orbitando que se calienta por fricción
4. **Esfera de Fotones**: Órbita estable más cercana para la luz (1.5 × Rs)

### Métrica de Schwarzschild

La simulación usa la solución de Schwarzschild para agujeros negros estáticos:

```
ds² = -(1 - Rs/r)c²dt² + (1 - Rs/r)⁻¹dr² + r²(dθ² + sin²θ dφ²)
```

Donde:
- **Rs** = Radio de Schwarzschild = 2GM/c²
- **G** = Constante gravitacional
- **M** = Masa del agujero negro
- **c** = Velocidad de la luz

### Lente Gravitacional

Según la Relatividad General de Einstein, la masa curva el espacio-tiempo. La luz sigue esta curvatura, creando efectos como:

- **Deflexión de luz**: Ángulo ≈ 4GM/(c²b), donde b es el parámetro de impacto
- **Anillo de Einstein**: Cuando la fuente, lente y observador están alineados
- **Multiplicación de imágenes**: Una estrella puede aparecer múltiples veces

### Corrimiento al Rojo Gravitacional

La luz que escapa del campo gravitatorio pierde energía:

```
λ_observed = λ_emitted / √(1 - Rs/r)
```

Esto hace que la luz se vuelva más roja cerca del horizonte.

---

## 🎨 Parámetros Ajustables

En el código puedes modificar:

```python
# Masa del agujero negro (afecta el tamaño del horizonte)
BLACK_HOLE_MASS = 1.0

# Radio del horizonte de eventos
EVENT_HORIZON_RADIUS = 1.0

# Tamaño del disco de acreción
DISC_INNER_RADIUS = 1.5  # Mínimo: 1.0 (horizonte)
DISC_OUTER_RADIUS = 8.0

# Grosor del disco
DISC_THICKNESS = 0.3

# Número de estrellas de fondo
NUM_STARS = 2000

# Intensidad del efecto de lente gravitacional
LENSING_STRENGTH = 1.0

# Brillo del Doppler boosting
DOPPLER_FACTOR = 0.5
```

---

## ⚠️ Notas Importantes

1. **Requiere interfaz gráfica**: La simulación necesita una ventana GUI (X11, Wayland, Windows, macOS)
2. **Rendimiento**: En hardware limitado, reduce `NUM_STARS` o la resolución de la ventana
3. **Precisión científica**: Es una visualización educativa, no una simulación astrofísica completa
4. **Agujero negro estático**: No incluye rotación (Kerr metric) por simplicidad

---

## 📚 Créditos y Referencias

### Película
- **Interstellar** (2014) - Director: Christopher Nolan
- Asesor científico: Dr. Kip Thorne

### Publicaciones Científicas
- Thorne, K. S. (2014). *The Science of Interstellar*. W. W. Norton & Company.
- James, O., von Tunzelmann, E., Franklin, A., & Thorne, K. (2015). "Gravitational lensing by spinning black holes in astrophysics, and in the movie Interstellar". *Classical and Quantum Gravity*, 32(6), 065001.

### Software
- Desarrollado con Python, NumPy, Pygame y PyOpenGL
- Algoritmos de ray tracing inspirados en visualizaciones de NASA/ESA

---

## 🌟 Curiosidades

- El agujero negro Gargantua en Interstellar gira al **99.8%** de la velocidad máxima posible
- Para un agujero negro de 100 millones de masas solares, el horizonte tendría ~300 millones de km de diámetro
- Si cayeras en un agujero negro supermasivo, sobrevivirías cruzando el horizonte (las fuerzas de marea son débiles)
- Desde fuera, te verían congelado en el horizonte debido a la dilatación temporal

---

## 📞 Soporte

Si encuentras errores o tienes sugerencias, revisa:
1. Que todas las dependencias estén instaladas
2. Que tu sistema tenga aceleración OpenGL habilitada
3. Los logs de error en la terminal

¡Disfruta explorando uno de los fenómenos más extremos del universo! 🕳️✨

---

**Autor**: Simulación generada para fines educativos  
**Licencia**: Código abierto para uso educativo y de investigación  
**Versión**: 1.0 - Enero 2025
