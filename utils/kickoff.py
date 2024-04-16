from .data_parser import extract_text_from_url

def kickoff(url):
    try:
        return extract_text_from_url(url)
    except Exception as e:
        print("kickoff failed")
        return e