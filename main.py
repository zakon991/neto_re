import csv
import re

def normalization_full_name(data: list) -> list:
    for i in range(1, len(data)):
        new_row = data[i][:3]
        new_row = ' '.join(new_row).strip().split()
        for j in range(0, len(new_row)):
            data[i][j] = new_row[j]
    return data

def normalization_phone_number(data:list) -> list:
    pattern = r"(\+7|8)?\s*\(?(\d{2,3})\)?\s*(\d{2,3})[-\s]*(\d{2,3})[-\s]*(\d{2,3})\s*\(*(доб\.)*\s*(\d+)*\)*"
    substitute = r"+7(\2)\3-\4-\5 \6\7"
    for i in range(1, len(data)):
        result = re.sub(pattern, substitute, data[i][5])
        data[i][5] = result.strip()
    return data

def union_dublicates(data:list) -> list:
    my_dict = {}
    for row in data:
        key = row[0] + ' ' + row[1]
        if key not in my_dict:
            my_dict[key] = row[2:]
        else:
            for i in range(5):
                if not my_dict[key][i]:
                    my_dict[key][i] = row[i+2]
    result = []
    for key, value in my_dict.items():
        key = key.split()
        key.extend(value)
        result.append(key)
    return result

if __name__ == '__main__':
    with open('phonebook_raw.csv', encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=',')
        contact_list = list(rows)

    new_data = normalization_full_name(contact_list)
    new_data = normalization_phone_number(new_data)
    new_data = union_dublicates(new_data)

    with open("phonebook.csv", "w", encoding='utf-8') as f:
        data_writer = csv.writer(f, delimiter=',', lineterminator="\r")
        data_writer.writerows(new_data)