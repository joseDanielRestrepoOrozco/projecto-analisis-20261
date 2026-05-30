# Plan de Trabajo — Extensión de Bipartición a $k$-Partición ($k \leq 5$)

## Objetivo General

Extender el algoritmo geométrico actual de **bipartición óptima** hacia una solución general de **$k$-partición** para:

[
k \in {2,3,4,5}
]

sin romper:

- la estructura geométrica del hipercubo,
- la lógica tensorial,
- la tabla de costos (T),
- ni la metodología ya implementada.

La meta es reutilizar al máximo el código existente.

---

# 1. Diagnóstico Inicial del Código Base

## Objetivo

Identificar exactamente qué partes del código ya son reutilizables.

---

## Tareas

### 1.1 Identificar módulos existentes

Debes ubicar:

- construcción TPM,
- marginalización,
- representación estado-nodo,
- generación del hipercubo,
- cálculo de distancia Hamming,
- BFS modificado,
- construcción de tabla (T),
- evaluación de bipartición,
- cálculo de discrepancia tensorial,
- reconstrucción tensorial.

---

### 1.2 Separar componentes “genéricos” de “bipartición”

Idealmente debes terminar con:

```text
/core
    hypercube.py
    tensor.py
    costs.py
    marginalization.py

/bipartition
    evaluator.py
    search.py

/kpartition
    dp.py
    evaluator.py
```

---

### 1.3 Verificar si la tabla T es independiente de la bipartición

Esto es CRÍTICO.

La tabla:

[
T[i,j]
]

debe depender SOLO del sistema y NO de una partición específica.

Si esto se cumple:

✅ excelente reutilización
✅ DP viable
✅ memoización eficiente

---

# 2. Formalizar Matemáticamente la k-Partición

## Objetivo

Definir correctamente el problema antes de programar.

---

# 2.1 Definición formal

Actualmente tienes:

[
V = S_1 \cup S_2
]

Extender a:

[
V = S_1 \cup S_2 \cup \dots \cup S_k
]

tal que:

[
S_i \cap S_j = \emptyset
]

---

# 2.2 Definir la nueva función objetivo

NO reutilices directamente la de bipartición.

Debes definir:

[
\delta_k(V,{S_1,\dots,S_k})
]

---

## Recomendación práctica

Inicialmente usa:

[
\delta_k =
\sum_i Cost(S_i)

- \lambda \sum\_{i<j} Interaction(S_i,S_j)
  ]

donde:

- `Cost(S_i)` usa información derivada de (T),
- `Interaction` mide acoplamiento residual,
- `λ` regula penalización.

---

# 2.3 Mantener compatibilidad con bipartición

Debe cumplirse:

[
\delta_2 \equiv \delta_{bipartición}
]

Esto garantiza coherencia teórica.

---

# 3. Diseño de la Representación Interna

## Objetivo

Representar particiones de forma eficiente.

---

# 3.1 Usar bitmasks

Mantén:

```python
mask = 0b101101
```

porque:

- ya coincide con el hipercubo,
- facilita operaciones rápidas,
- simplifica memoización.

---

# 3.2 Representar una k-partición

Ejemplo:

```python
[
    0b000011,
    0b001100,
    0b110000
]
```

---

# 3.3 Utilidades necesarias

Crear funciones:

```python
count_bits(mask)

intersects(a,b)

union(parts)

generate_submasks(mask)

canonical_partition(parts)
```

---

# 4. Construcción de Costos por Subconjunto

## Objetivo

Precomputar todos los costos necesarios.

---

# 4.1 Crear tabla de subconjuntos

Necesitarás:

```python
subset_cost[mask]
```

---

# 4.2 Qué debe almacenar

Idealmente:

```python
subset_cost[mask] = {
    "internal_cost": ...,
    "tensor_discrepancy": ...,
    "projection_cost": ...,
    "transition_energy": ...
}
```

---

# 4.3 Precomputación

Complejidad:

[
O(2^n)
]

Para:

[
n \le 20
]

es manejable si optimizas.

---

# 5. Primera Implementación: Fuerza Bruta Controlada

