#!/bin/bash
if ! [ -n "$BASH_VERSION" ];then
    echo "This is not bash, calling self with bash....";
    SCRIPT=$(readlink -f "$0")
    /bin/bash $SCRIPT
    exit;
fi

# Check have sudo/root permissions.
USER=`whoami`

if [ "$USER" != "root" ]; then
        echo "You need to run me with sudo!"
        exit
fi

# Ask the user for the path where they are going to stick the VPN config files
read -e -p "Path where you will store client configs (your local machine): 
" \
-i "/home/USER/my-vpn" CONFIG_FILE_PATH

# Update OS to latest
sudo apt-get update && sudo apt-get dist-upgrade -y

# Install needed packages
sudo apt-get install openvpn openssl udev -y

sudo cp -R /usr/share/doc/openvpn/examples/easy-rsa/ /etc/openvpn

# Fix issue with openssl
sed -i 's;cnf="$1/openssl.cnf";cnf="$1/openssl-1.0.0.cnf";' /etc/openvpn/easy-rsa/2.0/whichopensslcnf


# Rather than execute the vars dir, lets just define them here:
export EASY_RSA="/etc/openvpn/easy-rsa/2.0/"
export OPENSSL="openssl"
export PKCS11TOOL="pkcs11-tool"
export GREP="grep"
export KEY_CONFIG=`$EASY_RSA/whichopensslcnf $EASY_RSA`
export KEY_DIR="$EASY_RSA/keys"
export PKCS11_MODULE_PATH="dummy"
export PKCS11_PIN="dummy"
export KEY_SIZE=1024
export CA_EXPIRE=3650
export KEY_EXPIRE=3650

# These are the fields which will be placed in the certificate.
# Don't leave any of these fields blank. Update if you want
export KEY_COUNTRY="US"
export KEY_PROVINCE="CA"
export KEY_CITY="SanFrancisco"
export KEY_ORG="Fort-Funston"
export KEY_EMAIL="noreply@getlost.com"
export KEY_CN=changeme
export KEY_NAME=changeme
export KEY_OU=changeme
export PKCS11_MODULE_PATH=changeme
export PKCS11_PIN=1234
# END OF vars

. /etc/openvpn/easy-rsa/2.0/clean-all
. /etc/openvpn/easy-rsa/2.0/build-ca

# create the server key
. /etc/openvpn/easy-rsa/2.0/build-key-server server


# Create the client Key, update these if you want. The details MUST be slightly diff to server
export KEY_COUNTRY="US"
export KEY_PROVINCE="TX"
export KEY_CITY="Austin"
export KEY_ORG="The Alamo"
export KEY_EMAIL="noreply@getlost2.com"
export KEY_CN=changeme
export KEY_NAME=keyname
export KEY_OU=noidea
export PKCS11_MODULE_PATH=changeme
export PKCS11_PIN=1234
. /etc/openvpn/easy-rsa/2.0/build-key client1

# generate Deffie Hellman Parameters
. /etc/openvpn/easy-rsa/2.0/build-dh

# Move the keys we just generated to the directory that actually runs the openvpn service
cd /etc/openvpn/easy-rsa/2.0/keys
cp ca.crt ca.key client1.key client1.crt dh1024.pem server.crt server.key /etc/openvpn 


# Copy the sample server configuration file to the directory that will run it.
cd /usr/share/doc/openvpn/examples/sample-config-files
uncompress server.conf.gz
sudo cp server.conf /etc/openvpn/.
sudo cp client.conf /etc/openvpn/.


# Update the client.conf
SERVER_IP=`/sbin/ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'`
sed -i "s;remote my-server-1 1194;remote $SERVER_IP 1194;" /etc/openvpn/client.conf
sed -i "s;ca ca.crt;ca $CONFIG_FILE_PATH/ca.crt;" /etc/openvpn/client.conf
sed -i "s;cert client.crt;cert $CONFIG_FILE_PATH/client1.crt;" /etc/openvpn/client.conf
sed -i "s;key client.key;key $CONFIG_FILE_PATH/client1.key;" /etc/openvpn/client.conf

# Update the server.conf by uncommenting the redirect of gateway
sed -i 's:;push "redirect-gateway def1 bypass-dhcp":push "redirect-gateway def1 bypass-dhcp":' \
/etc/openvpn/server.conf

# Update the dhcp-option to push google as the DNS
sed -i 's:;push "dhcp-option DNS 208.67.220.220":push "dhcp-option DNS 8.8.8.8":' \
/etc/openvpn/server.conf

sed -i 's:;push "dhcp-option DNS 208.67.220.220":push "dhcp-option DNS 10.8.0.1":' \
/etc/openvpn/server.conf


# Set up packet forwarding.
sed -i "s;#net.ipv4.ip_forward=1;net.ipv4.ip_forward=1;" /etc/sysctl.conf
echo 1 > /proc/sys/net/ipv4/ip_forward

# Set up iptables to forward packets for vpn and do this upon startup.
echo 'iptables -A FORWARD -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -s 10.8.0.0/24 -j ACCEPT
iptables -A FORWARD -j REJECT
iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -o eth0 -j MASQUERADE
exit 0' > /etc/rc.local

# Call the startup script immediately so user does not have to reboot to get going.
sudo bash /etc/rc.local

# Package up the files we need into a tar for sending
mkdir /etc/openvpn/vpn-details

cp /etc/openvpn/client.conf \
/etc/openvpn/ca.crt \
/etc/openvpn/client1.crt \
/etc/openvpn/client1.key \
/etc/openvpn/vpn-details/

cd /etc/openvpn/
tar --create --gzip --file ~/vpn-details.tar.gz vpn-details

# clean up
sudo rm -rf /etc/openvpn/vpn-details
sudo rm /etc/openvpn/client.conf
service openvpn restart

echo 'Now move the "vpn-details.tar.gz" folder to your local computer and carry on from there.'
echo "You may want to reboot this server."