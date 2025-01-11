from tronpy import Tron
from tronpy.keys import PrivateKey
import requests
import time
import os
from datetime import datetime

colors = {
    "red": '\033[00;31m',
    "green": '\033[00;32m',
    "light_green": '\033[01;32m',
    "yellow": '\033[01;33m',
    "light_red": '\033[01;31m',
    "blue": '\033[00;34m',
    "purple": '\033[01;35m',
    "cyan": '\033[00;36m',
    "gray": '\033[90m',
    "highlight": '\033[38;5;130m',
    "white": "\033[37m"
}

os.system("cls" if os.name == "nt" else "clear")

def print_header():
    print(f"""
{colors['red']}888    888                                     {colors['yellow']}8888888b.           888    
{colors['red']}888    888                                     {colors['yellow']}888   Y88b          888    
{colors['red']}888    888                                     {colors['yellow']}888    888          888    
{colors['red']}8888888888  .d88b.  88888b.   .d88b.  888  888 {colors['yellow']}888   d88P  .d88b.  888888 
{colors['red']}888    888 d88""88b 888 "88b d8P  Y8b 888  888 {colors['yellow']}8888888P"  d88""88b 888    
{colors['red']}888    888 888  888 888  888 88888888 888  888 {colors['yellow']}888        888  888 888    
{colors['red']}888    888 Y88..88P 888  888 Y8b.     Y88b 888 {colors['yellow']}888        Y88..88P Y88b.  
{colors['red']}888    888  "Y88P"  888  888  "Y8888   "Y88888 {colors['yellow']}888         "Y88P"   "Y888 {colors['red']}
                                           888                            
                                      Y8b d88P                            
                                       "Y88P"  

            {colors['blue']}HoneyPot Wallet V1                           
""")

def get_input(prompt):
    return input(f'{colors["red"]}[{colors["green"]}+{colors["red"]}] {colors["light_green"]}{prompt}{colors["highlight"]}')

def get_tron_balance(wallet_address):
    response = requests.get(f"https://api.trongrid.io/v1/accounts/{wallet_address}")
    if response.status_code == 200:
        try:
            return response.json()['data'][0]['balance'] / 1_000_000
        except IndexError:
            exit(f"{colors['red']}Your inventory is empty!")
    print(f"{colors['red']}Error to get Balance")
    return None

def display_time():
    return datetime.now().strftime("%H:%M:%S")

def send_tron(client, from_address, to_address, amount, private_key):
    priv_key = PrivateKey(bytes.fromhex(private_key))
    try:
        tx = client.trx.transfer(from_address, to_address, amount).build().sign(priv_key)
        result = tx.broadcast()
        return result
    except Exception as e:
        print(f"{colors['red']}Error: {e}")
        return None

print_header()
hwallet = get_input("Enter the Honeypot wallet address: ")
pwallet = get_input("Enter the private key of Honeypot wallet: ")
uwallet = get_input("Enter your main wallet address: ")

while True:
    balance = get_tron_balance(hwallet)
    if balance is not None:
        balance = int(balance) - 1
        if balance > 1:
            balance *= 1_000_000
            print(f"{colors['white']}[{colors['yellow']}{display_time()}{colors['white']}] {colors['light_green']}Number tron received: {colors['green']}{balance / 1_000_000} {colors['green']}TRX")
            client = Tron()
            result = send_tron(client, hwallet, uwallet, balance, pwallet)
            if result and result['result']:
                print(f"\n{colors['cyan']}+++++++++++++++++++++++++++++++++++++++++++++++\n{colors['red']}[{colors['light_green']}{display_time()}{colors['red']}] {colors['green']}Sending {colors['yellow']}{balance / 1_000_000}{colors['green']} To {colors['yellow']}{uwallet}\n{colors['red']}[ {colors['yellow']}*{colors['red']} ] {colors['green']}TXID: {colors['yellow']}{result['txid']}\n{colors['cyan']}+++++++++++++++++++++++++++++++++++++++++++++++\n")
            else:
                print(f"{colors['red']}Error sending.")
        else:
            print(f'{colors['white']}[{colors['yellow']}{display_time()}{colors['white']}] {colors['yellow']}Balance: {colors['red']}0')
    time.sleep(2)