# Fez
Fez and TransBot Discord bots for the Transpeak Discord server.

Fez: In `/Fez`, entry point: `Fez/main.py`

TransBot: In `/TransBot`, entry point: `TransBot/main.py`

## Setup

### Windows
Windows users should use WSL and follow the instructions for Linux.

### Linux

A setup.sh script is provided for convenience, however it will only work on Debian-based distros. You will still need to provide your own bot tokens.   

1. Install system dependencies

These commands are for Debian-based distros. Other distro users (Fedora, Arch, etc.) should check their distro's package manager
```shell
sudo apt update
sudo apt install python3-venv
```
2. Clone the repo
```shell
git clone https://github.com/AvenIsHere/Fez.git
cd Fez
```
3. Set up venv
```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
4. Create a `.env` file and add bot tokens
```dotenv
FEZ_TOKEN= [Fez's token]
TBOT_TOKEN= [TransBot's token]
```
5. Run it
* Fez
```shell
python Fez/main.py
```
* TransBot
```shell
python TransBot/main.py
```
6. Hell yeah