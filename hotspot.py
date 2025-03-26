import subprocess

def configurar_hotspot():
    print("Configurando hotspot SpyPi...")

    # Configuração do DHCP e IP fixo
    dhcp_config = """
interface wlan0
static ip_address=192.168.4.1/24
nohook wpa_supplicant
"""
    with open("/etc/dhcpcd.conf", "a") as file:
        file.write(dhcp_config)

    # Configuração do dnsmasq
    dnsmasq_config = """
interface=wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
"""
    with open("/etc/dnsmasq.conf", "w") as file:
        file.write(dnsmasq_config)

    # Configuração do hostapd
    hostapd_config = f"""
interface=wlan0
ssid=SpyPi
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=hackme
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
"""
    with open("/etc/hostapd/hostapd.conf", "w") as file:
        file.write(hostapd_config)

    # Apontar o novo hostapd.conf no sistema
    subprocess.run(["sed", "-i", "s|#DAEMON_CONF=\"\"|DAEMON_CONF=\"/etc/hostapd/hostapd.conf\"|g", "/etc/default/hostapd"])

    # Ativar encaminhamento de pacotes para rotear a conexão
    subprocess.run(["sh", "-c", "echo 1 > /proc/sys/net/ipv4/ip_forward"])

    print("Reiniciando serviços...")
    subprocess.run(["sudo", "systemctl", "restart", "dhcpcd"])
    subprocess.run(["sudo", "systemctl", "start", "dnsmasq"])
    subprocess.run(["sudo", "systemctl", "start", "hostapd"])

    print("Hotspot SpyPi ativado!")

if __name__ == "__main__":
    configurar_hotspot()
