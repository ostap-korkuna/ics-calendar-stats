import argparse
import logging
import time

from calendar_stats import CalendarStats
from stats_config import StatsConfig


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--file', dest='file', default=None, required=True,
                        help='Input ics file')
    parser.add_argument('-c', '--config', dest='config', default='config_example.json', required=False,
                        help='Config for stats tracking')
    parser.add_argument("--date-range", nargs="+", default=[],
                        help='Date range to filter')
    parser.add_argument('-v', '--verbose', action='store_true',
                        dest='verbose', default=None, required=False,
                        help='Verbose logging')
    parser.add_argument('--csv', action='store_true',
                        dest='csv', default=False, required=False,
                        help='Export summary in csv')
    parser.add_argument('--weekly', action='store_true',
                        dest='weekly', default=False, required=False,
                        help='In CSV export weekly statistics instead of daily')
    parser.add_argument('--hours', action='store_true',
                        dest='hours', default=False, required=False,
                        help='In CSV export data in hours instead of minutes')

    args = parser.parse_args()

    return args


def init_logging(args):
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        level=logging.INFO if not args.verbose else logging.DEBUG)


if __name__ == '__main__':
    start_time = time.time()
    args = parse_args()
    init_logging(args)
    logging.debug("Parsed cmd line args: " + str(args))

    config = StatsConfig(args.config)

    stats = CalendarStats(args)
    stats.run(config)

    end_time = time.time()
    logging.debug('The script took {} seconds'.format(int(end_time - start_time)))

