#!/usr/bin/env python3
import sys
import subprocess
from rich.console import Console
from rich.table import Table
from pathlib import Path
console_stderr = Console(stderr=True)
console_stdout = Console()


def check_and_install_uv():
    """Comprueba si uv está instalado; si no, intenta instalarlo."""
    console_stderr.print("Comprobando si 'uv' está instalado...")

    try:
        subprocess.run(["uv", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        console_stderr.print("uv está instalado.")
    except Exception:
        console_stderr.print("uv no está instalado.")
        console_stderr.print("Intentando instalar uv...")

        try:
            subprocess.run(["pip", "install", "uv"], check=True)
            console_stderr.print("uv instalado correctamente.")
            subprocess.run(["uv", "init", "proyecto_sam"], check=True)
            subprocess.run(["uv", "add", "rich"], check=True)            
            console_stderr.print("uv y dependencia rich instalados correctamente.")
        except Exception:
            console_stderr.print("No se pudo instalar uv o sus dependencias automáticamente. Instálalo manualmente.")
            sys.exit(1)

def process_sam(file_path):
    print("Comenzando proceso de contado de reads con MAPQ = 60")
    total_reads = 0
    mapq_60 = 0

    with open(file_path, "r") as sam:
        for line in sam:
            if line.startswith("@"):
                continue
            fields = line.split("\t")
            if len(fields) < 5:         # Comprobación de columnas mínimas
                console_stderr.print(f"Advertencia: línea ignorada por formato incorrecto: {line.strip()}")
                continue
            
            try:
                mapq = int(fields[4])   # Comprobación de MAPQ numérico
            except ValueError:
                console_stderr.print(f"Advertencia: MAPQ no numérico, línea ignorada: {line.strip()}")
                continue
            total_reads += 1
            if mapq == 60:
                mapq_60 += 1
    return total_reads, mapq_60

def main():
    if len(sys.argv) != 2:
        console_stdout.print("Uso: python3 main.py <ruta_al_archivo.sam>")
        sys.exit(1)

    sam_path = Path(sys.argv[1])

    if not sam_path.exists():
        console_stderr.print(f"El archivo {sam_path} no existe.")
        sys.exit(1)

    check_and_install_uv()

    total, mapq60 = process_sam(sam_path)
    percentage = round((mapq60 / total) * 100, 2)

    table = Table(title="Resultados del análisis SAM")
    table.add_column("Métrica", style="black", no_wrap=True)
    table.add_column("Valor", style="black")

    table.add_row("Total de lecturas alineadas:", str(total))
    table.add_row("Lecturas con MAPQ = 60", str(mapq60))
    table.add_row("Porcentaje", f"{percentage} %")

    console_stdout.print(table)

main()
