import serial
import time

# Configura a porta serial (ajuste conforme necessário)
arduino = serial.Serial('/dev/ttyS0', 9600, timeout=1)  # Usando UART no Raspberry Pi
time.sleep(2)  # Aguarda o Arduino inicializar

def send_duckyscript(script):
    # Envia o comando para o Arduino via UART
    arduino.write(script.encode() + b'\n')  # Adiciona um '\n' ao final do script
    time.sleep(1)  # Aguarda a execução do comando

# Exemplo de DuckyScript para testar
duckyscript = """
STRING Hello, World!
ENTER
DELAY 500
STRING This is a DuckyScript example.
ENTER
"""
send_duckyscript(duckyscript)
