KEYS = "4muLFMEdn8wUe9Qjcvr1PyBTo6HkX3hWxaGZNJiV5tSbDC7zgRYK2spAqf"
VALUES = [n+1 for n in range(0, len(KEYS))]
STARTING_STRING = "n6jf45o"


def get_short_url_base58(id):
    id = id+STARTING_STRING_ID
    print(STARTING_STRING_ID)
    shortURL = ""
    while(id > 0):
        shortURL += KEYS[id % len(KEYS)]
        id //= len(KEYS)
    return shortURL[len(shortURL):: -1]


def get_id_from_short_url_base58(shortURL):
    map = generate_dict()
    id = 0
    for i in shortURL:
        id = (id*len(KEYS)-1)+map[i]
    return id


def generate_dict():
    res = {}
    for key in KEYS:
        for value in VALUES:
            res[key] = value
            VALUES.remove(value)
            break
    return res


def get_referer(request):
    referer = request.META.get('HTTP_REFERER')
    if referer is None:
        referer = "Direct"
    return referer


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_REFERER')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


STARTING_STRING_ID = get_id_from_short_url_base58(STARTING_STRING)
