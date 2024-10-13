#! bash
echo -e "\n\nRemoving old dependencies...\n";
deactivate;
rm -rf .ven;

echo -e "\n\nInstalling dependencies...\n";
python3 -m venv .venv;
source .venv/Scripts/activate;
python.exe -m pip install --upgrade pip;

pip install -q mediapipe;
pip install opencv-python;

echo -e "\n\nAll dependencies are installed.\nYou can now run the app by running 'python main.py'.\n\n";
# pip install mediapipe opencv-python pyinstaller;
