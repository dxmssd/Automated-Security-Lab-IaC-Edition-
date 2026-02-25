# Palabras prohibidas que queremos detectar
SECRET_KEYWORDS = ["api_key", "password", "token", "secret","username", "db_name", ]
DANGEROUS_CONFIGS = ["source_address_prefix      = \"*\"", "destination_port_range     = \"22\""]


def scan_file(filename):
    # PASO A: Inicializar la bandera en False (asumimos que está limpio)
    found_something = False

    try:
        with open(filename, 'r') as file:
            for line_number, line in enumerate(file, 1):
                clean_line = line.lower().strip()

                # Revisar Secretos
                for keyword in SECRET_KEYWORDS:
                    if keyword in clean_line:
                        print(f"[ALERTA] Línea {line_number}: Secreto -> '{keyword}'")
                        found_something = True  # <--- ¡Importante marcarlo!

                # Revisar Configs Peligrosas
                for pattern in DANGEROUS_CONFIGS:
                    if pattern.replace(" ", "") in clean_line.replace(" ", ""):
                        print(f"[CRÍTICO] CONFIGURACIÓN INSEGURA: Línea {line_number} -> '{pattern}'")
                        found_something = True

        return found_something

    except FileNotFoundError:
        print(f"Error: El archivo {filename} no existe.")
        return False



# Esto es lo que lee el Pipeline de CI/CD
if __name__ == "__main__":
    resultado = scan_file("terraform/main.tf")

    if resultado:
        print("\n FALLO: Se encontraron riesgos. Corregir antes de subir.")
        exit(1)  # Código de error para detener el Pipeline
    else:
        print("\n ÉXITO: No se detectaron riesgos conocidos.")
        exit(0)
