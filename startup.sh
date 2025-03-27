sudo nmcli con add type wifi ifname wlan0 con-name my-hotspot autoconnect yes ssid MyHotspot
sudo nmcli con modify my-hotspot 802-11-wireless.mode ap 802-11-wireless.band bg ipv4.method shared
sudo nmcli con modify my-hotspot wifi-sec.key-mgmt wpa-psk
sudo nmcli con modify my-hotspot wifi-sec.psk "MinhaSenha123"
sudo nmcli con up my-hotspot
