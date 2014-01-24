echo "Installing Building Rules Backend!"
echo "First of all, removing old installation..."
./uninstall.sh
echo "Now installing it..."
mkdir venv
virtualenv venv
source venv/bin/activate
pip install flask==0.9
pip install MySQL-python
pip install requests

wget http://www.alessandronacci.com/repo/BuildingRulesInstaller/z3-x64-ubuntu-12.04.zip
unzip z3-x64-ubuntu-12.04.zip -d tools/z3
rm z3-x64-ubuntu-12.04.zip
mv tools/z3/z3-4.3.2.a5335270042c-x64-ubuntu-12.04 tools/z3/z3
rm -r tools/z3/__MACOSX
