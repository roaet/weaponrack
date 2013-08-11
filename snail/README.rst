supernova-inova-login toolkit
=============================

If you intend on using inova-login ensure that you are connected to the
internal network somehow.

You can check this by attempting to ping an internal address.

Steps to install this toolkit
-----------------------------

1. Ensure you're connected to an internal network
2. Run install_supernova.sh
3. Edit the file config_supernova_keyrings.sh

   a. Add environments to the sn_environments on line 2 if needed
   b. Add environments to the il_environments on line 3 if needed
   c. Change the value of configured to 1 from 0

7. Prepare your API keys and SSO for entry and/or copy/paste
8. Enter the virtual environment by running: source
   ~/bin/supernova/.venv/bin/activate
9. Run config_supernova_keyrings.sh

To uninstall this toolkit
-------------------------

1. Ensure you're not in the virtual environment
2. Run uninstall_supernova.sh

To upgrade this toolkit
-----------------------

1. uninstall then reinstall, but you can skip the credentials step
