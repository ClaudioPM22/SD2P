import Pyro5.api
import logging
import time

class CentralLogServer:
    def __init__(self):
        log_filename = 'centralized_log.log'
        logging.basicConfig(filename=log_filename,
                            filemode='a',
                            level=logging.INFO,
                            format='%(asctime)s, %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')

    @Pyro5.api.expose
    def log_event(self, event_type, juego, action, *args):
        timestamp = int(time.time())
        log_message = f'{timestamp}, {event_type}, {juego}, {action}, ' + ', '.join(map(str, args))
        logging.info(log_message)
        return "Logged Successfully"

daemon = Pyro5.api.Daemon()
ns = Pyro5.api.locate_ns()
uri = daemon.register(CentralLogServer)
ns.register("example.central_log_server", uri)

print("Central Log Server is ready.")
daemon.requestLoop()
