colors = {
    "red":"\033[1;31m",
    "green":"\033[1;32m",
    "yellow":"\033[1;33m",
    "blue":"\033[1;34m",
    "purple":"\033[1;35m",
    "cyan":"\033[1;36m",
    "white":"\033[1;37m"
}


def cprint(color, text):
    print(colors[color] + text + "\033[0m")


def alert(text):
    print(colors["red"] + "[!] " + "\033[0m" + text)

def success(text):
    print(colors["green"] + "[+] " + "\033[0m" + text)

def info(text):
    print(colors["blue"] + "[*] " + "\033[0m" + text)

def warn(text):
    print(colors["yellow"] + "[*] " + "\033[0m" + text)

