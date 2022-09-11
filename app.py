import argparse

from data_collectors.async_data_collector import AsyncDataCollector
from data_collectors.sync_data_collector import SyncDataCollector


def run_parser(parser_type: str, page_from: int, page_to: int, save_to: str):
    parser_choices = {"sync": SyncDataCollector,
                      "async": AsyncDataCollector}
    return parser_choices[parser_type](page_from, page_to,
                                       save_to)


def main():
    parser = argparse.ArgumentParser(description="Parser app")
    parser.add_argument('page_from', default=1, type=int,
                        help="Specify the site page to start parsing")
    parser.add_argument('page_to', default=2, type=int,
                        help="Specify the site page to start parsing")
    parser.add_argument('save_to', choices=['postgres', 'google_sheets'],
                        default='postgres',
                        help="Specify how the data will be saved")
    parser.add_argument("parser_type", choices=['sync', 'async'],
                        default='sync',
                        help="Specify which type of parsing to use")
    args = parser.parse_args()

    run_parser(args.parser_type, args.page_from, args.page_to,
               args.save_to)


if __name__ == "__main__":
    main()
