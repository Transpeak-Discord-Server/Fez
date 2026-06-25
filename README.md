# Fez
Fez and TransBot Discord bots for the Transpeak Discord server.

## Setup

### Windows

Windows users should use WSL and follow the instructions for Linux.

### Linux

1. Install system dependencies

(Debian-based distros)
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
FEZ_TOKEN= # Fez's token
TBOT_TOKEN= # TransBot's token
```
5. Create the `private` folder and add all private files to it

See Private Files below for the required files

6. Run it

   (from the project root)
* Fez
```shell
python -m Fez.main
```
* TransBot
```shell
python -m TransBot.main
```
7. Hell yeah

## Private Files

```tree
private
└── images
    ├── ash_staff_command.gif
    └── luna_staff_command.png
```