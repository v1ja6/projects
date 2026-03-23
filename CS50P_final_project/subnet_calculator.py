import re
import sys
import socket


class Subnet_calc:
    def __init__(self, ip_addr, subnet_cidr, prefix):
        self.ip_addr = ip_addr
        self.subnet_cidr = subnet_cidr
        self.preifx = prefix

    def ip_class(self):
        first_octet = int(self.ip_addr.split(".")[0])

        if 1 <= first_octet <= 127:
            return "\nClass A"

        elif 128 <= first_octet <= 191:
            return "\nClass B"

        elif 192 <= first_octet <= 223:
            return "\nClass C"

        elif 224 <= first_octet <= 239:
            return "\nClass D (Multicast)"

        elif 240 <= first_octet <= 255:
            return "\nClass F (Experimental)"

    def num_hosts(self):
        subnet = int(self.subnet_cidr.replace("/", ""))
        host_bits = 32 - subnet
        total = pow(2,host_bits)
        usable = total - 2

        return f"""Total number of Hosts: {total}
Total number of usable Hosts: {usable}"""

    def ip_to_binary(self):
        octets = self.ip_addr.split(".")
        binary_octets = []
        for octet in octets:
            int_octet = int(octet)
            binary = bin(int_octet)[2:].zfill(8)
            binary_octets.append(binary)
        binary_ip = ".".join(binary_octets)
        return binary_ip


    def binary_to_ip(self, binary_str):
        octets = []

        for i in range(0, 32, 8):
            octets.append(str(int(binary_str[i:i+8], 2)))
        return ".".join(octets)

    def subnet_mask(self):
        cidr = int(self.subnet_cidr.replace("/", ""))
        binary = "1" * cidr + "0" * (32 - cidr)

        octets = []
        for i in range(0, 32, 8):
            octets.append(binary[i:i+8])

        mask = ".".join(octets)
        return f"Subnet mask is: {mask}"


    def ip_to_binary_raw(self):
        octets = self.ip_addr.split(".")
        binary_octets = [bin(int(octet))[2:].zfill(8) for octet in octets]
        return "".join(binary_octets)

    def ip_range(self):
        ip_bin = self.ip_to_binary_raw()
        net_bits = int(self.subnet_cidr.replace("/", ""))
        host_bits = 32 - net_bits

        network_bin = ip_bin[:net_bits] + "0" * host_bits
        network_ip = self.binary_to_ip(network_bin)


        broadcast_bin = ip_bin[:net_bits] + "1" * host_bits
        broadcast_ip = self.binary_to_ip(broadcast_bin)


        first_ip_bin = bin(int(network_bin, 2) + 1)[2:].zfill(32)
        first_ip = self.binary_to_ip(first_ip_bin)


        last_ip_bin = bin(int(broadcast_bin, 2) - 1)[2:].zfill(32)
        last_ip = self.binary_to_ip(last_ip_bin)

        return f"""Network Address: {network_ip},
Broadcast Address: {broadcast_ip},
Usable Range: {first_ip}-{last_ip}"""



def main():
    Intro = "Welcome to the IPv4 subnet machine!"
    print(Intro.strip())

    option_checker()



def option_checker():
    try:
        while True:
            option = input("""
Great! Now choose from the following options:
1. Reverse DNS Lookup (PTR Record)
2. DNS Lookup (A Record)
3. Subnet Calculator
>>> """)


            if option == "1":
                ip = ip_getter()
                ans = reverse_dns_lookup(ip)
                menu = input(f"""\nThe name is: {ans}
If you would like to go to main menu press any key. If you would like to quit press [CTRL] + C\n""")
                if menu:
                    continue

            elif option == "2":
                ans = dns_lookup()
                menu = input(f"""\nThe IP is: {ans}
If you would like to go to main menu press any key. If you would like to quit press [CTRL] + C\n""")
                if menu:
                    continue

            elif option == "3":
                ip = ip_getter()
                subnet = subnet_getter()
                ip_prefix = ip + subnet
                calc = Subnet_calc(ip, subnet, ip_prefix)
                print(calc.ip_class())
                print(calc.num_hosts())
                print(f"Binary version of this IPv4 address is: {calc.ip_to_binary()}")
                print(calc.subnet_mask())
                print(calc.ip_range())

                menu = input("\nIf you would like to go to main menu press any key. If you would like to quit press [CTRL] + C\n")
                if menu:
                    continue


            else:
                print("Please choose from one of the following options!")

    except KeyboardInterrupt:
        sys.exit("\nQuitting...")

def ip_getter():
    try:
        while True:
            ip_addr = input("Insert IP Address here (Format: xxx.xxx.xxx.xxx) >>> ")
            ip_validate = ip_addr_check(ip_addr)
            if ip_validate:
                return ip_addr
                break
            else:
                print(f"IP address: {ip_addr} is not valid.")
    except KeyboardInterrupt:
        sys.exit("\nQuitting...")

def ip_addr_check(ip):
    pattern = r"^([1-9]?[0-9]?[0-9])\.([1-9]?[0-9]?[0-9])\.([1-9]?[0-9]?[0-9])\.([1-9]?[0-9]?[0-9])$"
    check = re.search(pattern, ip)

    if check:
        if int(check.group(1)) > 255 or int(check.group(2)) > 255 or int(check.group(3)) > 255 or int(check.group(4)) > 255 or int(check.group(1)) == 0:
            return False
        else:
            return True
    else:
        return False


def subnet_getter():
    try:
        while True:
            subnet = input("Insert subnet here (Format: /xx)>>> ")
            subnet_validate = subnet_checker(subnet)

            if subnet_validate:
                return subnet
                break
            else:
                print(f"Subnet: {subnet} is not valid")
                continue

    except KeyboardInterrupt:
        sys.exit("\nQuitting...")


def subnet_checker(sub):
    pattern = r"^/([1-3]?[0-9])$"
    check = re.search(pattern, sub)

    if check:
        if int(check.group(1)) > 32 or int(check.group(1)) < 1:
            return False
        else:
            return True

    else:
        return False


def reverse_dns_lookup(ip):
    name, alias, ip_addr = socket.gethostbyaddr(ip)
    return name


def dns_lookup():
    while True:
        try:
            host = input("Please input host name >>> ")
            port = input("Please input port >>> ")
            result = list( map( lambda x: x[4][0], socket.getaddrinfo(host,port,type=socket.SOCK_STREAM)))
            return result[0]
            break

        except (socket.gaierror):
            print("Invalid host or port")
            continue

if __name__ == "__main__":
    main()
