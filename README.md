# EcoPlastic-Tools
Blender add-on to calculate the carbon footprint of an object made of plastic and assists in the selection of plastic.

_Guía de uso y referencia científica para el addon en Blender 3.x_

## Compatibilidad y Requisitos
- **Blender**: Versión 3.x (3.3 o superior)  
- **Python**: 3.x (incluido con Blender)  
- **Dependencias**: Ninguna externa; solo APIs internas de Blender  
- **Sistemas operativos**: Windows, macOS y Linux  

---

## 1. Instalación

1. Descarga el archivo `plastico.py`.  
2. En Blender, ve a **Editar → Preferencias → Add-ons → Instalar...**.  
3. Selecciona `plastico.py` y haz clic en **Instalar add-on**.  
4. Activa el addon marcando su casilla en la lista.  

---

## 2. Interfaz de Usuario

### 2.1 Panel «Plástico» (Properties → Object)
- **Selector de Plástico**: enum con todas las variantes.  
- **Símbolo**: abreviatura CEN.  
- **Densidad**: en g/cm³.  
- **CO₂**: huella por kg de material (kg CO₂/kg).  
- **Fin de vida**: destino (vertedero, reciclaje, compost).  
- **Biodegradabilidad**: tiempo estimado.  
- **Usos**: ejemplos profesionales.  

### 2.2 Panel «Huella de Carbono» (3D Viewport Sidebar → Plástico)
- **Proceso**: Extrusión, Inyección, FDM.  
- **Transporte**: tramos (camión, tren, barco, avión) con distancia (km).  
- **Consumo eléctrico** (kWh): energía usada en el ciclo de vida (LED, pantallas, climatización, etc.).  
- **Fin de vida**: vertedero, reciclaje, incineración.  
- **Unidades**: número de piezas.  
- **Botón Calcular**: muestra detalle por fase y total.  

**Procesos disponibles**:

| Plástico      | Extrusión | Inyección | FDM   | Moldeo artesanal |
|---------------|:---------:|:---------:|:-----:|:----------------:|
| PET           | Sí        | Sí        | No    | No               |
| r-PET         | Sí        | Sí        | No    | No               |
| PET-G         | Sí        | Sí        | Sí    | No               |
| HDPE          | Sí        | Sí        | No    | No               |
| LDPE          | Sí        | Sí        | No    | No               |
| EVA           | Sí        | No        | No    | No               |
| PP            | Sí        | Sí        | Sí    | No               |
| r-PP          | Sí        | Sí        | No    | No               |
| PVC rig.      | Sí        | Sí        | No    | No               |
| PVC flex      | Sí        | Sí        | No    | No               |
| PS            | Sí        | Sí        | No    | No               |
| ABS           | Sí        | Sí        | Sí    | No               |
| PMMA          | Sí        | Sí        | No    | No               |
| PC            | Sí        | Sí        | Sí    | No               |
| PCL           | No        | No        | No    | Sí               |
| TPS           | Sí        | Sí        | No    | No               |
| Starch-blend  | Sí        | No        | No    | No               |
| Cellophane    | No        | No        | No    | Sí               |
| CA            | No        | No        | No    | Sí               |
| PGA           | No        | No        | No    | Sí               |

### 2.3 Panel «Biodegradabilidad»
- Muestra el tiempo estimado de degradación en días (convierte meses y años a días).

### 2.4 Panel «Recomendación de Plástico»
- **Necesidad**: Rígido, Flexible o cualquiera.  
- **Top N**: número de resultados.  
- **Cuestionario AHP**: 15 comparaciones pareadas.  
- **Generar recomendaciones**: ordena según criterios.

#### 2.4.1 Preguntas del Cuestionario AHP  
En esta fase, el diseñador/interiorista valora cada par de criterios así:

1. **Biodegradabilidad vs. Huella de Carbono**  
   - ¿Qué es más importante: que el material se degrade rápido al desmontarlo o que haya emitido poca CO₂ durante su uso?  
   Piensa si prefieres compostar sin residuos o minimizar emisiones desde la fabricación.

2. **Biodegradabilidad vs. Rigidez**  
   - ¿Más relevante: que desaparezca tras el pop-up o que aguante carga intensa?  
   Contrasta un mueble desechable frente a uno robusto.

3. **Biodegradabilidad vs. Flexibilidad**  
   - ¿Prefieres cortinas compostables o paneles que plieguen sin romperse?  
   Decide entre fin de vida ecológico o plegabilidad intensa.

