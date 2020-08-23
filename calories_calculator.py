import pdfplumber
import pprint
import re

class PDFConverter():
    def __init__(self, path):
        self.source_path = path

    def get_plain_text(self):
        pdf = pdfplumber.open(self.source_path)
        plain_text = ''
        for page in pdf.pages:
            plain_text += page.extract_text()
        pdf.close()
        return plain_text

    def categorize_list(self, text):
        product_list = dict()
        text = text.split('\n')

        category = ''
        counter = 0
        for element in text:
            if element.isdigit() or 'LISTA ZAKUPÓW' in element:
                continue
            if not any(letter.isdigit() for letter in element):
                category = element
                product_list[category] = []
            else:
                counter += 1
                entry = self.create_entry(element)
                product_list[category].append(entry)
        pprint.pprint(product_list)
        return product_list

    def create_entry(self, product):
        match_one_number = '(.+) - (\d+)\s?([a-z]+)'
        match_two_numbers = ('(.+)około\s?(\d+\.?\d?\d?)\s(.+)\s(\d+)\s?([a-z]+)')
        match_one = re.match(match_one_number, product)
        match_two = re.match(match_two_numbers, product)
        element = dict()
        if match_one:
            name = match_one.group(1)
            element[name] = {}
            element[name]['weight'] = match_one.group(2)
            element[name]['unit'] = match_one.group(3)
        elif match_two:
            name = match_two.group(1)
            element[name] = {}
            element[name]['quantity'] = match_two.group(2)
            element[name]['quantity_unit'] = match_two.group(3)
            element[name]['weight'] = match_two.group(4)
            element[name]['unit'] = match_two.group(5)
        else:
            raise Exception("{} didnt match ".format(product))
        return element




source_path = 'source/shopping_list.pdf'
pdfConverter = PDFConverter(source_path)
text = pdfConverter.get_plain_text()
shopping_list = pdfConverter.categorize_list(text)


