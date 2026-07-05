# Cendra Financial Insights

> Inteligencia financiera para pequeños negocios.

Cendra es una aplicación de analítica financiera que transforma archivos Excel y CSV en indicadores, señales de riesgo, análisis de concentración y métricas de salud financiera.

El objetivo del proyecto es reducir la dependencia de reportes manuales y convertir datos transaccionales en información clara para apoyar la toma de decisiones.

---

## Descripción general

Muchos pequeños negocios administran ventas y gastos mediante hojas de cálculo, pero convertir esos registros en información útil suele requerir consolidación manual, fórmulas y revisión constante.

Cendra propone un flujo simple:

```text
Excel / CSV
    ↓
Carga de datos
    ↓
Normalización
    ↓
Validación
    ↓
Filtros dinámicos
    ↓
Analítica financiera
    ↓
Cendra Score
    ↓
Riesgos y anomalías
    ↓
Visualización
    ↓
Reporte ejecutivo
```

La aplicación permite explorar el comportamiento financiero del negocio sin modificar manualmente fórmulas ni construir dashboards desde cero.

---

## Características principales

### Analítica financiera

Cendra calcula automáticamente:

- Ventas
- Gastos
- Utilidad
- Margen
- Variación frente al período anterior
- Evolución temporal del negocio

### Analítica comercial

Incluye indicadores como:

- Ticket promedio
- Número de ventas
- Producto líder
- Cliente principal
- Ventas por producto
- Distribución de gastos por categoría

### Cendra Score

Cendra incorpora un indicador heurístico de salud financiera en una escala de `0 a 100`.

El Score considera las dimensiones disponibles:

| Dimensión | Objetivo |
|---|---|
| Rentabilidad | Evaluar el desempeño del margen |
| Crecimiento | Medir la evolución de ventas |
| Control de gastos | Analizar la variación de gastos |
| Estabilidad | Evaluar la variabilidad de ventas |

Cuando una dimensión no dispone de información suficiente, se excluye del cálculo y los pesos disponibles se normalizan.

Esto evita interpretar la ausencia de histórico como un resultado financiero neutral.

> El Cendra Score es un indicador heurístico de apoyo y no constituye asesoría financiera.

### Riesgo de concentración

Cendra analiza la dependencia del negocio respecto a:

- Clientes principales
- Productos principales
- Participación relativa
- Concentración mediante HHI

El objetivo es identificar escenarios donde una parte significativa de los ingresos depende de pocos clientes o productos.

### Detección de anomalías

La aplicación identifica transacciones estadísticamente inusuales dentro del período analizado.

La detección se realiza separando tipos de operación para evitar comparar directamente distribuciones financieras con comportamientos diferentes.

Ejemplos:

- Ventas extraordinariamente altas
- Gastos fuera del patrón
- Operaciones con desviaciones significativas

### Señales automáticas

Cendra genera señales interpretables a partir de cambios relevantes en los indicadores.

Ejemplos:

```text
Las ventas aumentaron frente al período anterior.
```

```text
Los gastos crecieron por encima del ritmo de ventas.
```

```text
Existe una concentración elevada en el cliente principal.
```

### Reporte ejecutivo

El usuario puede descargar un archivo Excel con:

- Indicadores financieros
- Indicadores comerciales
- Cendra Score
- Cobertura del análisis
- Riesgos de concentración
- Señales detectadas
- Transacciones filtradas

El reporte refleja el período y los filtros seleccionados en la aplicación.

---

## Capturas de pantalla

> Añadir capturas después del despliegue público.

### Vista principal

```text
docs/screenshots/dashboard.png
```

### Cendra Score

```text
docs/screenshots/cendra-score.png
```

### Riesgos y anomalías

```text
docs/screenshots/risk-analysis.png
```

---

## Arquitectura

El proyecto sigue una separación modular entre lógica de negocio, componentes visuales y servicios.

