import requests
from utils import link_preprocessing_urlparse

def extract_text_bs4(url):
    """
    Extracts full raw text from a webpage using BeautifulSoup.

    Args:
        url (str): The URL of the webpage.

    Returns:
        str: Extracted plain text.
    """
    from bs4 import BeautifulSoup
    text = ''

    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")

    # Extracts all visible text, separating elements by space
    text = soup.get_text(separator=' ')

    return text


def extract_text_rlxml(url):
    """
    Extracts the title and main content from a webpage using the Readability algorithm.

    Args:
        url (str): The URL of the webpage.

    Returns:
        str: Concatenation of title and main content HTML.
    """
    from readability import Document
    text = ''

    response = requests.get(url)
    doc = Document(response.text)

    title = doc.title()
    content = doc.summary()

    # Combine title and content
    text = title + '\n\n' + content

    return text


def extract_text_gs3(url):
    """
    Extracts the title and cleaned article text using Goose3.

    Args:
        url (str): The URL of the webpage.

    Returns:
        str: Concatenation of article title and cleaned body text.
    """
    from goose3 import Goose
    text = ''

    g = Goose()
    article = g.extract(url=url)

    # Combine title and cleaned text
    text = article.title + "\n\n" + article.cleaned_text

    return text


def extract_text_trafilatura(url):
    """
    Extracts cleaned article text using Trafilatura.

    Args:
        url (str): The URL of the webpage.

    Returns:
        str: Cleaned main text of the article.
    """
    import trafilatura
    text = ''

    response = requests.get(url)

    # Extract relevant content
    text = trafilatura.extract(response, include_comments=False, include_tables=False)

    return text

def extract_text(url, extraction_method):
    if extraction_method == 'bs4':
        return extract_text_bs4(url)
    elif extraction_method == 'rlxml':
        return extract_text_rlxml(url)
    elif extraction_method == 'gs3':
        return extract_text_gs3(url)
    elif extraction_method == 'trafilatura':
        return extract_text_trafilatura(url)
    else:
        raise ValueError(f"Unsupported extraction method: {extraction_method}")
