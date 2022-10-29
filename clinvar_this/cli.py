"""Console script for ClinVar This!"""
import argparse
import json
import logging
import sys

import logzero
from logzero import logger


def main(argv=None):
    """Console script for clinvar_this."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--verbose", action="store_true", default=False, help="Enable more verbose output"
    )
    args = parser.parse_args(argv)

    # Setup logging verbosity.
    if args.verbose:
        level = logging.DEBUG
    else:
        formatter = logzero.LogFormatter(
            fmt="%(color)s[%(levelname)1.1s %(asctime)s]%(end_color)s %(message)s"
        )
        logzero.formatter(formatter)
        level = logging.INFO
    logzero.loglevel(level=level)

    logger.info("args = %s", json.dumps(vars(args), indent=2))

    logger.info("All done, have a nice day!")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
