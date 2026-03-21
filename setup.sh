sudo apt update
sudo apt install python3-venv
git clone https://github.com/AvenIsHere/Fez.py
cd Fez || exit
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
touch .env