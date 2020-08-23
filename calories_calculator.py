import pdfplumber
import re
import os
import json

class PDFConverter():
    def __init__(self, path):
        self.source_path = path
        self.product_list = self.categorize_list()

    def get_plain_text(self):
        pdf = pdfplumber.open(self.source_path)
        plain_text = ''
        for page in pdf.pages:
            plain_text += page.extract_text()
        pdf.close()
        return plain_text

    def categorize_list(self):
        text = self.get_plain_text().split('\n')
        product_list = dict()

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
        return product_list

    def create_entry(self, product):
        match_one_number = '(.+) - (\d+)\s?([a-z]+)'
        match_one_number_some = '(.+) troszeczkę (\d+)\s?([a-z]+)'
        match_two_numbers = ('(.+)około\s?(\d+\.?\d?\d?)\s(.+)\s(\d+)\s?([a-z]+)')
        match_one = re.match(match_one_number, product) or re.match(match_one_number_some, product)
        match_two = re.match(match_two_numbers, product)
        element = dict()
        if match_one:
            element['name'] = match_one.group(1)
            element['weight'] = match_one.group(2)
            element['unit'] = match_one.group(3)
        elif match_two:
            element['name'] = match_two.group(1)
            element['quantity'] = match_two.group(2)
            element['quantity_unit'] = match_two.group(3)
            element['weight'] = match_two.group(4)
            element['unit'] = match_two.group(5)
        else:
            raise Exception("{} didn't match ".format(product))
        return element

class DataExporter():
    def __init__(self, path, data, factor):
        self.path = path
        self.data = data
        self.factor = factor
        self.name = 'shopping_list.txt'
        self.write()

    def refactor(self):
        text = ''
        for key, value in self.data.items():
            text += "\n{}\n".format(key)
            for item in value:
                element = "{} | {}{}".format(item.get('name'), float(item.get('weight'))*1.7, item.get('unit'))
                if item.get('quantity'):
                    element += ' | {} {}'.format(float(item.get('quantity', 0))*1.7, item.get('quantity_unit'))
                text += '{}\n'.format(element)
        return text

    def write(self):
        text = self.refactor()
        with open(os.path.join(self.path, self.name), 'w', encoding='utf-8') as file:
            file.write(text)


factor = 1.7

SOURCE_PATH = 'source/shopping_list.pdf'
OUTPUT_PATH = 'output'
pdfConverter = PDFConverter(SOURCE_PATH)

dataExporter = DataExporter(OUTPUT_PATH, pdfConverter.product_list, factor)
# print(pdfConverter.product_list)
