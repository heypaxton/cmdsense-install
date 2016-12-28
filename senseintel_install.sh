#!/bin/bash

#set -e

confirminstall () {
    read -r -p "$1 [y/n]" response
    case $response in
        [yY])
            true
            ;;
        *)
            false
            ;;
    esac
}

if ! confirminstall "Would you like to install Senseintel?"; then
    exit
fi

echo "Installing Senseintel on the device"

echo "Getting system updates"
sudo apt-get updates

echo "Adding network connection to /etc/network/interfaces"
read -r -p "$1 Enter your SSID:" ssid
read -r -p "$1 Enter your wifi password:" wifipass

cat > /etc/network/interfaces << EOF
auto wlan0
allow-hotplug wlan0
iface wlan0 inet dhcp
${TAB} wpa-ssid: "$ssid" 
${TAB} wpa-psk:  "$wifipass" 

auto lo eth0
iface lo inet loopback
iface eth0 inet static
${TAB} address 192.168.0.22
${TAB} netmask 255.255.255.0
${TAB} gateway 192.168.0.20
EOF

installed=`which git`
if [ "$installed" == "" ]; then
    echo "Installing Git"
    sudo apt-get install git
fi

echo "Installing GPS"
sudo apt-get install gpsd gpsd-clients python-gps
# TODO start GPS

echo $'\n'
echo "Senseintel installation complete"
echo $'\n'

echo "Downloading sensor application"
#git clone git@github.com:heypaxton/senseintel-sensorapp.git $HOME/pythoncode/sensorapp

echo "Starting sensor application"
#python $HOME/pythoncode/sensorapp.py

