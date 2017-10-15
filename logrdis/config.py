import yaml


def parse(filename):
    """Parse a yaml config file.

    :param filename: a filename / filepath
    :returns: dict. a parsed configuration object
    """
    with open(filename) as fptr:
        data = yaml.load(fptr.read())
    return data