snail toolkit
=============

snail is a wrapper for supernova and inova-login. You must be connected to
the internal network for this installer to work.

You can check this by attempting to ping an internal address.

What does it do?
----------------

snail will generate a special supernova configuration file that allows it to
manage the authentication information. 

Requirements
------------

Snail requires at least the following is installed on your system:

1. Distribute 

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

It is necessary to have in your user home a snail.conf file. This file
will provide snail the information to generate your proper credentials for all
environments. This file also maintains the references to the remote
repositories that will be needed to gather template files.

The command line option of --refresh will allow you to reload the credentials
and add new endpoints/targets if necessary.

Example snail.conf configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You will notice that a lot of information, such as endpoint URLs and other
things aren't listed below. A lot of those details are stored in a remote repo
and are brought in by the installer.

Custom endpoints are possible if necessary by adding an endpoint options.

The snail configuration file follows the INI format::

  #everything in this section is absolutely required
  [snail]
  inova_repo = github.moonbase.com/moonuser/inova-login.git
  template_repo = https://github.moonbase.com/moonuser/weaponrack_secure.git
  inova_user = moonuser

  [inova-moonbase]
  #inova is a special type that is required for inova connection
  #type is always required
  type = inova
  user = moonuser
  #sso is a special pw_type that will reuse a master pw prompted during install
  #pw_type is always required
  pw_type = sso

  [inova-moonbase2]
  type = inova
  user = moonuser
  #prompt is a special pw_type that will force the user to prompt for a pw
  pw_type = prompt

  [moonbase-cloud]
  #supernova is a special type that is required for supernova connections
  type = supernova
  user = moonuser
  #tenant is properly substituted during generation for application options
  tenant = 123456
  #if pw_type is neither sso, or prompt, it will use it as a pw, as this API
  #key shows below
  pw_type = 123456789abcdef123456789abcdef00

  [moonbase2-cloud]
  type = supernova
  #custom endpoints, can be specified this way
  endpoint = https://identity.api.mooncloud.com/v2.0
  region = MOON
  user = moonuser
  tenant = 123456
  pw_type = 123456789abcdef123456789abcdef00
  #any configuration things applicable to supernova will be applied if added
  #here

A summary of the above annotations follows:

1. the snail section and all options in it are required
2. type is always required
3. inova is a special type that is required for inova connection
4. supernova is a special type that is required for supernova connection
5. pw_type is always required
6. sso is a special pw_type that will reuse a prompted password during install
7. prompt is a special pw_type that will prompt for a password during install
8. if pw_type is neither sso or prompt, it will use the value
9. tenant will be used appropriately
10. any additional options will be passed to the generated supernova conf
