import serial.tools.list_ports as sertools
import serial
import logging
import sys
import json
import serial
import time
import configparser

class HumonSens:
    """
    Classe pour gérer la connexion et la lecture des données d'un capteur capacitif flexible via le port série du HumonSens.
    """

    def __init__(self, config_file='humonsens.ini'):
        """
        Initializes the FlexSens object with default serial communication parameters.

        Attributes:
            port (str): The serial port to use for communication.
            baud_rate (int): The baud rate for the serial communication.
            parity (serial.Serial.PARITY_*): The parity bit setting for the serial communication.
            stopbits (serial.Serial.STOPBITS_*): The number of stop bits for the serial communication.
            bytesize (serial.Serial.EIGHTBITS): The number of data bits for the serial communication.
            xonxoff (bool): Enables or disables software flow control.
            timeout (int or float): The read timeout value for the serial communication.
            serial_connection (serial.Serial or None): The serial connection object, initialized as None.
        """
        # Lire les paramètres de configuration du fichier de configuration
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

        # Extraire les paramètres de configuration
        self.port = self.config["SENSOR"]["port"]
        self.baudrate = int(self.config["SENSOR"]["baudrate"])
        self.parity = serial.PARITY_NONE
        self.stopbits = serial.STOPBITS_ONE
        self.bytesize = serial.EIGHTBITS
        self.xonxoff = True
        self.timeout = int(self.config["SENSOR"]["timeout"])
        self.serial_connection = None

        # Configurer les paramètres de logging
        log_file = self.config.get('LOGGING', 'log_file')
        log_level = self.config.get('LOGGING', 'log_level').upper()
        log_format = self.config.get('LOGGING', 'log_format')
        
        # Créer un gestionnaire pour le fichier de log
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, log_level))
        file_handler.setFormatter(logging.Formatter(log_format))
        
        # Créer un gestionnaire pour la sortie console avec affichage instantané
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level))
        console_handler.setFormatter(logging.Formatter(log_format))
        console_handler.flush = sys.stdout.flush  # Assure l'affichage instantané
        
        # Configurer le logger racine
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, log_level))
        
        # Ajouter les gestionnaires au logger racine
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
        
        # Initialisation d'une connexion série 'vide' à la balance
        self.serial_connection = None

        logging.info("Configuration du capteur HumonSens V2.0 .")

    def __open_link(self):
        """
        Établit la connexion série avec le HumonSens.
        """
        try:
            self.serial_connection = serial.Serial(
                self.port, 
                self.baudrate, 
                parity=self.parity,
                stopbits=self.stopbits,
                bytesize=self.bytesize,
                xonxoff=self.xonxoff,
                timeout=self.timeout
            )
            logging.info("Liaison serie avec le capteur etablie")
            
        except Exception as e:
            logging.error(f"Erreur lors de la connexion au HumonSens: {e}")
            
    def __get_values(self, frequency: int = 10000, wait_period=0.6):
        """
        Reads values from a serial connection at a specified frequency.
        Args:
            frequency (int): The frequency at which to read values. Default is 10000.
            wait_period (float): The period to wait between checks for available data. Default is 0.6 seconds.
        Returns:
            dict: A dictionary containing the read values and the requested frequency. 
                  If the JSON decoding fails, an empty dictionary is returned.
        Raises:
            json.JSONDecodeError: If the last line read from the serial connection cannot be decoded as JSON.
        """
        print(f"Reading serial on 1 with frequency {frequency}")

        # We set the frequency
        self.serial_connection.write(f"SX{frequency}\n".encode("utf-8"))
        # We wait for the values to be ready
        sleep_count = 0

        # We wait for the values to be ready
        while not self.serial_connection.in_waiting and sleep_count < 10:
            time.sleep(wait_period)
            sleep_count += 1
            logging.info(f"Sleep count: {sleep_count}")

        last_line = "{}"
        # We exhaust the serial connection to the last value    
        while self.serial_connection.in_waiting > 0:
            last_line = self.serial_connection.readline().decode("utf-8")
            logging.info(f"Read line: {last_line}")

        try:
            values = json.loads(last_line)
            values["asked_frequency"] = frequency
        except json.JSONDecodeError:
            logging.error(f"Could not decode json: {last_line}")
            return {}
        
        return values
    
    def __close_link(self):
        """
        Closes the serial connection.
        """
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            logging.info('Connexion série fermée.')

    def get_ports(self):
        """
        Retourne la liste des ports série disponibles.
        Returns:
            list: Liste des ports série disponibles.
        """ 
        return sertools.comports()

    def run(self):
        try:
            self.__open_link()
            value=self.__get_values()
            logging.info(f'Valeur recue: {value}')
            return value
        except Exception as e:
            logging.error(f'Erreur lors de la routine de mesure: {e}')
        finally:
            self.__close_link()


    
if __name__ == "__main__":
    humonsens = HumonSens()

    # for port in humonsens.get_ports():
    #     print(port)

    measures = humonsens.run()

    # Valeur recue: {'ID': 'dryCheck_1', 'cap': 22, 'freq': 10000, 'temp': 25, 'RH': 33, 'asked_frequency': 10000}
    for key, value in measures.items():
        print(f"{key}: {value}")

