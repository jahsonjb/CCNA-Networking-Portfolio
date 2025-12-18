from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "192.168.0.133",
    "username": "admin",
    "password": "cisco123",
    "secret": "enablepassword",
}

net_connect = ConnectHandler(**device)
net_connect.enable()
output = net_connect.send_command("show ip int brief")
print(output)
net_connect.disconnect()
