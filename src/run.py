import argparse

from classes.test import api_test


def get_args():
    parser = argparse.ArgumentParser('python src/run.py')
    parser.add_argument('--test', dest='test', action='store_const', const=True, default=False,
                        help='perform system test')

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()

    if args.test:
        api_test()
