import logging
import pexpect
import sys

LOG = logging.getLogger("snail." + __name__)


def get_snail_title():
    snail = (
        "\n     _____" +
        "\n   .'     `.            supernova and inova-login" +
        "\n  /  .-=-.  \   \ __" +
        "\n  | (  C\ \  \_.'')     a weaponrack production" +
        "\n _\  `--' |,'   _/" +
        "\n/__`.____.'__.-'")
    return snail


def pexpect_supernova(env, parameter, password, verbose=False, noop=False):
    cmd = 'supernova-keyring -s %s %s' % (env, parameter)
    child = pexpect.spawn(cmd)
    if verbose:
        child.logfile = sys.stdout
    child.expect('.*abort: ')
    if noop:
        LOG.info('Would send %s' % password)
        child.sendcontrol('d')
    else:
        child.sendline(password)
    child.expect("\n")
    child.expect("\n")


def pexpect_inovalogin(password, verbose=False, noop=False):
    cmd = 'inova-login -s'
    child = pexpect.spawn(cmd)
    if verbose:
        child.logfile = sys.stdout
    child.expect('Password:*')
    if noop:
        LOG.info('Would send %s' % password)
        child.sendcontrol('d')
    else:
        child.sendline(password)
