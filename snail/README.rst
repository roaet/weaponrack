snail toolkit
=============

snail is a wrapper for supernova and inova-login. You must be connected to
the internal network for this installer to work.

You can check this by attempting to ping an internal address.

How to use
----------

snail installed by default in ~/bin/snail. To use it you must:

1. activate the virtualenv [ source ~/bin/snail/.venv/bin/activate ]
2. execute your supernova or inova-login of choice:

   a. supernova <options>
   b. inova-login -e <environment> <options>

How to install
--------------
Usage: snail_installer [options]                                 
                                                                 
Options:                                                         
  -h, --help     show this help message and exit                 
  --overwrite    DANGER: overwrite preexisting supernova backup  
  --reinstall    reinstall snail if previously installed         
  --refresh      just refresh conf and do not attempt to install 
  --uninstall    remove snail install except system packages     
  -v, --verbose  output all available information                
