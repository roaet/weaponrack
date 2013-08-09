#!/bin/bash
sn_environments=("preprodord" "netdev")
il_environments=("inova-iad" "inova-ord" "inova-dfw" "inova-lon" "inova-syd")
configured=0

if [ $UID -eq 0 ]; then
    echo "$0 must not be run as root"
    exit 1
fi

if [ $configured -eq 0 ]; then
    echo "This needs to be configured. Edit this file $0 and change the"
    echo "sn_environments and il_environments accordingly"
fi

# Ensure supernova is installed OUR way
if [ ! -d ~/bin/supernova ]; then
    echo "supernova not found. run install_supernova.sh first"
    exit 1
fi

in_venv=`python ~/bin/check_venv.py`
if [ "$in_venv" = "1" ]; then
    echo "Not within virtualenv. Source activate first. Kthx"
    exit 1
fi
echo "A series of prompts will follow that will ask for information"
echo "You need to do this for every USE_KEYRING in your .supernova config file"
echo "If you are missing some environments you will need to edit this file and"
echo "add them"
echo ""
echo ""
echo "Will now ask for you to enter your API key for multiple environments"
echo "These prompts apply to nova credentials"

echo "Looping through the list of environments, CTRL+D if you do not have it:"
for e in "${sn_environments[@]}"; do
    echo "key: <enter $e API key>"
    supernova-keyring --set $e OS_PASSWORD
done
echo "Will now ask for you to enter your SSO for multiple environments"
echo "These prompts apply to inova-login credentials"
echo ""
for e in "${il_environments[@]}"; do
    echo "key: <enter SSO for $e inova-login>"
    supernova-keyring --set $e NOVA_API_KEY
done

echo "Will now ask for you SSO for inova-login's SSH, one more time!"
echo "SSO:"
inova-login -s

echo "Running the login test to see if the install worked"
echo "If you see any failures feel free to re-run this program and try again"
echo "Most failures are typos or mis-types"
inova-login -t

echo "Finished. Re-run if the login-tests failed"
exit 0
