from flask import Flask, render_template, request
import subprocess
import paramiko

app = Flask(__name__)

wifi_device = "wlan0"  # Alterar conforme necessário para o seu dispositivo WiFi

def hotspot_exists(connection_name):
    try:
        result = subprocess.run(["nmcli", "con", "show"], capture_output=True, text=True)
        return connection_name in result.stdout
    except Exception as e:
        return False

@app.route('/')
def home():
    options = [
        {'name': 'Configurar Wi-Fi', 'route': '/opcao1'},
        {'name': 'Executar um comando de Shell', 'route': '/opcao2'},
        {'name': 'Estabelecer conexão ssh', 'route': '/opcao3'},
        {'name': 'Realizar scan de portas', 'route': '/opcao4'},
        {'name': 'Realizar enumeração de hosts', 'route': '/opcao5'},
        {'name': 'Criar hotspot', 'route': '/opcao5'},
    ]
    return render_template('index.html', options=options)

@app.route('/opcao1')
def opcao1():
    return index()

def index():
    devices = ["wlan0", "wlan1"]
    ssids = {}
    for device in devices:
        try:
            result = subprocess.check_output([
                "nmcli", "--colors", "no", "-m", "multiline", "--get-value", "SSID", "dev", "wifi", "list", "ifname", device
            ])
            ssids[device] = [ssid.replace("SSID:", "").strip() for ssid in result.decode().split('\n') if ssid.strip()]
        except subprocess.CalledProcessError:
            ssids[device] = []
    
    dropdown_display = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Wifi Control</title>
        </head>
        <body>
            <h1>Wifi Control</h1>
            <form action="/submit" method="post">
                <label for="device">Escolha um adaptador WiFi:</label>
                <select name="device" id="device" onchange="updateSSIDList()">
                    <option value="wlan0">wlan0</option>
                    <option value="wlan1">wlan1</option>
                </select>
                <p/>
                <label for="ssid">Escolha uma rede WiFi:</label>
                <select name="ssid" id="ssid">
    """
    
    for device, ssids_list in ssids.items():
        for ssid in ssids_list:
            dropdown_display += f'<option class="{device}" value="{ssid}">{ssid}</option>'
    
    dropdown_display += """
                </select>
                <p/>
                <label for="password">Senha: <input type="password" name="password"/></label>
                <p/>
                <input type="submit" value="Conectar">
            </form>
            <script>
                function updateSSIDList() {
                    var selectedDevice = document.getElementById("device").value;
                    var options = document.getElementById("ssid").options;
                    for (var i = 0; i < options.length; i++) {
                        options[i].style.display = options[i].classList.contains(selectedDevice) ? "block" : "none";
                    }
                }
                window.onload = updateSSIDList;
            </script>
        </body>
        </html>
    """
    return dropdown_display

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

@app.route('/opcao6', methods=['GET', 'POST'])
def opcao6():
    if request.method == 'POST':
        device = request.form['device']
        ssid = request.form['ssid']
        password = request.form['password']
        connection_name = "my-hotspot"

        if hotspot_exists(connection_name):
            return f"Hotspot '{connection_name}' já existe."
        
        try:
            subprocess.run(["nmcli", "con", "add", "type", "wifi", "ifname", device, "con-name", connection_name, "autoconnect", "yes", "ssid", ssid], check=True)
            subprocess.run(["nmcli", "con", "modify", connection_name, "802-11-wireless.mode", "ap", "802-11-wireless.band", "bg", "ipv4.method", "shared"], check=True)
            subprocess.run(["nmcli", "con", "modify", connection_name, "wifi-sec.key-mgmt", "wpa-psk"], check=True)
            subprocess.run(["nmcli", "con", "modify", connection_name, "wifi-sec.psk", password], check=True)
            subprocess.run(["nmcli", "con", "up", connection_name], check=True)
            return f"Hotspot '{ssid}' criado com sucesso na interface {device}."
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
            <label for="ssid">Nome da Rede (SSID): <input type="text" name="ssid" required/></label>
            <p/>
            <label for="password">Senha: <input type="password" name="password" required/></label>
            <p/>
            <input type="submit" value="Criar Hotspot">
        </form>
    '''

# Resto das rotas para as outras opções

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
