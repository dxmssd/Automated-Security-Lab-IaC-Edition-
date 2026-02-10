import re
import time
import requests
import syslog # Para hablarle directo al sistema

# ============================================================================
# CONFIGURACIÓN
# ============================================================================
# Archivo donde el sistema anota los intentos de SSH
LOG_PATH = "/var/log/auth.log"

# ============================================================================
# FUNCIONES
# ============================================================================
def get_location(ip):
    try:
        # Consulta a API de geolocalización gratuita
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        if r['status'] == 'success':
            return f"{r['lat']},{r['lon']},{r['country']},{r['city']}"
        else:
            return "0,0,Unknown,Unknown"
    except Exception:
        return "0,0,Error,Error"

# ============================================================================
# BUCLE PRINCIPAL
# ============================================================================
print("[*] Monitoring attacks and injecting into Syslog...")
print("-" * 50)

try:
    with open(LOG_PATH, "r") as f:
        # Ir al final del archivo para procesar solo lo nuevo
        f.seek(0, 2)
        
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue

            # Detectar intento fallido de SSH
            if "Failed password" in line:
                # Extraer IP con Regex
                ip_match = re.search(r'from ([\d\.]+) port', line)
                
                if ip_match:
                    ip = ip_match.group(1)
                    geo = get_location(ip)

                    # Formatear el mensaje para Sentinel
                    # Usamos un prefijo claro para que la consulta KQL sea fácil
                    log_msg = f"HONEYPOT_EVENT | IP: {ip} | Geo: {geo} | Raw: {line.strip()}"

                    # INYECCIÓN DIRECTA A SYSLOG (Simulamos un evento de auth)
                    syslog.openlog(ident="HONEYPOT")
                    syslog.syslog(syslog.LOG_AUTH | syslog.LOG_INFO, log_msg)
                    syslog.closelog()
                    
                    print(f"[!] Attack detected and injected: {ip} ({geo.split(',')[-2]})")

except KeyboardInterrupt:
    print("\n[!] Stopped by user.")
except Exception as e:
    print(f"\n[!] Error: {e}")
