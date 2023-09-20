import math


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def corutine(gen):
    def inner(*args, **kwargs):
        fn = gen(*args, **kwargs)
        next(fn)
        return fn
    return inner


@corutine
def write_chunks_in_file(file_path: str):
    with open(file_path, 'wb') as file:
        while True:
            chunk = yield
            file.write(chunk)
