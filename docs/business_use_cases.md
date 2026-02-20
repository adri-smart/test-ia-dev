# KAN-468: 10 Casos de Uso de Negocio Predefinidos

Este documento contiene 10 casos de uso de negocio predefinidos para medir de forma consistente la tasa de interpretación correcta del agente conversacional y asegurar que cumplimos con el KPI de éxito del 80%.

Estos casos han sido aprobados por el Product Owner.

---

### Caso de Uso 1: Consulta de Ventas Totales
- **Pregunta de Usuario:** "muéstrame las ventas totales del último trimestre"
- **Intención Esperada:** `consultar_ventas_trimestrales`
- **Descripción:** El usuario quiere conocer el monto total de ventas consolidadas en los últimos tres meses.

---

### Caso de Uso 2: Producto Más Vendido
- **Pregunta de Usuario:** "¿Cuál es el producto más vendido de este mes?"
- **Intención Esperada:** `obtener_producto_mas_vendido`
- **Descripción:** El usuario busca identificar el producto con el mayor número de unidades vendidas en el mes actual.

---

### Caso de Uso 3: Reporte de Ventas por Región
- **Pregunta de Usuario:** "Genera un reporte de ventas por región"
- **Intención Esperada:** `generar_reporte_regional`
- **Descripción:** El usuario necesita un desglose de las ventas totales por cada una de las regiones geográficas definidas.

---

### Caso de Uso 4: Comparativa Anual de Ventas
- **Pregunta de Usuario:** "Compara el rendimiento de ventas de este año con el año pasado"
- **Intención Esperada:** `comparar_rendimiento_anual`
- **Descripción:** El usuario quiere una comparación porcentual y absoluta del total de ventas del año actual contra el año anterior.

---

### Caso de Uso 5: Proyección de Ingresos
- **Pregunta de Usuario:** "Muéstrame la proyección de ingresos para Q3"
- **Intención Esperada:** `proyectar_ingresos_trimestre`
- **Descripción:** El usuario solicita una estimación de los ingresos para el tercer trimestre del año.

---

### Caso de Uso 6: Clientes de Mayor Valor
- **Pregunta de Usuario:** "¿Quiénes son los clientes con mayor valor?"
- **Intención Esperada:** `identificar_clientes_valiosos`
- **Descripción:** El usuario busca un listado de los clientes que más han gastado (top N por ingresos).

---

### Caso de Uso 7: Segmentación por Comportamiento
- **Pregunta de Usuario:** "dame la lista de clientes que compraron el producto A y no el B"
- **Intención Esperada:** `segmento_comportamiento_compra`
- **Descripción:** El usuario quiere un segmento específico de clientes basado en su historial de compras.

---

### Caso de Uso 8: Tasa de Retención de Clientes
- **Pregunta de Usuario:** "¿cuál es nuestra tasa de retención de clientes para el último semestre?"
- **Intención Esperada:** `calcular_tasa_retencion`
- **Descripción:** El usuario necesita conocer el porcentaje de clientes existentes que continúan comprando.

---

### Caso de Uso 9: Rendimiento de Campaña
- **Pregunta de Usuario:** "analiza el rendimiento de la campaña 'Verano2024'"
- **Intención Esperada:** `analizar_rendimiento_campana`
- **Descripción:** El usuario quiere métricas sobre el impacto de una campaña de marketing específica.

---

### Caso de Uso 10: Clientes Inactivos
- **Pregunta de Usuario:** "identifica clientes que no han comprado en los últimos 6 meses"
- **Intención Esperada:** `identificar_clientes_inactivos`
- **Descripción:** El usuario busca un listado de clientes en riesgo de abandono para campañas de reactivación.
