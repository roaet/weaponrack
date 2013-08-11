import sys


def main():
    if hasattr(sys, 'real_prefix'):
        print "0"
    else:
        print "1"
    sys.exit()


if __name__ == "__main__":
    main()