4. **Biodegradabilidad vs. Procesado**  
   - ¿Máxima degradación o mínima energía de producción?  
   Piensa en rapidez de taller vs. limpieza posterior.

5. **Biodegradabilidad vs. Fin de Vida**  
   - ¿Compostaje doméstico rápido o reciclaje industrial?  
   Elige compostaje casero o rutas urbanas de reciclaje.

6. **Huella de Carbono vs. Rigidez**  
   - ¿Menos CO₂ o suelo muy resistente?  
   Compara ligereza ecológica vs. durabilidad extrema.

7. **Huella de Carbono vs. Flexibilidad**  
   - ¿Baja huella o gran doblado?  
   Elige emisiones reducidas vs. geometrías complejas.

8. **Huella de Carbono vs. Procesado**  
   - ¿Poca CO₂ o moldeado ágil?  
   Decide entre ahorro de emisiones vs. tiempo de taller.

9. **Huella de Carbono vs. Fin de Vida**  
   - ¿Huella baja o fácil reciclaje?  
   Contrasta emisiones totales vs. circularidad.

10. **Rigidez vs. Flexibilidad**  
    - ¿Estructura firme o plegable?  
    Piensa en estanterías fijas vs. paneles guardables.

11. **Rigidez vs. Procesado**  
    - ¿Fuerza mecánica o producción express?  
    Decide entre robustez y plazos cortos.

12. **Rigidez vs. Fin de Vida**  
    - ¿Durabilidad o reciclaje post-uso?  
    Balancea vida útil y economía circular.

13. **Flexibilidad vs. Procesado**  
    - ¿Doblado extremo o bajo consumo en fabricación?  
    Compara maleabilidad vs. eficiencia de recursos.

14. **Flexibilidad vs. Fin de Vida**  
    - ¿Adaptabilidad o compostabilidad/reciclaje?  
    Valora formas dinámicas vs. fin de vida limpio.

15. **Procesado vs. Fin de Vida**  
    - ¿Montaje rápido o economía circular?  
    Prioriza despliegue exprés vs. cierre del ciclo.

---

## 3. Detalle Científico y Fórmulas

### 3.1 Datos de Plásticos
| Plástico       | Símbolo | Densidad (g/cm³) | CO₂ material (kg/kg) | Moldeo                         | Destino final   | Biodegradabilidad  | Usos comunes                                      |
|---------------|---------|------------------:|---------------------:|-------------------------------|-----------------|--------------------|---------------------------------------------------|
| PET           | PET     | 1.38              | 3.0                  | Extrusión, Inyección          | Vertedero       | No • >450 años      | Paneles acústicos, tejidos back-lit               |
| r-PET         | PET⟳    | 1.35              | 0.8                  | Extrusión, Inyección          | Reciclaje       | Reciclable          | Láminas recicladas, impresión UV                  |
| PET-G         | —       | 1.27              | 3.0                  | Extrusión, Inyección, FDM     | Vertedero       | No • >400 años      | Placas termoformables para stands                 |
| HDPE          | 2       | 0.95              | 1.9                  | Extrusión, Inyección          | Vertedero       | No • >500 años      | Tarimas modulares, mobiliario reciclado           |
| LDPE          | 4       | 0.92              | 1.85                 | Extrusión, Inyección          | Vertedero       | No • >500 años      | Films protectores, envolventes tensadas           |
| EVA           | —       | 0.94              | 2.2                  | Extrusión                     | Vertedero       | No • >300 años      | Suelos blandos, soft-graphics                     |
| PP            | 5       | 0.90              | 1.65                 | Extrusión, Inyección, FDM     | Vertedero       | No • >400 años      | Panel alveolar, impresión 3D                      |
| r-PP          | 5⟳      | 0.89              | 0.7                  | Extrusión, Inyección          | Reciclaje       | Reciclable          | Carcasas de luminaria, módulos desmontables       |
| PVC rig.      | 3       | 1.42              | 3.25                 | Extrusión, Inyección          | Vertedero       | No • >1000 años     | Paneles espumados Forex®, perfilería temporal     |
| PVC flex      | 3       | 1.32              | 3.45                 | Extrusión, Inyección          | Vertedero       | No • >1000 años     | Lonas back-lit, suelos vinílicos clic            |
| PS            | 6       | 1.05              | 2.85                 | Extrusión, Inyección          | Vertedero       | No • >500 años      | Maquetas, núcleos XPS, rótulos corpóreos          |
| ABS           | 7       | 1.05              | 4.0                  | Extrusión, Inyección, FDM     | Vertedero       | No • >500 años      | Piezas impresas FDM, carcasas de expo             |
| PMMA          | —       | 1.18              | 4.5                  | Extrusión, Inyección          | Vertedero       | No • >400 años      | Paneles LED edge-lit, letras traslúcidas          |
| PC            | 7       | 1.20              | 5.0                  | Extrusión, Inyección, FDM     | Vertedero       | No • >1000 años     | Visores transparentes, cubiertas ligeras          |
| PCL           | —       | 1.14              | 2.25                 | Modelado artesanal            | Compost dom.    | Sí • <12 meses      | Moldeables DIY, adhesivos low-temp                |
| TPS           | —       | 1.20              | 1.6                  | Extrusión, Inyección          | Compost dom.    | Sí • 1-6 meses      | Vajilla desechable, recubrimientos hidrosolubles  |
| Starch-blend  | —       | 1.20              | 1.85                 | Extrusión                     | Compost dom.    | Sí • 3-6 meses      | Lonas compostables, cubre-alfombras               |
| Cellophane    | —       | 1.45              | 2.0                  | Modelado artesanal            | Suelo           | Sí • 10-30 días     | Ventanas de packaging, láminas envolventes       |
| CA            | —       | 1.30              | 2.25                 | Modelado artesanal            | Compost dom.    | Sí • 2-4 meses      | Láminas semitransparentes para back-light         |
| PGA           | —       | 1.50              | 2.8                  | Modelado artesanal            | Compost dom.    | Sí • <60 días       | Hilos de fijación temporal, piezas solubles       |

