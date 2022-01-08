from faker import Faker
from faker.providers import ssn
import pandas as pd
from datetime import datetime


def get_date_from_ssn(ssn_str):

    true_ssn_day = int(ssn_str[4:6])

    month_to_decode = int(ssn_str[2:4])
    true_ssn_month = month_to_decode % 20

    year_to_decode = int(ssn_str[0:2])
    if 1 <= month_to_decode <= 12:
        true_ssn_year = 1900 + year_to_decode
    elif 1 + 20 <= month_to_decode <= 12 + 20:
        true_ssn_year = 2000 + year_to_decode
    elif 1 + 40 <= month_to_decode < 12 + 40:
        true_ssn_year = 2100 + year_to_decode
    elif 1 + 60 <= month_to_decode < 12 + 60:
        true_ssn_year = 2200 + year_to_decode
    elif 1 + 80 <= month_to_decode < 12 + 80:
        true_ssn_year = 1800 + year_to_decode
    else:
        true_ssn_year = 0

    true_ssn_date = datetime(true_ssn_year, true_ssn_month, true_ssn_day)
    print(f" {ssn_str} --- {true_ssn_date}  y {ssn_str[0:2]}, --> {true_ssn_year}, m {ssn_str[2:4]} --> {true_ssn_month}, d {ssn_str[4:6]}")
    return true_ssn_date



def generate_ssns(elements):
    # log time
    # start = datetime.now()
    # log time

    fake = Faker(locale='pl_PL')
    ssns_list = []
    for element in range(elements):
        value = fake.ssn()
        ssns_list.append(value)

    ssns_series = pd.Series(ssns_list)

    # log time
    # end = datetime.now()
    # print(f"Time ----- {end - start}\n")
    # with open('run_log.txt', 'a+') as file:
    #    file.write(f"gs  at time {start} ---> {end - start}, {elements}\n")
    # log time

    return ssns_series


def generate_unique_ssns(elements, sex, in_start_dte, in_end_dte):
    # log time
    start = datetime.now()
    # log time

    ssns_list = []
    while len(ssns_list) + 1 <= elements:

        # ssn_str = fake.ssn()
        ssn_str = generate_ssns(1).tolist()[0]

        if ssn_str not in ssns_list:
            start_dte = datetime.strptime(in_start_dte, '%Y-%m-%d')
            end_dte = datetime.strptime(in_end_dte, '%Y-%m-%d')
            true_ssn_date = get_date_from_ssn(ssn_str)

            if start_dte <= true_ssn_date <= end_dte:
                if sex == 'F' and int(ssn_str[9]) % 2 == 0:
                    ssns_list.append(ssn_str)
                elif sex == 'M' and int(ssn_str[9]) % 2 != 0:
                    ssns_list.append(ssn_str)

    ssns_series = pd.Series(ssns_list)

    # log time
    end = datetime.now()
    print(f"Time ----- {end - start}")
    with open('test.txt', 'a+') as file:
        file.write(f"gus at time {start} ---> {end - start}, {elements}, {sex}, {in_start_dte}, {in_end_dte}\n")
    # log time

    return ssns_series

def validate_ssn(ssn_str, sex, in_birth_dte):
    # TEST IS 11 INT
    if ssn_str.isnumeric() and len(ssn_str) == 11:
        # TEST SEX
        check_sex = ''
        if sex == 'dowolna':
            check_sex = 'sex NOT CHECKED.'
        else:
            if sex == 'F':
                if int(ssn_str[9]) % 2 == 0:
                    check_sex = '1 - is female PESEL'
                else:
                    check_sex = '0 - is not female PESEL'
            elif sex == 'M':
                if int(ssn_str[9]) % 2 != 0:
                    check_sex = '1 - is male PESEL'
                else:
                    check_sex = '0 - is not male PESEL'

        # TEST DATE OF BIRTH
        if in_birth_dte == 'dowolna':
            check_dte = 'date of birth NOT CHECKED.'
        else:
            true_ssn_date = get_date_from_ssn(ssn_str)

            birth_dte = datetime.strptime(in_birth_dte, '%Y-%m-%d')
            if true_ssn_date == birth_dte:
                check_dte = '1 - date of birth AS expected'
            else:
                check_dte = '0 - date of birth OTHER than expected'

        # TEST LAST DIGIT
        weights_for_check_digit = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
        sum_digit = 0
        for digits in range(0, 10):
            sum_digit += weights_for_check_digit[digits] * int(ssn_str[digits])
            # print(f"{sum_digit} =  {weights_for_check_digit[digits]} * {int(ssn_str[digits])}")

        check_digit = 10 - sum_digit % 10
        # print(check_digit)

        if check_digit == 10:
            check_digit = 0

        # print(int(ssn_str[10]), check_digit)

        # OUTPUTS
        if check_digit == int(ssn_str[10]):
            return f"1 -Correct PESEL | {check_sex} (ex {sex}) | {check_dte} (is{true_ssn_date.date()},ex{in_birth_dte})"
        else:
            return f"0 -Incorrect PESEL - incorrect control digit, {check_sex}, {check_dte}"

    return "0 - Incorrect PESEL - must be 11 digits"



print('\nget_date_from_ssn ---------------------1')
print(get_date_from_ssn('05250142649'))

print('\ngenerate_ssns -----------------------2')
print(generate_ssns(10))

print('\ngenerate_unique_ssns F, 1900-01-01, 1999-12-31 -------------')
print(generate_unique_ssns(10, 'F', '1900-01-01', '1999-12-31'))
#print('\ngenerate_unique_ssns F, 1800-01-01, 1899-12-31 -------------')
#print(generate_unique_ssns(10, 'F', '1800-01-01', '1899-12-31'))
print('\ngenerate_unique_ssns F, 2100-01-01, 2000-12-31 -------------')
print(generate_unique_ssns(10, 'F', '2000-01-01', '2000-12-31'))