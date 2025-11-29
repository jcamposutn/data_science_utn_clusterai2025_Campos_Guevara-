import subprocess

# Lista de scripts a correr de manera secuencial
scripts = [
    "clusterai_joaquin_campos_guevara_eda.py",
    "clusterai_joaquin_campos_guevara_manipulaciones.py",
    "clusterai_joaquin_campos_guevara_machine_learning.py"
]

# genero un archivo tipo log que recolecte los outputs de cada archivo
log_file = "output.log"

# abro el archivo en modo escritura y recorro los scripts listados
with open(log_file, "w") as log:
    for script in scripts:
        log.write(f"\n=== Ejecutando {script} ===\n")
        try:
            # corre el script y guarda la salida estándar y el error si hubiera
            result = subprocess.run(
                ["python", script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Si corre el EDA, no queremos que imprima todas las comprobaciones realizadas
            if "clusterai_joaquin_campos_guevara_eda.py" in script.lower():
                log.write("Limpieza y transformacion del dataframe airbnb_df \n")
            elif "clusterai_joaquin_campos_guevara_manipulaciones.py" in script.lower():
                log.write("Se entrenó a ambos modelos de ML con los datos \n")
            else:
                log.write(result.stdout)
                log.write(result.stderr)

            log.write(f"\n=== Finalizado {script} ===\n")

        except Exception as e:
            log.write(f"Error al ejecutar {script}: {e}\n")

