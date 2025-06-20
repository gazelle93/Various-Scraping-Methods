from urllib.parse import urlparse

def link_preprocessing_urlparse(_link):
    parsed_url = urlparse(_link)
    return parsed_url