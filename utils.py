import re
import html
import unicodedata

def clean_email_text(text):
    """
    Cleans email text by removing irrelevant content dynamically.
    
    Args:
        text (str): The raw email content.
        
    Returns:
        str: Cleaned text.
    """
    text = html.unescape(text)

    # Normalize Unicode and remove non-printable characters
    text = unicodedata.normalize("NFKC", text)  # Normalize Unicode to Compatibility Normal Form

    # Remove CSS/inline styles
    text = re.sub(r'[\xad\u2007\u200c\xa0]', '', text)
    text = re.sub(r'(?s)<style.*?>.*?</style>', '', text)  # Inline CSS
    text = re.sub(r'(?s)font-size:\s*\d+%.*?;', '', text)  # Inline font-size styles
    text = re.sub(r'font-family:[^;]+;', '', text)
    text = re.sub(r'[a-zA-Z0-9\s,.:;#\-\(\)%]+{[^}]*}', '', text)

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Remove repetitive HTML entities or characters
    text = re.sub(r'(&nbsp;|&zwnj;|\\xa0|\\u200c|\\xad|\\u2007)+', ' ', text)

    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)

    # Remove email footers (generalized to detect repeated line patterns or copyrights)
    text = re.sub(r'©\s?\d{4}\s?.*?All Rights Reserved.*', '', text, flags=re.IGNORECASE)
    
    # Remove excessive whitespace, tabs, and newlines
    text = re.sub(r'\\[rnt]+', '', text)
    text = re.sub(r'\s{2,}', ' ', text)
    text = re.sub(r'\n+', '\n', text)

    # Trim leading/trailing spaces
    text = text.strip()

    return text