import logging


def load_config():
    logging.basicConfig(level=logging.INFO, filename="log.log", filemode="a",
                        format="%(asctime)s %(levelname)s %(message)s")
