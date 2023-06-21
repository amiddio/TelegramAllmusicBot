_release_types = {
    'albums': {'label': 'Albums', 'uri': '{url}/discography'},
    'compilations': {'label': 'Compilations', 'uri': '{url}/discography/compilations'},
    'singles': {'label': 'Singles & EPs', 'uri': '{url}/discography/singles'},
    'videos': {'label': 'DVDs & Videos', 'uri': '{url}/discography/video'},
    'others': {'label': 'Others', 'uri': '{url}/discography/others'},
}


def get_release_type_key(label: str) -> str:
    for key, value in _release_types.items():
        if value['label'] == label:
            return key


def get_release_type_value(key: str) -> dict:
    return _release_types[key]
