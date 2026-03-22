import openpyxl
from collections import defaultdict
import datetime
import os
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font
from utilidades import normalizar_nombre, pintar_encabezados

def consolidar(ruta_principal, ruta_nombres, carpeta_salida):
    # Abrir archivo principal
    libro = openpyxl.load_workbook(ruta_principal)

    # Detectar hojas EMA/EBA
    nombre_EMA, nombre_EBA = None, None
    for nombre in libro.sheetnames:
        if "EMA" in nombre.upper():
            nombre_EMA = nombre
        elif "EBA" in nombre.upper():
            nombre_EBA = nombre
    if not nombre_EMA or not nombre_EBA:
        raise ValueError("No se encontraron hojas EMA o EBA en el archivo.")

    EMA = libro[nombre_EMA]
    EBA = libro[nombre_EBA]

    # Leer archivo de nombres organizados
    ref_libro = openpyxl.load_workbook(ruta_nombres)
    ref_hoja = ref_libro.active
    mapa_departamentos = {}
    for clave, depto in ref_hoja.iter_rows(min_row=2, max_col=2, values_only=True):
        if clave:
            clave_norm = normalizar_nombre(clave)
            mapa_departamentos[clave_norm] = depto

    # Crear hoja resultado
    if "Resultado Consolidado" in libro.sheetnames:
        libro.remove(libro["Resultado Consolidado"])
    resultado = libro.create_sheet("Resultado Consolidado")

    # Mapas y encabezados
    mapa_indices = {
        "I": 19, "J": 20, "H": 21, "L": 22, "M": 23,
        "N": 24, "O": 25, "P": 26, "K": 28, "Q": 29
    }

    encabezado = [""] * 30
    encabezado[0] = EMA[1][0].value
    encabezado[1] = EMA[1][1].value
    encabezado[2] = "Departamento"
    for idx in range(2, 18):
        encabezado[idx+1] = EMA[1][idx].value
    for col, destino_idx in mapa_indices.items():
        idx_origen = openpyxl.utils.column_index_from_string(col)-1
        encabezado[destino_idx] = EBA[1][idx_origen].value
    encabezado[27] = "Total"
    resultado.append(encabezado)
    pintar_encabezados(resultado)

    # Agrupar filas EMA/EBA
    filas_EMA = [fila for fila in EMA.iter_rows(min_row=2, max_col=19, values_only=True) if fila[0]]
    filas_EBA = [fila for fila in EBA.iter_rows(min_row=2, max_col=18, values_only=True) if fila[0]]

    grupo_EMA = defaultdict(list)
    grupo_EBA = defaultdict(list)
    for fila in filas_EMA:
        grupo_EMA[fila[0]].append(fila)
    for fila in filas_EBA:
        grupo_EBA[fila[0]].append(fila)

    valores_comunes = set(grupo_EMA.keys()) & set(grupo_EBA.keys())

    grupos = defaultdict(list)
    for valor in valores_comunes:
        filas_EMA = grupo_EMA[valor]
        filas_EBA = grupo_EBA[valor]
        max_reps = max(len(filas_EMA), len(filas_EBA))

        clave_norm = normalizar_nombre(filas_EMA[0][1])
        depto = mapa_departamentos.get(clave_norm, "SIN DEPTO") or "SIN DEPTO"

        for i in range(max_reps):
            fila_EMA = list(filas_EMA[i % len(filas_EMA)])
            fila_EBA = filas_EBA[i % len(filas_EBA)]

            fila_final = [""] * 30
            fila_final[0] = fila_EMA[0]
            fila_final[1] = fila_EMA[1]
            fila_final[2] = depto
            for idx in range(2, 18):
                fila_final[idx+1] = fila_EMA[idx]
            for col, destino_idx in mapa_indices.items():
                idx_origen = openpyxl.utils.column_index_from_string(col)-1
                fila_final[destino_idx] = fila_EBA[idx_origen]

            valor_EMA_S = fila_EMA[18] or 0
            valor_EBA_R = fila_EBA[17] or 0
            fila_final[27] = valor_EMA_S + valor_EBA_R

            grupos[depto].append(fila_final)

    # Guardar filas de totales
    filas_totales = {}
    for depto in sorted(grupos.keys()):
        filas = grupos[depto]
        resultado.append([None, depto])
        inicio = resultado.max_row + 1
        for fila in filas:
            resultado.append(fila)
        fin = resultado.max_row

        fila_formula = [""] * 8
        for col in range(9, 31):
            letra = get_column_letter(col)
            formula = f"=SUM({letra}{inicio}:{letra}{fin})"
            fila_formula.append(formula)
        resultado.append(fila_formula)

        fila_total = resultado.max_row
        filas_totales[depto] = fila_total

        resultado.append([])
        resultado.append([])
        resultado.append([])

    # Tablas verticales
    conceptos = [
        "INFONAVIT","SAR","CESANTÍA PATRONAL",
        "CESANTÍA OBRERO","IMSS PATRONAL","IMSS OBRERO","TOTAL"
    ]
    mapa_resumen = {
        "INFONAVIT": ["W","AA"],
        "SAR": ["V"],
        "CESANTÍA PATRONAL": ["T"],
        "CESANTÍA OBRERO": ["U"],
        "IMSS PATRONAL": ["I","J","L","N","P","Q","S"],
        "IMSS OBRERO": ["K","M","O","R"]
    }

    col_inicio = 32
    fila_inicio = 2
    for depto in sorted(grupos.keys()):
        col_letra1 = get_column_letter(col_inicio)
        col_letra2 = get_column_letter(col_inicio+1)
        rango = f"{col_letra1}{fila_inicio}:{col_letra2}{fila_inicio}"
        resultado.merge_cells(rango)
        resultado.cell(row=fila_inicio, column=col_inicio, value=depto).font = Font(bold=True)

        for i, concepto in enumerate(conceptos, start=1):
            resultado.cell(row=fila_inicio+i, column=col_inicio, value=concepto)

            if concepto in mapa_resumen:
                refs = [f"{col}{filas_totales[depto]}" for col in mapa_resumen[concepto]]
                formula = f"=SUM({','.join(refs)})"
            elif concepto == "TOTAL":
                formula = f"=SUM({col_letra2}{fila_inicio+1}:{col_letra2}{fila_inicio+len(conceptos)-1})"
            else:
                formula = "$ -"

            celda_valor = resultado.cell(row=fila_inicio+i, column=col_inicio+1, value=formula)
            celda_valor.number_format = '"$"#,##0.00'

        col_inicio += 3

    # Celda BM9
    refs_totales = []
    col_inicio = 32
    fila_inicio = 2
    for depto in sorted(grupos.keys()):
        col_letra_valor = get_column_letter(col_inicio+1)
        fila_total_tabla = fila_inicio + len(conceptos)
        refs_totales.append(f"{col_letra_valor}{fila_total_tabla}")
        col_inicio += 3

    formula_BM9 = f"=SUM({','.join(refs_totales)})"
    celda_BM9 = resultado.cell(row=9, column=openpyxl.utils.column_index_from_string("BM"), value=formula_BM9)
    celda_BM9.font = Font(bold=True)
    celda_BM9.number_format = '"$"#,##0.00'

    # Guardar archivo final
    hoy = datetime.date.today()
    mes = hoy.strftime("%B")
    año = hoy.year
    nombre_archivo = f"revision consolidada {mes}, {año}.xlsx"
    ruta_salida = os.path.join(carpeta_salida, nombre_archivo)
    libro.save(ruta_salida)
    return ruta_salida
