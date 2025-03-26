from flask import Flask, render_template, request
import subprocess
import paramiko

app = Flask(__name__)

wifi_device = "wlan0"  # Alterar conforme necessário para o seu dispositivo WiFi

@app.route('/')
def home():
    options = [
        {'name': 'Opção 1', 'route': '/opcao1'},
        {'name': 'Opção 2', 'route': '/opcao2'},
        {'name': 'Opção 3', 'route': '/opcao3'},
        {'name': 'Opção 4', 'route': '/opcao4'},
        {'name': 'Opção 5', 'route': '/opcao5'},
    ]
    return render_template('index.html', options=options)

@app.route('/opcao1')
def opcao1():
    return index()

def index():
    result = subprocess.check_output(["nmcli", "--colors", "no", "-m", "multiline", "--get-value", "SSID", "dev", "wifi", "list", "ifname", wifi_device])
    ssids_list = result.decode().split('\n')
    
    dropdowndisplay = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Wifi Control</title>
        </head>
        <body>
            <h1>Wifi Control</h1>
            <form action="/submit" method="post">
                <label for="ssid">Escolha uma rede WiFi:</label>
                <select name="ssid" id="ssid">
    """
    
    for ssid in ssids_list:
        only_ssid = ssid.removeprefix("SSID:")
        if len(only_ssid) > 0:
            dropdowndisplay += f"""
                    <option value="{only_ssid}">{only_ssid}</option>
            """
    
    dropdowndisplay += f"""
                </select>
                <p/>
                <label for="password">Senha: <input type="password" name="password"/></label>
                <p/>
                <input type="submit" value="Conectar">
            </form>
        </body>
        </html>
    """
    return dropdowndisplay

@app.route('/opcao2', methods=['GET', 'POST'])
def opcao2():
    if request.method == 'POST':
        command = request.form['command']
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            return render_template('command_output.html', output=output.decode())
        except subprocess.CalledProcessError as e:
            return render_template('command_output.html', output=e.output.decode())
    
    return render_template('command_input.html')

@app.route('/opcao3', methods=['GET', 'POST'])
def opcao3():
    if request.method == 'POST':
        ip = request.form['ip']
        port = request.form['port']
        username = request.form['username']
        password = request.form['password']  # Senha para autenticação SSH
        
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip, port=int(port), username=username, password=password)

            # Cria um canal e abre um shell
            shell = client.invoke_shell()
            shell.send("echo 'Conexão estabelecida!'\n")

            # Recebe a saída
            output = shell.recv(1024).decode()
            return render_template('ssh_output.html', output=output)
        
        except Exception as e:
            return f"Erro ao conectar via SSH: {str(e)}"

    return render_template('reverse_shell_input.html')

@app.route('/opcao4', methods=['GET', 'POST'])
def opcao4():
    if request.method == 'POST':
        host = request.form['host']
        ports = request.form['ports']
        
        # Construindo o comando nmap
        nmap_command = ["nmap", host, "-p", ports]
        try:
            result = subprocess.check_output(nmap_command, stderr=subprocess.STDOUT)
            output = result.decode()
        except subprocess.CalledProcessError as e:
            output = f"Erro ao executar nmap: {e.output.decode()}"
        
        return render_template('nmap_output.html', output=output)
    
    return render_template('nmap_input.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        ssid = request.form['ssid']
        password = request.form['password']
        connection_command = ["nmcli", "--colors", "no", "device", "wifi", "connect", ssid, "ifname", wifi_device]
        
        if len(password) > 0:
            connection_command.append("password")
            connection_command.append(password)
        
        result = subprocess.run(connection_command, capture_output=True)
        
        if result.stderr:
            return f"Erro: falha ao conectar à rede WiFi: <i>{result.stderr.decode()}</i>"
        elif result.stdout:
            return f"Sucesso: <i>{result.stdout.decode()}</i>"
        
        return "Erro: falha ao conectar."

# Resto das rotas para as outras opções

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
