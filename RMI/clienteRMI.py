import Pyro5.api
import argparse
import time

def cargar_configuracion():
    parser = argparse.ArgumentParser(description='Script para CLIENTE RMI')
    parser.add_argument('ruta_archivo', type=str, help='Ruta del archivo de configuración')
    args = parser.parse_args()
    ruta_configuracion = args.ruta_archivo
    return ruta_configuracion

def leer_logs(log_filename):
    with open(log_filename, 'r') as archivo:
        return archivo.readlines()

def enviar_logs(logs, central_log_server):
    for log in logs:
        parts = log.strip().split(', ')
        timestamp, event_type, juego, action = parts[:4]
        args = parts[4:]
        central_log_server.log_event(event_type, juego, action, *args)

if __name__ == "__main__":
    ruta_configuracion = cargar_configuracion()
    log_filename = ruta_configuracion.replace('.json', '.log')
    
    logs = leer_logs(log_filename)
    
    central_log_server = Pyro5.api.Proxy("PYRONAME:example.central_log_server")
    enviar_logs(logs, central_log_server)