## Objetivo

Tener una referencia correcta antes de DP.

---

# 5.1 Implementar generador de k-particiones

Solo para:

```text
n <= 10
```

---

# 5.2 Validar coherencia

Comparar:

- bipartición antigua,
- nueva implementación con (k=2).

Los resultados deben coincidir.

---

# 5.3 Crear suite de pruebas

Casos:

- sistemas triviales,
- sistemas simétricos,
- sistemas desacoplados,
- sistemas totalmente conectados.

---

# 6. Implementar Programación Dinámica

## Objetivo

Reducir explosión combinatoria.

---

# 6.1 Estado DP

Usa:

[
DP[k][mask]
]

donde:

- `mask` = variables aún disponibles,
- `k` = número de partes restantes.

---

# 6.2 Recurrencia

Primera versión:

[
DP[k][mask]
===========

\min\_{sub \subset mask}
{
Cost(sub)

- DP[k-1][mask \setminus sub]
  }
  ]

  ***

# 6.3 Evitar duplicados

MUY importante.

La misma partición aparece muchas veces:

```text
[A][B][C]
[B][A][C]
[C][B][A]
```

Debes imponer:

```python
sub > first_element
```

o usar forma canónica.

---

# 6.4 Memoización

Guardar:

```python
memo[(k, mask)]
```

---

# 6.5 Reconstrucción de solución

Guardar decisiones:

```python
parent[(k,mask)] = best_submask
```

---

# 7. Integración con la Geometría del Hipercubo

## Objetivo

No perder la esencia del proyecto.

---

# 7.1 Incorporar distancias Hamming

Puedes definir:

[
Cost(sub)
=========

\sum\_{i,j \in sub} T[i,j]
]

ponderado por:

[
d_H(i,j)
]

---

# 7.2 Explorar proyecciones geométricas

Inspirado en el PDF:

- proyección marginal,
- cohesión interna,
- separación topológica.

---

# 7.3 Detectar simetrías

Usar:

- permutaciones,
- automorfismos,
- equivalencias topológicas.

Esto puede reducir muchísimo el espacio.

---

# 8. Optimización

## Objetivo

Escalar hasta 15-20 variables.

---

# 8.1 Podas

Agregar bounds:

```python
if current_cost > best:
    prune()
```

---

# 8.2 Cache multinivel

Separar:

```python
subset_cost
interaction_cost
projection_cost
```

---

# 8.3 Paralelización

Muy recomendable en:

- construcción de (T),
- evaluación de subconjuntos,
- exploración DP.

---

# 9. Validación Experimental

## Objetivo

Demostrar que funciona.

---

# 9.1 Comparaciones

Comparar contra:

- bipartición original,
- fuerza bruta,
- random partitions.

---

# 9.2 Métricas

Registrar:

- tiempo,
- memoria,
- número de estados explorados,
- calidad de partición.

---

# 9.3 Visualización

MUY recomendable.

Visualizar:

- hipercubo,
- clusters,
- cortes,
- proyecciones.

---

# 10. Roadmap Recomendado

# Fase 1 — Refactor

✅ modularizar código
✅ aislar tabla T
✅ aislar función costo

---

# Fase 2 — Generalización

✅ representar k-particiones
✅ implementar fuerza bruta
✅ validar con k=2

---

# Fase 3 — DP

✅ memoización
✅ reconstrucción
✅ canonicalización

---

# Fase 4 — Optimización Geométrica

✅ simetrías
✅ podas topológicas
✅ reducción dimensional

---

# Fase 5 — Escalamiento

✅ paralelización
✅ profiling
✅ benchmarks

---

# Recomendación Arquitectónica Final

Tu mejor estrategia NO es:

```text
“hacer DP encima de biparticiones”
```

Tu mejor estrategia es:

```text
“convertir la bipartición actual en un evaluador genérico de subconjuntos”
```

y luego construir encima:

- fuerza bruta,
- DP,
- heurísticas,
- branch and bound,
- clustering topológico.

Eso te dará una arquitectura muchísimo más sólida y extensible.
