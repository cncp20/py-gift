import os
from common.error import NotFileError, FormatError

def check_file(path):
    if not os.path.exists(path):
        raise NotFileError("not found %s" % path)
    if not path.endswith(".json"):
        raise FormatError()