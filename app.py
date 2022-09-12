import argparse

from data_collectors.async_data_collector import AsyncDataCollector
from data_collectors.sync_data_collector import SyncDataCollector


def run_parser(page_from: int, page_to: int,
               save_to: str, parser_type: str) -> object:
    """
    Function to start parsing.
    Parameters
    ----------
    page_from : int
        Specified the site page to start parsing.
    page_to : int
        Specified the site page to end parsing.
    save_to : str
        Specified how the data will be saved.
    parser_type : str
        Specified which type of parsing to use.
    """
    parser_choices = {"sync": SyncDataCollector,
                      "async": AsyncDataCollector}
    return parser_choices[parser_type](page_from, page_to,
                                       save_to)


def main():
    """
    The main function to start CLI app. Creating arguments for specifying
    program operation parameters.
    For starting app "python app.py" command can be used.
    With this command will start parsing pages from the first to the tenth
    using sync scenario with Selenium and saving parsed data to the PostgreSQL
    DB by default. For changing parameters CLI command can be used,
    for example: "python app.py 10 100 google_sheets async"
    """
    parser = argparse.ArgumentParser(description="Parser app")
    parser.add_argument('page_from', default=1, type=int,
                        help="Specify the site page to start parsing")
    parser.add_argument('page_to', default=10, type=int,
                        help="Specify the site page to end parsing")
    parser.add_argument('save_to', choices=['postgres', 'google_sheets'],
                        default='postgres',
                        help="Specify how the data will be saved")
    parser.add_argument("parser_type", choices=['sync', 'async'],
                        default='sync',
                        help="Specify which type of parsing to use")
    args = parser.parse_args()

    run_parser(args.page_from, args.page_to,
               args.save_to, args.parser_type)


if __name__ == "__main__":
    main()
