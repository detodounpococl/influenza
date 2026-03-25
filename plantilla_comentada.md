# Plantilla de columnas esperadas (Excel → JSON)

Este documento describe las columnas que el script `actualizar_json.py` intentará mapear automáticamente.
Ajuste `MAPEO_COLUMNAS` en el script si su Excel usa nombres distintos.

## Columnas recomendadas (nombres en Excel) y su mapeo
- **Fecha** → `fecha`  
  Formato preferido: `YYYY-MM-DD` o una columna de fecha reconocible por Excel.
- **Hora** → `hora` (opcional)  
  Formato `HH:MM` o texto libre.
- **Mes** → `mes`  
  Nombre del mes en español (Enero, Febrero, ...). Si no existe, el script intentará inferirlo desde `fecha`.
- **Año** / **ANIO** → `año`  
  Año numérico (ej. 2025).
- **DOSIS_MES** / **Cantidad** → `cantidad`  
  Número entero con la cantidad registrada.
- **Categoría** / **GRUPO_OBJETIVO** → `categoria`  
  Categoría principal (ej. "Niños 6 meses a 5 años", "Personas mayores").
- **Subcategoría** → `subcategoria` (opcional)
- **Diagnóstico** / **Diagnóstico_Actividad** → `diagnostico_actividad` (opcional)  
  Si existe, activa la Pestaña 4 (Top 5). Si no existe, la pestaña mostrará un aviso.
- **Profesional** → `profesional` (opcional)
- **Turno** → `turno` (opcional)  
  Ej.: "Mañana", "Tarde", "Noche".
- **Observación** → `observacion` (opcional)

## Reglas y recomendaciones
- El script busca automáticamente el primer archivo `.xlsx` o `.xls` en la carpeta.
- La primera hoja será leída por defecto.
- Si su Excel tiene nombres de columna distintos, actualice `MAPEO_COLUMNAS` en `actualizar_json.py`.
- El script genera `datos.json` con la estructura:
  {
    "meta": { "dashboard_nombre":"", "area":"", "ultima_actualizacion":"", "total_registros": 0, "version":"1.0" },
    "registros": [ { "id":1, "fecha":"YYYY-MM-DD", "hora":"HH:MM", "mes":"Enero", "mes_num":1, "año":2025, "categoria":"", "subcategoria":"", "diagnostico_actividad":"", "cantidad":1, "profesional":"", "turno":"", "observacion":"" } ]
  }
- Campos opcionales:
  - `hora`, `turno`: si no existen, las interfaces que dependen de ellos (filtros) se ocultarán.
  - `diagnostico_actividad`: si no existe, la pestaña Top 5 mostrará un aviso y no fallará.

## Flujo recomendado para mantenimiento (sin programación)
1. Actualice el Excel con los datos nuevos.
2. Coloque el Excel en la misma carpeta que `actualizar_json.py`.
3. Ejecute: `python actualizar_json.py`
4. Suba `datos.json` resultante al repositorio de GitHub Pages.
5. En el dashboard (index.html) haga clic en **🔄 Actualizar** para recargar los datos remotos.

## Notas de calidad de datos
- Evite filas con celdas vacías en columnas clave (`fecha` o `año` y `mes` y `cantidad`).
- Use nombres de mes consistentes (recomendado: Enero, Febrero, Marzo, ...).
- Verifique que `cantidad` sea numérico; el script intentará convertirlo a entero.
