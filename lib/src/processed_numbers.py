def process_numbers(numbers):
    processed_numbers = []
    for number in numbers:
        if not number:
            continue
        if number[0] == '9':
            processed_number = '7' + number[:]
        elif number[0] == '7':
            processed_number = number
        else:
            continue
        processed_numbers.append(str(processed_number).replace('.0', ''))
    return processed_numbers