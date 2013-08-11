import ConfigParser
import logging

import snail.common as common


LOG = logging.getLogger("snail." + __name__)
DEBUG = True
NO_INOVA = False
INSTALL_PATH = "%s/bin/snail" % common.get_home()


class AlreadyInstalledException(Exception):
    message = "Already installed"


class SnailInstaller(object):
    verbose = False
    noop = False
    no_inova = False

    def __init__(self, verbose=False, noop=False, no_inova=False):
        self.verbose = verbose
        self.noop = noop
        self.no_inova = no_inova
        self.install_path = INSTALL_PATH

    def abort(self):
        common.remove_dir(self.install_path)
        common.exit(1)

    def run(self, reinstall=False, refresh_conf=False):
        LOG.info("Installing snail _@/")
        if not common.check_basics(require_super=False, require_venv=False):
            common.exit(1)

        if not refresh_conf:
            self.install(reinstall)
        if not self.backup_existing_supernova_conf():
            exit(1)
        self.generate_supernova_conf()
        if not self.configure_keyring():
            if not DEBUG:
                self.abort()
        self.confirm_inovas()

    def confirm_inovas(self):
        LOG.info("Confirming inova-login credentials.")
        if not common.confirm_inova_login():
            LOG.error("failed?")

    def configure_keyring(self):
        LOG.info("Configuring keyring")
        sn_conf = "%s/.supernova" % common.get_home()
        if not common.check_file(sn_conf):
            LOG.error("No supernova conf found. Cannot configure")
            return False
        sn = ConfigParser.ConfigParser()
        sn.readfp(open(sn_conf))
        if not sn.has_section("snail"):
            LOG.error("Supernova conf isn't a snail conf: " +
                      "can't safely continue")
            return False
        venv_path = "%s/%s" % (self.install_path, ".venv")

        if not common.check_venv() and not common.enter_virtualenv(venv_path):
                LOG.error("Could not enter virtualenv")
                self.abort()

        snail_conf = "%s/snail.conf" % common.get_home()
        if not common.check_file(snail_conf):
            LOG.error("Could not locate snail.conf")
            self.abort()
        snail_config = ConfigParser.ConfigParser()
        snail_config.readfp(open(snail_conf))

        sso = common.get_confirmed_password("Enter your SSO")

        for section in sn.sections():
            if not sn.has_option(section, 'type'):
                continue
            pw_type = "prompt"
            if snail_config.has_section(section) and\
                    snail_config.has_option(section, 'pw_type'):
                pw_type = snail_config.get(section, 'pw_type')
            do_prompt = pw_type == "prompt"
            prompt_msg = "Please enter your password"
            for k, v in sn.items(section):
                if v == 'USE_KEYRING':
                    pw = pw_type
                    if pw_type == "sso":
                        pw = sso
                    if do_prompt:
                        try:
                            pw = common.get_confirmed_password(prompt_msg)
                        except EOFError:
                            LOG.error("Caught CTRL+D. Aborting")
                            if DEBUG:
                                exit(1)
                            self.abort()
                    common.pexpect_supernova(section, k, pw,
                                             verbose=self.verbose,
                                             noop=self.noop)

        common.pexpect_inovalogin(sso, verbose=self.verbose, noop=self.noop)
        return True

    def backup_existing_supernova_conf(self):
        sn_conf = "%s/.supernova" % common.get_home()
        sn_bak = sn_conf + ".bak"
        if not common.check_file(sn_conf):
            LOG.info("No pre-existing supernova conf found")
            return True
        #check if existing supernova conf is a snail conf
        conf_check = ConfigParser.ConfigParser()
        conf_check.readfp(open(sn_conf))
        if conf_check.has_section("snail"):
            """ No need to back up a snail config file."""
            return True
        if common.check_file(sn_bak):
            LOG.error("Backup already exists! Confirm with --overwrite")
            if not DEBUG:
                return False
        LOG.info("Backing up existing conf to %s" % sn_bak)
        common.copy_file(sn_conf, sn_bak)
        return True

    def install(self, reinstall=False):
        if common.check_dir(self.install_path):
            if not reinstall:
                raise AlreadyInstalledException()
            else:
                common.remove_dir(self.install_path)

        if not common.mkdir_p(self.install_path):
            LOG.error("Could not create installation path, %s" %
                      self.install_path)
            self.abort()

        if not common.install_system_package('curl git python-dev python-pip'):
            LOG.error("Could not install basic packages")
            self.abort()

        if not common.install_python_package('virtualenv', with_sudo=True):
            LOG.error("Could not install virtualenv")
            self.abort()

        venv_path = "%s/%s" % (self.install_path, ".venv")
        if not common.install_virtual_env("( _@/ )", venv_path):
            LOG.error("Could not create virtualenv")
            self.abort()

        if not common.enter_virtualenv(venv_path):
            LOG.error("Could not enter virtualenv")
            self.abort()

        packages = ['pip', 'distribute', 'eventlet', 'pexpect',
                    'rackspace-novaclient']
        if not common.install_python_package(packages):
            LOG.error("Could not install %s" % packages)
            self.abort()

        pkg = "github.com/openstack/python-novaclient.git"
        if not common.install_git_package(pkg, "python-novaclient"):
            LOG.error("Could not install %s" % pkg)
            self.abort()

        pkg = "github.com/emonty/rackspace-auth-openstack.git"
        if not common.install_git_package(pkg, "rackspace-auth-openstack"):
            LOG.error("Could not install %s" % pkg)
            self.abort()

        pkg = "github.com/roaet/supernova.git"
        if not common.install_git_package(pkg, "supernova"):
            LOG.error("Could not install %s" % pkg)
            self.abort()

        pkg = "github.rackspace.com/major-hayden/inova-login.git"
        if not common.install_git_package(pkg, "inova-login"):
            LOG.error("Could not install %s" % pkg)
            self.abort()

    def generate_supernova_conf(self):
        repo = "https://github.rackspace.com/just5245/weaponrack_secure.git"
        secure_dir = "%s/%s" % (self.install_path, "secure")
        if common.check_dir(secure_dir):
            common.remove_dir(secure_dir)
        if not common.clone_from_git_repo(repo, secure_dir):
            LOG.error("Could not clone %s" % repo)
            self.abort()

        seed_file = "%s/snail/supernova_seed.conf" % secure_dir
        remote_config = ConfigParser.ConfigParser()
        remote_config.readfp(open(seed_file))

        snail_conf = "%s/snail.conf" % common.get_home()
        if not common.check_file(snail_conf):
            LOG.error("Could not locate snail.conf")
            self.abort()
        snail_config = ConfigParser.ConfigParser()
        snail_config.readfp(open(snail_conf))

        inovas = {}
        supernovas = {}
        inova_template = None
        sn_template = None

        config_list = [remote_config, snail_config]
        ignored_keys = ['pw_type']
        for config in config_list:
            sections = config.sections()
            for section in sections:
                td = {}
                for k, v in config.items(section):
                    if k in ignored_keys:
                        continue
                    td[k] = v
                if section == 'inova-template':
                    inova_template = td
                    continue
                elif section == 'supernova-template':
                    sn_template = td
                    continue
                if not config.has_option(section, 'type'):
                    continue
                type = config.get(section, 'type')
                if type == 'inova':
                    if section in inovas:
                        inovas[section].update(td)
                    else:
                        inovas[section] = td
                elif type == 'supernova':
                    if section in supernovas:
                        supernovas[section].update(td)
                    else:
                        supernovas[section] = td

        if not inova_template or not sn_template:
            LOG.error("Could not find inova or supernova template anywhere")
            common.self.abort()

        out_file = "%s/snail/supernova_out.conf" % secure_dir
        if common.check_file(out_file):
            common.remove_file(out_file)
        out_config = ConfigParser.ConfigParser()
        out_config.add_section("snail")
        out_config.set("snail", "version", "0.1")

        out_list = [(inovas, inova_template), (supernovas, sn_template)]
        for listing, template in out_list:
            for title, items in listing.items():
                out_config.add_section(title)
                for template_key, template_value in template.items():
                    src = template_value.lower()
                    value = template_value
                    if src == 'title':
                        value = title
                    if src in items:
                        value = items[template_value.lower()]
                    if template_key.lower() in items:
                        value = items[template_key.lower()]
                    out_config.set(title, template_key.upper(), value)

                for template_key, template_value in template.items():
                    src = template_value.lower()
                    if src in items:
                        del items[template_value.lower()]

                for item_key, item_value in items.items():
                    if not out_config.has_option(title, item_key):
                        out_config.set(title, item_key, item_value)
        out_config.write(open(out_file, 'w+'))
        sn_conf = "%s/.supernova" % common.get_home()
        common.copy_file(out_file, sn_conf)