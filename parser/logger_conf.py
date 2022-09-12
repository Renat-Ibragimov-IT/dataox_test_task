import logging

logging.getLogger().setLevel(logging.INFO)


def logger(msg: str) -> None:
    """
    Function to create logger and show msg in the console.
    Parameters
    __________
    msg : list
        Message to show in console
    Returns
    _______
    Logger object.
    """
    return logging.info(msg)
