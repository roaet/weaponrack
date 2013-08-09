#!/bin/bash

#this script will uninstall the supernova installed using the 
# paired installer

if [[ $UID -eq 0 ]]; then
    echo "$0 must not be run as root"
    exit 1
fi

# Remove existing supernovas
if [ ! -d ~/bin/supernova ]; then
    echo "supernova not found"
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
rm -rf ~/bin/supernova
echo "Supernova uninstalled"
exit 0
