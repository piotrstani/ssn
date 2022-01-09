from faker import Faker
from faker.providers import ssn
import pandas as pd
from datetime import datetime


# ZADANIE 1
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


# ZADANIE 2
def is_valid_date_format(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")


def is_valid_date(year, month, day):
    try:
        datetime(year, month, day)
    except ValueError:
        raise ValueError("Incorrect date, it is not a date")


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
    is_valid_date(true_ssn_year, true_ssn_month, true_ssn_day)
    true_ssn_date = datetime(true_ssn_year, true_ssn_month, true_ssn_day)
    return true_ssn_date

def generate_unique_ssns(elements, sex, in_start_dte, in_end_dte):
    # log time
    # start = datetime.now()
    # log time
    ssns_list = []
    while len(ssns_list) + 1 <= elements:

        # ssn_str = fake.ssn()
        ssn_str = generate_ssns(1).tolist()[0]

        if ssn_str not in ssns_list:
            start_dte = datetime.strptime(in_start_dte, '%Y-%m-%d')
            is_valid_date_format(in_start_dte)
            end_dte = datetime.strptime(in_end_dte, '%Y-%m-%d')
            is_valid_date_format(in_end_dte)

            true_ssn_date = get_date_from_ssn(ssn_str)

            if start_dte <= true_ssn_date <= end_dte:
                if sex == 'F' and int(ssn_str[9]) % 2 == 0:
                    ssns_list.append(ssn_str)
                elif sex == 'M' and int(ssn_str[9]) % 2 != 0:
                    ssns_list.append(ssn_str)

    ssns_series = pd.Series(ssns_list)

    # log time
    # end = datetime.now()
    # print(f"Time ----- {end - start}")
    # with open('test.txt', 'a+') as file:
    #    file.write(f"gus at time {start} ---> {end - start}, {elements}, {sex}, {in_start_dte}, {in_end_dte}\n")
    # log time

    return ssns_series


def validate_ssn(ssn_str, sex, in_birth_dte):

    # TEST IS 11 INT
    if ssn_str.isnumeric() and len(ssn_str) == 11:

        # TEST LAST DIGIT
        check_digit_flag = ''
        weights_for_check_digit = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
        sum_digit = 0

        for digits in range(0, 10):
            sum_digit += weights_for_check_digit[digits] * int(ssn_str[digits])
            # print(f"{sum_digit} =  {weights_for_check_digit[digits]} * {int(ssn_str[digits])}")

        check_digit = 10 - sum_digit % 10
        if check_digit == 10:
            check_digit = 0

        if check_digit == int(ssn_str[10]):
            check_digit_flag = '1'
        else:
            check_digit_flag = '0'

        # TEST SEX
        check_sex_flag = ''
        if sex == 'dowolna':
            check_sex_flag = '?'
        else:
            if sex == 'F':
                if int(ssn_str[9]) % 2 == 0:
                    check_sex_flag = '1' # is female PESEL'
                else:
                    check_sex_flag = '0' # is not female PESEL'
            elif sex == 'M':
                if int(ssn_str[9]) % 2 != 0:
                    check_sex_flag = '1' # is male PESEL'
                else:
                    check_sex_flag = '0' # is not male PESEL'

        # TEST DATE OF BIRTH
        if in_birth_dte == 'dowolna':
            check_dte_flag = '?'
        else:
            is_valid_date_format(in_birth_dte)
            true_ssn_date = get_date_from_ssn(ssn_str)
            print(true_ssn_date)
            birth_dte = datetime.strptime(in_birth_dte, '%Y-%m-%d')
            print(birth_dte)
            if true_ssn_date == birth_dte:
                print('tu')
                check_dte_flag = '1' # date of birth AS expected
            else:
                check_dte_flag = '0' # date of birth OTHER than expected
    # OUTPUT
        return f"PESEL:{ssn_str}|correct_pesel:{check_digit_flag}|{sex}:{check_sex_flag}|{in_birth_dte}:{check_dte_flag}"

    else:
        return f"PESEL:{ssn_str}|PESEL must have 11 digits"


# ZADANIE 3
test_set4 = ['93031378554']
print(validate_ssn('93031378554', 'F', '1999-03-13')+'exp F:0,1999-03-13:1')


test_set3 = ['06222487465']
print(validate_ssn('06222487465', 'M', '2006-02-24')+'exp F:0,2006-02-24:1')
