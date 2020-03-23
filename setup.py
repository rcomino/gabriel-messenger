"""GameManager setup file."""

import argparse
import logging

from src.application.application import Application
from src.services.common.enums.environment import Environment
from src.infrastructure.configuration.configuration import Configuration


def parse_args():
    """Parse arguments from initial call."""
    parser = argparse.ArgumentParser(description='Publish publications and news to social networks.')
    parser.add_argument(
        '--environment',
        dest='environment',
        nargs='?',
        type=Environment,
        choices=Environment.__members__.values(),
        help="Force environment. If you do not set this option, environment value from config.yaml will be loaded.")

    parser.add_argument(
        '--global-logging-level',
        dest='global_logging_level',
        nargs='?',
        type=str,
        choices=logging._nameToLevel.keys(),  # pylint: disable=protected-access
        help="Force global logging level. If you do not set this option, global logging level value from config.yaml "
        "will be loaded.")

    parser.add_argument(
        '--app-logging-level',
        dest='app_logging_level',
        nargs='?',
        type=str,
        choices=logging._nameToLevel.keys(),  # pylint: disable=protected-access
        help="Force app logging level. If you do not set this option, app logging level value from config.yaml "
        "will be loaded.")

    return vars(parser.parse_args())


def run():
    """Run App."""
    configuration = Configuration(**parse_args())
    logging.basicConfig(level=configuration.get_global_configuration()['global_logging_level'],
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    app = Application(configuration=configuration)
    app.run()


if __name__ == '__main__':
    run()
