"""
actualizar_json.py  —  Campaña Antiinfluenza
=============================================
Convierte el Excel en datos.json listo para el dashboard.
Uso: python actualizar_json.py
Dependencias: pip install pandas openpyxl
"""
import pandas as pd, json, sys
from datetime import datetime
from pathlib import Path

EXCEL_FILE      = "Influenza.xlsx"   # ← cambia por el nombre de tu Excel
HOJA_HISTORICO  = "HISTORICO"
HOJA_ACTUALIZAR = "ACTUALIZAR"
OUTPUT_JSON     = "datos.json"

MES_NUM = {"ENERO":1,"FEBRERO":2,"MARZO":3,"ABRIL":4,"MAYO":5,"JUNIO":6,
           "JULIO":7,"AGOSTO":8,"SEPTIEMBRE":9,"OCTUBRE":10,"NOVIEMBRE":11,"DICIEMBRE":12}

def encontrar_excel():
    p = Path(EXCEL_FILE)
    if p.exists(): return str(p)
    c = list(Path(".").glob("*.xlsx")) + list(Path(".").glob("*.xls"))
    if c: print(f"⚠  Usando: {c[0].name}"); return str(c[0])
    print("❌  No se encontró Excel."); sys.exit(1)

def procesar(df, fuente, id_ini):
    rows = []
    col_sem = "SEMANA" if "SEMANA" in df.columns else None
    for i, r in df.iterrows():
        mes = str(r.get("MES","")).strip().upper()
        if not mes or mes == "NAN":
            continue  # saltar filas vacías
        try:
            dosis = int(float(r.get("DOSIS_MES", 0) or 0))
        except:
            dosis = 0
        try:
            anio = int(float(r.get("ANIO", 0) or 0))
        except:
            anio = 0
        rows.append({
            "id": id_ini + len(rows),
            "campania": str(r.get("CAMPANIA","")).strip(),
            "año": anio,
            "origen": str(r.get("ORIGEN","")).strip(),
            "grupo_objetivo": str(r.get("GRUPO_OBJETIVO","")).strip(),
            "mes": mes,
            "mes_num": MES_NUM.get(mes, 0),
            "semana": str(r.get(col_sem,"")).strip() if col_sem else "",
            "dosis": dosis,
            "fuente": fuente
        })
    return rows

def main():
    print("="*50)
    print("  datos.json — Campaña Antiinfluenza")
    print("="*50)
    archivo = encontrar_excel()
    print(f"\n📂 Leyendo: {archivo}")
    df_h = pd.read_excel(archivo, sheet_name=HOJA_HISTORICO)
    print(f"✅ {HOJA_HISTORICO}: {len(df_h)} filas")
    try:
        df_a = pd.read_excel(archivo, sheet_name=HOJA_ACTUALIZAR)
        print(f"✅ {HOJA_ACTUALIZAR}: {len(df_a)} filas")
    except:
        df_a = pd.DataFrame()
        print(f"⚠  {HOJA_ACTUALIZAR} no encontrada")
    r1 = procesar(df_h, "HISTORICO", 1)
    r2 = procesar(df_a, "ACTUALIZAR", len(r1)+1)
    todos = r1 + r2
    años  = sorted(set(r["año"] for r in todos))
    td    = sum(r["dosis"] for r in todos)
    data  = {
        "meta": {
            "dashboard_nombre": "Campaña de Vacunación Antiinfluenza",
            "area": "Epidemiología / Salud Pública",
            "ultima_actualizacion": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "total_registros": len(todos),
            "total_dosis": td,
            "anos_disponibles": años,
            "version": "1.0"
        },
        "registros": todos
    }
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n✅ {OUTPUT_JSON} generado: {len(todos):,} registros | {td:,} dosis | años: {años}")
    print("📌 Coloca datos.json junto a index.html para actualizar el dashboard.")
    print("="*50)

if __name__ == "__main__":
    main()
