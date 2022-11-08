# shuffle  "4muLFMEdn8wUe9Qjcvr1PyBTo6HkX3hWxaGZNJiV5tSbDC7zgRYK2spAqf"
# base 58 "abcdefghijkmnopqrstuvwxyz123456789ABCDEFGHJKLMNPQRSTUVWXYZ"
KEYS = "4muLFMEdn8wUe9Qjcvr1PyBTo6HkX3hWxaGZNJiV5tSbDC7zgRYK2spAqf"
VALUES = [n+1 for n in range(0, len(KEYS))]
STARTING_STRING = "n6jf45o"


def idToShortURL(id):
    id = id+STARTING_STRING_ID
    print(STARTING_STRING_ID)
    shortURL = ""
    while(id > 0):
        shortURL += KEYS[id % len(KEYS)]
        id //= len(KEYS)
    return shortURL[len(shortURL):: -1]


def shortURLToId(shortURL):
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


STARTING_STRING_ID = shortURLToId(STARTING_STRING)
