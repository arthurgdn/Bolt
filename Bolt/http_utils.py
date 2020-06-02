def utf8_bytes(text):
    """
    Ensures  that text becomes utf-8 bytes.
    :param text: strings or bytes.
    :return: a bytes object.
    """
    if not isinstance(text, bytes):
        return text.encode('utf-8')
    return text




