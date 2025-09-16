# rm -rf adk/venv
# python3.12 -m venv adk/venv
# source adk/venv/bin/activate

sed -i 's/credsStore/credStore/g' ~/.docker/config.json
python3.12 -m pip install --upgrade pip
pip install --user -r adk/requirements.txt

