import csv


def csv_to_list(file):
    with open(file, 'r') as data:
        list_of_values = [line for line in csv.DictReader(data)]
    return list_of_values

a = csv_to_list('ChatbotIZS - DB model.xlsx - Answers.csv')
print(a)