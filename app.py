import argparse

from sync_parser import SyncParser


def run_parser(type_of_parser: str):
    parser_choices = {"sync": SyncParser, "async": ''}  # TODO: async
    return parser_choices[type_of_parser](args.page_from, args.page_to,
                                          args.save_to)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parser app")
    parser.add_argument('-page_from', default=1, type=int,
                        help="Specify the site page to start parsing")
    parser.add_argument('-page_to', default=2, type=int,
                        help="Specify the site page to start parsing")
    parser.add_argument('-save_to', choices=['postgres', 'google_sheets'],
                        default='postgres',
                        help="Specify how the data will be saved")
    parser.add_argument("-parser_type", choices=['sync', 'async'],
                        default='sync',
                        help="Specify which type of parsing to use")
    args = parser.parse_args()

    run_parser(args.parser_type)
