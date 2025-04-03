# Projeto SpyPi

## Descrição
O **SpyPi** é uma interface web desenvolvida para rodar em um **Raspberry Pi**, permitindo a execução de diversos comandos de rede e automação. O projeto integra funcionalidades como:

- Configuração de Wi-Fi
- Execução de comandos de shell
- Abertura de uma shell reversa
- Scan de portas
- Enumeração de hosts
- Criação de hotspot
- Envio de comandos de teclado via um Arduino Pro Micro

## Tecnologias Utilizadas
- **Raspberry Pi** como servidor principal
- **Arduino Pro Micro** para envio de comandos de teclado
- **Flask** para criação da interface web
- **nmcli** para gerenciamento de redes Wi-Fi e hotspot
- **Nmap** para escaneamento de portas e enumeração de hosts
- **UART** para comunicação entre dispositivos

## Configuração da Conexão via UART
Para estabelecer a comunicação entre o **Raspberry Pi** e o **Arduino Pro Micro**, utilizamos a interface **UART**. Os passos básicos incluem:

1. **Habilitar a UART no Raspberry Pi:**
   - Editar o arquivo `/boot/config.txt` e adicionar:
     ```
     enable_uart=1
     ```
   - Desativar o console serial no `raspi-config` caso esteja ativado.
   
2. **Conectar os pinos corretamente:**
   - **Raspberry Pi TX (GPIO 14) → Arduino RX**
   - **Raspberry Pi RX (GPIO 15) → Arduino TX**
   - **GND → GND**

3. **Testar a comunicação:**
   - No Raspberry Pi, utilizar:
     ```sh
     sudo apt install minicom
     minicom -b 115200 -o -D /dev/serial0
     ```
   - No Arduino, configurar o monitor serial na mesma taxa de transmissão.

## Interface Web
Abaixo, algumas telas do projeto **SpyPi**:

### Tela Inicial
![Tela Inicial](image1.png)

### Envio de Comandos de Teclado
![Envio de Comandos](image2.png)

### Resultado do Scan de Portas
![Resultado do Scan](image3.png)

Essas telas ilustram algumas funcionalidades principais do **SpyPi**, permitindo interações intuitivas e eficientes com os dispositivos conectados.

## Conclusão
O **SpyPi** é um projeto versátil que permite realizar diversas operações de rede e automação diretamente via uma interface web. Com a integração do **Raspberry Pi** e **Arduino Pro Micro**, é possível expandir ainda mais as funcionalidades para atender diferentes cenários de uso.

