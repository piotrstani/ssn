from faker import Faker
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


# 1
# %%time

def generate_ssns(elements):
    start = datetime.now()
    fake = Faker(locale='pl_PL')
    ssns_list = []
    for element in range(elements):
        value = fake.ssn()
        ssns_list.append(value)

    ssns = pd.Series(ssns_list)
    end = datetime.now()
    print(f"Time ----- {end - start}")
    with open('run_log.txt', 'a+') as file:
        file.write(f"gs  at time {start} ---> {end - start}, {elements}\n")
    return ssns

# 2
# %%time


def generate_unique_ssns(elements, sex, in_start_dte, in_end_dte):
    start = datetime.now()
    fake = Faker(locale='pl_PL')
    ssns_list = []
    while len(ssns_list) + 1 <= elements:

        ssn_str = fake.ssn()

        if ssn_str not in ssns_list:
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

            start_dte = datetime.strptime(in_start_dte, '%Y-%m-%d')
            end_dte = datetime.strptime(in_end_dte, '%Y-%m-%d')

            if start_dte <= true_ssn_date <= end_dte:
                print('jest w range')
                if sex == 'F' and int(ssn_str[9]) % 2 == 0:
                    ssns_list.append(ssn_str)
                elif sex == 'M' and int(ssn_str[9]) % 2 != 0:
                    ssns_list.append(ssn_str)
    ssns = pd.Series(ssns_list)
    end = datetime.now()
    print(f"Time ----- {end - start}")
    with open('test.txt', 'a+') as file:
        file.write(f"gus at time {start} ---> {end - start}, {elements}, {sex}, {in_start_dte}, {in_end_dte}\n")
    return ssns


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
                print('incorect?')

            true_ssn_date = datetime(true_ssn_year, true_ssn_month, true_ssn_day)

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




generate_ssns(1)
generate_unique_ssns(10, 'F', '1800-01-01', '2200-01-01')
print(validate_ssn('05250142649', 'F', '2005-05-01'))


test = generate_unique_ssns(1, 'M', '1800-01-01', '2200-01-01')
print(test[1])
for i in test.iteritems():
    print(i[1] + '  ' + i[1][0:6] + ' ' + i[1][9] + ' ----> ' + validate_ssn(i[1], 'M', '2005-05-01'))
