import serial
import time

# Configura a porta serial (ajuste conforme necessário)
arduino = serial.Serial('/dev/ttyS0', 9600, timeout=1)  # Usando UART no Raspberry Pi
time.sleep(2)  # Aguarda o Arduino inicializar

def send_duckyscript(script):
    # Envia o comando para o Arduino via UART
    arduino.write(script.encode() + b'\n')  # Adiciona um '\n' ao final do script
    time.sleep(1)  # Aguarda a execução do comando

def send_duckyscript_from_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.rstrip("\n")
            if line:
                print(f"Enviando: {repr(line)}")
                arduino.write((line + '\n').encode("utf-8"))
                time.sleep(1.5)  # Pequeno delay entre comandos para evitar erros

send_duckyscript_from_file("payload.txt")
