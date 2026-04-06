# Fez
Fez and TransBot Discord bots for the Transpeak Discord server.

## Setup

### Windows
Windows users should use WSL and follow the instructions for Linux.

### Linux

There is a `setup.sh` script that will set up the project for you. You will still need to add the bot tokens to `.env` and populate the `assets` folder. The script only works on Debian-based distros.   

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
FEZ_TOKEN= [Fez's token]
TBOT_TOKEN= [TransBot's token]
```
5. Create and add all the files to the `assets` folder

See "Private Files" for files that need to be added

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

```
assets
└── images
    ├── ash_staff_command.gif
    └── luna_staff_command.png
```