```text
Cendra/
│
├── app.py
│
├── components/
│   ├── __init__.py
│   ├── anomalies.py
│   ├── charts.py
│   ├── export.py
│   ├── filters.py
│   ├── kpis.py
│   └── layout.py
│
├── core/
│   ├── __init__.py
│   ├── analytics.py
│   ├── anomalies.py
│   ├── insights.py
│   ├── loader.py
│   ├── risk.py
│   ├── score.py
│   ├── transformer.py
│   └── validator.py
│
├── services/
│   ├── __init__.py
│   └── report_service.py
│
├── data/
│   └── demo.xlsx
│
├── .gitignore
├── requirements.txt
└── README.md
```

### Responsabilidades por capa

#### `core/`

Contiene la lógica de negocio y procesamiento:

```text
analytics.py
→ KPIs y agregaciones financieras

anomalies.py
→ detección de operaciones inusuales

insights.py
→ generación de señales

loader.py
→ carga de Excel y CSV

risk.py
→ concentración y métricas de riesgo

score.py
→ cálculo del Cendra Score

transformer.py
→ normalización de datos

validator.py
→ reglas de calidad y validación
```

#### `components/`

Contiene la capa de presentación:

```text
anomalies.py
→ visualización de anomalías

charts.py
→ gráficos financieros

export.py
→ interfaz de descarga

filters.py
→ filtros interactivos

kpis.py
→ tarjetas de indicadores

layout.py
→ estilos y estructura visual
```

#### `services/`

Contiene servicios de salida e integración:

```text
report_service.py
→ generación del reporte ejecutivo Excel
```

#### `app.py`

Actúa como orquestador principal:

```text
Carga
  ↓
Transformación
  ↓
Validación
  ↓
Filtrado
  ↓
Analítica
  ↓
Score
  ↓
Riesgos
  ↓
Anomalías
  ↓
Visualización
  ↓
Exportación
```

---

## Stack tecnológico

| Tecnología | Uso |
|---|---|
| Python | Lenguaje principal |
| Streamlit | Aplicación web |
| Pandas | Procesamiento y análisis |
| Plotly | Visualización interactiva |
| OpenPyXL | Generación de reportes Excel |

---

## Formato de datos

Cendra espera archivos `.xlsx` o `.csv`.

### Columnas requeridas

| Columna | Tipo esperado | Descripción |
|---|---|---|
| `fecha` | Fecha | Fecha de la operación |
| `tipo` | Texto | `Venta` o `Gasto` |
| `categoria` | Texto | Categoría de la operación |
| `producto` | Texto | Producto o concepto |
| `cliente` | Texto | Cliente o contraparte |
| `cantidad` | Numérico | Cantidad asociada |
| `monto` | Numérico | Importe de la operación |

### Ejemplo

| fecha | tipo | categoria | producto | cliente | cantidad | monto |
|---|---|---|---|---|---:|---:|
| 2025-01-05 | Venta | Tecnología | Laptop | Empresa Andina SAC | 2 | 5600.00 |
| 2025-01-07 | Gasto | Marketing | Publicidad digital | Meta Ads | 1 | 900.00 |
| 2025-01-10 | Venta | Accesorios | Mouse | Comercial Lima SRL | 5 | 600.00 |

---

## Validación y calidad de datos

Antes de ejecutar los análisis, Cendra valida la información recibida.

### Errores bloqueantes

La aplicación detiene el procesamiento ante problemas como:

- Columnas obligatorias ausentes
- Fechas inválidas
- Montos inválidos
- Montos negativos
- Cantidades inválidas
- Tipos de transacción desconocidos

### Advertencias

Cendra permite continuar, pero informa situaciones como:

- Filas duplicadas
- Categorías vacías
- Productos vacíos
- Clientes vacíos

Esta separación evita ejecutar indicadores sobre datos que no cumplen condiciones mínimas de calidad.

---

## Instalación local

### 1. Clonar el repositorio

```bash
git clone URL_DEL_REPOSITORIO
cd cendra-financial-insights
```

### 2. Crear entorno virtual

```bash
python -m venv venv
```

### 3. Activar el entorno

#### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

#### Windows CMD

