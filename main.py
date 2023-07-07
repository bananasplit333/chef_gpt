from pdf_parser import parse_pdf_data
import translator

delimiter = "####"
system_message = """
You will be provided with a block of text.
You will be acting as a translator from English to Korean.
The translation query will be delimited with {delimiter} characters.
"""

def main():
    pdf_location = "/Users/jhy/Documents/School/3331/penis.pdf"
    parsed_data = parse_pdf_data(pdf_location)
    
    # Print the parsed data
    print('parsing data:')
    for page_text in parsed_data:
        #messages = [
        #    {'role': 'system', 'content': system_message},
        #    {'role': 'user', 'content': page_text}
        #]
        print(page_text)

if __name__ == '__main__':
    main()