### 3.2 Cálculo de Masa
- **m (kg)** = densidad (kg/m³) × volumen (m³) × unidades  
  1. Convierte densidad de g/cm³ a kg/m³ (× 1 000).  
  2. Calcula volumen en m³ (X×Y×Z en metros).  
  3. Multiplica para masa total.

### 3.3 Cálculo de Huella de Carbono
Variables principales:
- **m**: masa total (kg)  
- **fₘ**: emisiones por kg de material (kg CO₂/kg)  
- **fₚ**: emisiones en el proceso (kg CO₂/kg):  
  - Extrusión: 0.20  
  - Inyección: 0.25  
  - FDM: 0.50  
- **dᵢ**: distancia (km)  
- **tᵢ**: factor transporte (kg CO₂/t·km):  
  - Camión: 0.090  
  - Tren: 0.040  
  - Barco: 0.010  
  - Avión: 0.580  
- **E**: consumo eléctrico (kWh)  
- **fₑ**: emisiones eléctricas (kg CO₂/kWh) ≈ 0.20  
- **f_fin**: fin de vida (kg CO₂/kg):  
  - Vertedero: 0.00  
  - Reciclaje: –0.30  
  - Incineración: 0.60  

Fórmulas:
1. Material: `CO₂_mat = m × fₘ`  
2. Procesado: `CO₂_proc = m × fₚ`  
3. Transporte: `CO₂_trans = Σ((m/1000) × dᵢ × tᵢ)`  
4. Uso eléctrico: `CO₂_use = E × fₑ`  
5. Fin de vida: `CO₂_end = m × f_fin`  
6. Total:  
   `CO₂_total = CO₂_mat + CO₂_proc + CO₂_trans + CO₂_use + CO₂_end`

### 3.4 Biodegradabilidad
Convierte días, meses y años a días para comparar tiempos de degradación.

### 3.5 Recomendador por AHP
1. Define 6 criterios: Biodegradación, CO₂, Rigidez, Flexibilidad, Procesado, Fin de vida.  
2. Realiza 15 comparaciones pareadas con escala de 1 a 9.  
3. Construye matriz 6×6 y calcula autovector principal.  
4. Normaliza pesos (suma = 1).  
5. Puntúa cada plástico (valores normalizados × pesos).  
6. Ordena y muestra Top N.

---

## 4. Ejemplo de Uso

1. Selecciona **PET** en el panel Plástico.  
2. Añade “Camión 200 km” en Huella de Carbono.  
3. Define Extrusión, 5 kWh, Reciclaje, 10 unidades.  
4. Haz clic en **Calcular huella**.  
5. Revisa degradación en días.  
6. Ejecuta Cuestionario AHP y obtén recomendaciones.

---

## 5. Road Map
- Incorporar huella hídrica y energético-social.

## Licencia y Autoría
- **Autor**: Israel Navarro Fernández, profesor de Materiales y Tecnología: Diseño en la Escuela de Arte y Superior de Diseño de Sevilla.  
- **Licencia**: Libre educativa.  
- **Contacto**: threads @isra.skylight  
