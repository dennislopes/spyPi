# spyPi - Interface web para hacking de redes com raspberry Pi

Este projeto é uma aplicação web construída com Flask, permitindo executar uma série de comandos de rede e sistema em um Raspberry Pi ou computador. Ele oferece a capacidade de configurar Wi-Fi, executar comandos de shell, criar hotspots, realizar escaneamento de portas, enumeração de hosts e até abrir uma shell reversa.

## Funcionalidades

- **Configurar Wi-Fi**: Permite buscar redes Wi-Fi disponíveis e conectar-se a uma delas.
- **Executar um comando de Shell**: Envia comandos shell e exibe a saída.
- **Abrir uma Shell Reversa**: Permite executar uma shell reversa para acessar o sistema remotamente.
- **Scan de Portas**: Realiza um escaneamento de portas usando o `nmap`.
- **Enumeração de Hosts**: Enumera dispositivos em uma rede utilizando `nmap`.
- **Criar Hotspot**: Cria um hotspot Wi-Fi utilizando a interface de rede do dispositivo.

## Requisitos

- Python 3.x
- Flask (`pip install flask`)
- `nmcli` (ferramenta de linha de comando do NetworkManager)
- `nmap` (ferramenta de escaneamento de redes)
