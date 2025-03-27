import subprocess

def ativar_bluetooth():
    # Ativa o modo discoverable do Bluetooth
    subprocess.run(["bluetoothctl", "discoverable", "on"])

def monitorar_bluetooth():
    # Abre o processo do bluetoothctl
    process = subprocess.Popen(
        ["bluetoothctl"], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        text=True
    )

    # Lendo a saída do bluetoothctl em tempo real
    for linha in process.stdout:
        print(linha.strip())  # Exibe no console
        if "[NEW]" in linha:
            print("Novo dispositivo detectado! Executando outro programa...")
            #subprocess.run(["python3", "outro_programa.py"])  # Substitua pelo seu programa

if __name__ == "__main__":
    ativar_bluetooth()
    monitorar_bluetooth()