```cmd
venv\Scripts\activate.bat
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación estará disponible localmente en:

```text
http://localhost:8501
```

---

## Dataset de demostración

El proyecto puede incluir un dataset sintético para demostrar las capacidades de Cendra.

El conjunto de prueba contiene:

- 12 meses de operaciones
- Ventas y gastos
- Múltiples clientes
- Múltiples productos
- Estacionalidad
- Concentración comercial
- Gastos recurrentes
- Operaciones extraordinarias

> Los datos de demostración son completamente sintéticos y no representan empresas ni operaciones reales.

---

## Metodología del Cendra Score

La versión `v0.1` utiliza cuatro dimensiones:

```text
Rentabilidad      35%
Crecimiento       25%
Control de gastos 20%
Estabilidad       20%
```

Si una dimensión no puede calcularse por falta de información:

```text
Dimensión no disponible
        ↓
Se excluye del cálculo
        ↓
Se recalcula el peso disponible
        ↓
Se informa la cobertura
```

Ejemplo:

```text
Rentabilidad       Disponible
Crecimiento        No disponible
Control de gastos  No disponible
Estabilidad        Disponible

Cobertura: 50%
```

Esto permite diferenciar entre:

```text
Resultado financiero neutral
```

y:

```text
Ausencia de información suficiente
```

---

## Seguridad y privacidad

La versión actual procesa los archivos durante la sesión de la aplicación.

Para información financiera sensible se recomienda:

- No utilizar datasets reales en despliegues públicos de demostración
- Evitar incluir credenciales en el repositorio
- Utilizar variables de entorno para secretos
- No versionar archivos `.env`
- No almacenar información financiera sensible en el repositorio

---

## Limitaciones actuales

Cendra `v0.1` es un MVP funcional y presenta limitaciones conocidas:

- No incluye autenticación
- No utiliza persistencia en base de datos
- No mantiene histórico entre sesiones
- No incorpora integraciones bancarias
- No incorpora integraciones ERP
- El Score utiliza reglas heurísticas
- La detección de anomalías es estadística y no implica fraude
- No constituye asesoría financiera

Estas limitaciones forman parte del alcance actual del MVP.

---

## Roadmap

### v0.1 — MVP

- [x] Carga Excel y CSV
- [x] Normalización
- [x] Validación
- [x] KPIs financieros
- [x] KPIs comerciales
- [x] Comparación temporal
- [x] Cendra Score
- [x] Cobertura del Score
- [x] Riesgo de concentración
- [x] HHI
- [x] Señales automáticas
- [x] Detección de anomalías
- [x] Filtros interactivos
- [x] Reporte ejecutivo Excel
- [x] Interfaz personalizada

### v0.2 — Producto

- [ ] Persistencia de datos
- [ ] Autenticación
- [ ] Gestión de organizaciones
- [ ] Histórico de análisis
- [ ] Configuración de reglas
- [ ] Reportes PDF
- [ ] Mejoras metodológicas de anomalías

### v0.3 — Inteligencia

- [ ] Resumen ejecutivo asistido por IA
- [ ] Explicación automática de variaciones
- [ ] Consultas en lenguaje natural
- [ ] Alertas inteligentes
- [ ] Recomendaciones contextuales

### Futuro

- [ ] Integraciones ERP
- [ ] Integraciones bancarias
- [ ] APIs externas
- [ ] Forecast financiero
- [ ] Arquitectura multiusuario

---

## Principios del proyecto

Cendra se desarrolla alrededor de cuatro principios:

### 1. Claridad

Los indicadores deben ser comprensibles para usuarios no técnicos.

### 2. Transparencia

Las métricas y scores deben explicar qué información utilizan.

### 3. Calidad de datos

No se deben ejecutar análisis financieros sobre información inválida sin advertir al usuario.

### 4. Evolución incremental

Las nuevas capacidades deben responder a necesidades reales y no únicamente aumentar el número de funcionalidades.

---

## Estado del proyecto

**Versión:** `v0.1.0`

**Estado:** MVP funcional

**Objetivo actual:** validación técnica, demostración de producto y recopilación de feedback.

---

## Autor

**Giussepe Delgado**

Desarrollador de software con experiencia en soluciones empresariales, integraciones, procesamiento de datos y sistemas financieros.

---

## Licencia

Este proyecto se encuentra actualmente en desarrollo.

Antes de reutilizar, redistribuir o utilizar comercialmente el código, revisa la licencia definida en el repositorio.