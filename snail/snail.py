#!/usr/bin/env python
import logging
import sys

import snail.installer as install


LOG = logging.getLogger("snail")
LOG.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(log_format)

ch.setFormatter(formatter)
LOG.addHandler(ch)


def main():
    LOG.info(
        "\n                      _____" +
        "\n supernova          .'     `." +
        "\n    and            /  .-=-.  \   \ __" +
        "\ninova-login        | (  C\ \  \_.'')" +
        "\n                  _\  `--' |,'   _/" +
        "\nBy: weaponrack   /__`.____.'__.-'")
    installer = install.SnailInstaller(verbose=True)
    try:
        installer.run()
    except install.AlreadyInstalledException:
        LOG.error("snail already exists, please run with --reinstall")
        sys.exit(1)


if __name__ == "__main__":
    main()
