#!/usr/bin/env python
import logging
import optparse
import sys

import snail.installer as install
import snail.snail_common as scommon


LOG = logging.getLogger("snail")
LOG.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(log_format)

ch.setFormatter(formatter)
LOG.addHandler(ch)


def main():
    parser = optparse.OptionParser()
    parser.add_option("--reinstall", action="store_true", dest="reinstall",
                      help="reinstall snail if previously installed")
    parser.add_option("-v", "--verbose", action="store_true",
                      dest="verbose",
                      help="output all available information")
    parser.add_option("--refresh_conf", action="store_true", dest="refresh",
                      help="just refresh conf and do not attempt to install")
    (options, args) = parser.parse_args()

    LOG.info(scommon.get_snail_title())
    installer = install.SnailInstaller(verbose=True)
    try:
        installer.run()
    except install.AlreadyInstalledException:
        LOG.error("snail already exists, please run with --reinstall")
        sys.exit(1)


if __name__ == "__main__":
    main()
