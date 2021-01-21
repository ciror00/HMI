from utils.ntp import human_date

# Nombre de archivo con formato de fecha
PATH = "info.log"


def logger(message, log_type="debug"):
    """Crea achivos de registro"""
    date = human_date()
    try:
        with open(PATH, "a") as file:
            file.write("{}-{}-{} {}:{}:{} - [{}]: {}\n".format(
                date[0], date[1], date[2],
                date[4], date[5], date[6],
                log_type.upper(), message))
    except OSError as err:
        print("No se puede abrir el archivo de logs ({}): {}".format(PATH, err))
