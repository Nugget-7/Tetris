import json
from Modelos import Jugador

class Manejador_Archivos:
    def __init__(self):
        pass
    def guardar_jugadores(self, jugadores):
        dict_jugadores = {}
        with open("jugadores.json", "w") as f:
            for i in range(len(jugadores)):
                dict_jugadores[f"jugador{i}"] = jugadores[i].__dict__#json.dumps(jugadores[i].__dict__)
            json.dump(dict_jugadores, f)
            f.close()


    def cargar_jugadores(self):
        try:
            with open("jugadores.json", "r") as f:
                contenido = f.read().strip()

                if not contenido:
                    return []

                json_data = json.loads(contenido)

        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

        data = []

        for key in json_data:
            info = json_data[key]
            jugador = Jugador.Jugador(info["nombre"], info["puntaje"])
            data.append(jugador)

        return data
