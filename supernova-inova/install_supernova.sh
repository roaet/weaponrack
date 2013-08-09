#!/bin/bash

# this script will install supernova in a virtual environment
# called supernova

# it will only need superuser rights to ensure that virtualenv
# is installed

if [[ $UID -eq 0 ]]; then
    echo "$0 must not be run as root"
    exit 1
fi
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
in_venv=`python $DIR/check_venv.py`
if [ "$in_venv" = "0" ]; then
    echo "Within virtualenv. Execute deactivate first. Kthx"
    echo "Example:"
    echo ""
    echo "$ deactivate"
    exit 1
fi
# check for  existing supernovas
if [ -d ~/bin/supernova ]; then
    echo "supernova already installed, please uninstall first"
    exit 1
fi
# Begin super user sections
sudo apt-get install curl git python-dev python-pip
sudo pip install virtualenv

# Remove existing supernovas
if [ -d ~/bin/supernova ]; then
    rm -rf ~/bin/supernova
fi

# Install the supernovas
mkdir -p ~/bin/supernova
cd ~/bin/supernova
virtualenv --prompt="(SUPERNOVA)" .venv
source .venv/bin/activate
pip install --upgrade distribute
# following the directions from:
# https://one.rackspace.com/display/NOVA/Accessing+Nova+Environments
pip install rackspace-novaclient
git clone https://github.com/openstack/python-novaclient.git
cd python-novaclient
python setup.py install
cd ~/bin/supernova

git clone https://github.com/emonty/rackspace-auth-openstack.git
cd rackspace-auth-openstack
python setup.py install
cd ~/bin/supernova

pip install keyring
git clone https://github.com/roaet/supernova.git
cd supernova
python setup.py install
cd ~/bin/supernova

if [ "$(ping -q -c1 github.rackspace.com)" ];then
    pip install keyring eventlet pexpect
    git clone https://github.rackspace.com/major-hayden/inova-login.git
    cd inova-login
    python setup.py install
    cd ~/bin/supernova
else
    echo "Skipping inova-login, internal not reachable"
fi

deactivate

echo "Everything seems fine"
echo ""
echo "Btw, you're going to need to setup all of the keyrings if you"
echo "havn't done that yet."

echo "Examples of this are:"
echo ""
echo "supernova-keyring --set production NOVA_API_KEY"
echo "or"
echo "supernova-keyring --set global NOVA_API_KEY"
echo ""
echo "or you can just use ./config_supernova_keyrings.sh"
echo ""
echo "You can list what things you're going to have to set by running:"
echo ""
echo "supernova -l"
echo ""
echo "And then looking for things that say USE_KEYRING"
echo ""
echo "Have fun :)"

exit 0
