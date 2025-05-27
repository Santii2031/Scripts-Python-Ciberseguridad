import subprocess
import datetime

def ejecutar_nmap(host):
    print(f"Ejecutando escaneo con Nmap en {host}...\n")
    comando = ["nmap", "-p-", "-sSCV", "-n", "-Pn", host]
    resultado = subprocess.run(comando, capture_output=True, text=True)
    return resultado.stdout

def parsear_salida_nmap(salida):
    resultados = []
    linea_puertos = False

    for linea in salida.splitlines():
        if linea.startswith("PORT"):
            linea_puertos = True
            continue
        if linea_puertos:
            if linea.strip() == "" or linea.startswith("Nmap done:"):
                break
            partes = linea.split()
            if len(partes) >= 3:
                puerto = partes[0]
                estado = partes[1].lower()
                servicio = partes[2]
                version = " ".join(partes[3:]) if len(partes) > 3 else ""
                # Solo puertos abiertos
                if estado == "open":
                    resultados.append((puerto, estado, servicio, version))
    return resultados

def generar_html(host, resultados, archivo_salida="reporte_nmap.html"):
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_puertos = len(resultados)

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8" />
    <title>Reporte Nmap - {host}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 30px auto;
            max-width: 900px;
            background: #f7f9fc;
            color: #222;
        }}
        h1 {{
            color: #2a4365;
            text-align: center;
            margin-bottom: 5px;
        }}
        .info {{
            text-align: center;
            margin-bottom: 20px;
            font-size: 1rem;
            color: #555;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            background: white;
        }}
        th, td {{
            padding: 12px 15px;
            border: 1px solid #ddd;
            text-align: left;
        }}
        th {{
            background-color: #2a4365;
            color: white;
            text-transform: uppercase;
            font-size: 0.9rem;
        }}
        tr:nth-child(even) {{
            background-color: #f2f6fa;
        }}
        .estado-open {{
            color: #2e7d32;
            font-weight: bold;
        }}
        .estado-closed {{
            color: #c62828;
            font-weight: bold;
        }}
        footer {{
            margin-top: 25px;
            font-size: 0.8rem;
            text-align: center;
            color: #777;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <h1>Reporte de Escaneo Nmap</h1>
    <p class="info">Host escaneado: <strong>{host}</strong> | Fecha y hora: {fecha}</p>
    <p class="info">Total de puertos abiertos detectados: <strong>{total_puertos}</strong></p>

    <table>
        <thead>
            <tr>
                <th>Puerto</th>
                <th>Estado</th>
                <th>Servicio</th>
                <th>Versión</th>
            </tr>
        </thead>
        <tbody>
    """

    for puerto, estado, servicio, version in resultados:
        clase_estado = "estado-open" if estado == "open" else "estado-closed"
        html += f"<tr><td>{puerto}</td><td class='{clase_estado}'>{estado}</td><td>{servicio}</td><td>{version}</td></tr>\n"

    html += """
        </tbody>
    </table>

    <footer>Reporte generado automáticamente con Nmap</footer>
</body>
</html>
"""

    with open(archivo_salida, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n✅ Reporte generado en '{archivo_salida}'. ¡Abrilo en tu navegador!")

def main():
    print("=== Escáner con Nmap + Reporte HTML ===\n")
    host = input("Ingresá la IP o dominio a escanear: ").strip()
    salida = ejecutar_nmap(host)
    resultados = parsear_salida_nmap(salida)

    if not resultados:
        print("⚠️ No se encontraron puertos abiertos o no se pudo interpretar la salida.")
    else:
        generar_html(host, resultados)

if __name__ == "__main__":
    main()
