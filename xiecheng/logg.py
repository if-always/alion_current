import logging
#####alion
def info(infos):

    logger = logging.getLogger()

    handler=logging.StreamHandler()

    fmt = '>>>%(asctime)s  %(message)s'

    formatter = logging.Formatter(fmt)

    handler.setFormatter(formatter)


    logger.addHandler(handler)

    logger.setLevel(logging.NOTSET)


    logger.info(infos)


if __name__ == '__main__':
    pass