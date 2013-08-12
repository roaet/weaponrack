import errno
import getpass
import logging
import os
import shutil
import sys
import subprocess


LOG = logging.getLogger("snail." + __name__)


def check_super():
    return os.geteuid() == 0


def check_host(host):
    cmd = ("ping -c 1 %s" % host).split(" ")
    FNULL = open(os.devnull, 'w')
    response = subprocess.call(cmd, stdout=FNULL, stderr=subprocess.STDOUT)
    if response == 0:
        return True
    return False


def confirm_inova_login():
    cmd = ("inova-login -t").split(" ")
    response = subprocess.call(cmd)
    if response == 0:
        return True
    return False


def check_venv():
    return hasattr(sys, 'real_prefix')


def check_dir(directory):
    return os.path.exists(directory)


def check_file(file):
    try:
        with open(file):
            pass
    except IOError:
        return False
    return True


def check_basics(require_super=True, require_venv=True,
                 require_internet=True, require_vpn=True):
    if not require_super and check_super():
        LOG.error("This script should not be run as root")
        return False
    if require_super and not check_super():
        LOG.error("You need root privileges to run this script")
        return False
    if require_venv and not check_venv():
        LOG.error("You are not in a virtual environment. Please activate")
        return False
    if not require_venv and check_venv():
        LOG.error("You are in a virtual environment. Please deactivate")
        return False
    if require_internet:
        hosts_to_try = ["google.com", "yahoo.com", "microsoft.com"]
        did_ping = False
        for host in hosts_to_try:
            if check_host(host):
                did_ping = True
                break
        if not did_ping:
            LOG.error("It appears you are not connected to the internet. " +
                      "Please connect")
            return False
    if require_vpn and not check_host("github.rackspace.com"):
        LOG.error("Cannot reach internal network. Please connect")
        return False
    return True


def copy_file(src, dst):
    shutil.copyfile(src, dst)


def enter_virtualenv(path):
    target = "%s/bin/activate_this.py" % path
    execfile(target, dict(__file__=target))
    return check_venv()


def exit(status):
    sys.exit(status)


def get_home():
    return os.path.expanduser("~")


def get_confirmed_password(prompt):
    while True:
        pw = getpass.getpass(prompt + "[CTRL+D to cancel]: ")
        confirm = getpass.getpass("Confirm: ")
        if pw == confirm:
            return pw
        LOG.error("Password mismatch")


def clone_from_git_repo(repo, target_directory):
    cmd = ("git clone %s %s" % (repo, target_directory)).split(" ")
    response = subprocess.call(cmd)
    return response == 0


def install_git_package(package, name, branch="master",
                        with_sudo=False):
    sudo_str = ""
    if with_sudo:
        sudo_str = "sudo "
    git_root = "git+git://"
    package = "%s%s@%s#egg=%s" % (git_root, package, branch, name)
    cmd = ("%spip install %s" % (sudo_str, package)).split(" ")
    response = subprocess.call(cmd)
    return response == 0


def install_python_package(package, with_sudo=False):
    if type(package) == list:
        package = " ".join(package)
    sudo_str = ""
    if with_sudo:
        sudo_str = "sudo "
    cmd = ("%spip install --upgrade %s" % (sudo_str, package)).split(" ")
    response = subprocess.call(cmd)
    return response == 0


def install_system_package(package, with_sudo=True):
    sudo_str = ""
    if with_sudo:
        sudo_str = "sudo "
    cmd = ("%sapt-get install -y %s" % (sudo_str, package)).split(" ")
    response = subprocess.call(cmd)
    return response == 0


def install_virtual_env(prompt, location):
    cmd = ("virtualenv --prompt='%s' --distribute --no-site-packages %s" %
           (prompt, location)).split(" ")
    response = subprocess.call(cmd)
    return response == 0


def mkdir_p(path, error_if_exists=False):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            return not error_if_exists
        else:
            raise
    return True


def remove_dir(path):
    shutil.rmtree(path)


def remove_file(path):
    os.remove(path)
