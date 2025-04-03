# SpyPi

SpyPi é um sistema baseado em Flask que oferece diversas funcionalidades para administração remota, testes de segurança e interação com um dispositivo Arduino. O sistema inclui opções para configuração de Wi-Fi, execução de comandos remotos, criação de um hotspot e envio de comandos de teclado via Arduino.

## Funcionalidades

- **Configurar Wi-Fi**: Lista redes Wi-Fi e permite conectar a uma rede específica.
- **Executar um comando de Shell**: Permite executar comandos no sistema e visualizar a saída.
- **Abrir uma shell reversa**: Estabelece uma conexão reversa para um IP e porta específicos.
- **Realizar scan de portas**: Utiliza `nmap` para escanear portas em um host remoto.
- **Realizar enumeração de hosts**: Identifica hosts ativos na rede usando `nmap`.
- **Criar hotspot**: Configura um hotspot Wi-Fi utilizando `nmcli`.
- **Enviar Comandos de Teclado**: Envia sequências de comandos via Arduino para simular entrada de teclado.

## Instalação

Certifique-se de ter o Python 3 instalado e as dependências necessárias:

```bash
sudo apt update && sudo apt install python3 python3-pip python3-serial nmap netcat
pip install flask
```

## Uso

1. Clone este repositório:
   ```bash
   git clone https://github.com/dennislopes/spyPi.git
   cd spyPi
   ```
2. Inicie o servidor Flask:
   ```bash
   python3 app.py
   ```
3. Acesse no navegador:
   ```
   http://<IP-DO-RASPBERRY>:5000
   ```

## Configuração do Arduino

Se estiver usando um Arduino para envio de comandos de teclado, conecte-o via porta serial `/dev/ttyS0`. Certifique-se de que o Arduino está rodando um firmware compatível com emulação de teclado.

## Estrutura do Projeto

```
spyPi/
├── templates/            # Arquivos HTML para renderização
├── static/               # Arquivos estáticos (CSS, JS)
├── app.py                # Servidor Flask
├── README.md             # Documentação do projeto
```

## Exemplo de Uso

Para enviar comandos de teclado via Arduino:

1. Acesse `http://<IP-DO-RASPBERRY>:5000/opcao7`
2. Insira os comandos desejados, como:
   ```
   GUI r
   STRING cmd
   ENTER
   STRING ipconfig /all
   ENTER
   ```
3. O Arduino irá processar os comandos e enviá-los ao sistema como entrada de teclado.

## Contribuição

Pull requests são bem-vindos! Para grandes mudanças, abra uma issue primeiro para discutir o que deseja modificar.

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

