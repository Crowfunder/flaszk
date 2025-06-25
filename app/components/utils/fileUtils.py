import os
from hashlib import sha256


def checkIfFileExists(file_path):
    return os.path.isfile(file_path)


def getFileHash(file_path):
    return sha256(open(file_path,'rb').read()).hexdigest()
