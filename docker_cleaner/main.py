import argparse
import logging

import logger
from auto_cleaner import AutoCleaner


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--force", dest="force",
    default=[], nargs='+', choices=["image", "volume", "all"],
    help="Force removing.")
parser.add_argument("-v", "--client-version", dest="version",
    default="auto", help="Version of docker client to use")
parser.add_argument("-o", "--older", dest="older",
    default=0,
    help="Clear resources that older amount of time (in minutes)")
parser.add_argument("--images-include", dest="images_include",
    nargs='+',
    default=[""],
    help="Filter images that only contains any of that names")
parser.add_argument("--volumes-include", dest="volumes_include",
    nargs='+',
    default=[""],
    help="Filter volumes that only contains any of that name")
parser.add_argument("--images-exclude", dest="images_exclude",
    nargs='+',
    default=[],
    help="Exclude images that contains any of that names")
parser.add_argument("--volumes-exclude", dest="volumes_exclude",
    nargs='+',
    default=[],
    help="Exclude volumes that contains any of that name")
parser.add_argument("-t", "--timeout", dest="timeout",
    default=None, help="Timeout of cleaning. "\
    "Live it empty in case of using cron job.")
parser.add_argument("-l", "--log", dest="log",
    help="Redirect logging to file")
args = parser.parse_args()

if args.log is not None:
    log = logging.getLogger(__name__)
    log.addHandler(logger.FileHandler(args.log))
    log.setLevel(logging.DEBUG)
else:
    log = logging.getLogger(__name__)
    log.addHandler(logger.StreamHandler())
    log.setLevel(logging.DEBUG)


def main():
    try:
        ac = AutoCleaner(timeout=args.timeout,
                         force=args.force,
                         version=args.version,
                         oldest=args.older,
                         images_include=args.images_include,
                         volumes_include=args.volumes_include,
                         images_exclude=args.images_exclude,
                         volumes_exclude=args.volumes_exclude,
                         filelog=args.log)
        ac.clean()

    except KeyboardInterrupt:
        print('\nThe process was interrupted by the user')
        raise SystemExit

if __name__ == "__main__":
    main()

