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




print('\nget_date_from_ssn ---------------------1')
print(get_date_from_ssn('05250142649'))

print('\ngenerate_ssns -----------------------2')
print(generate_ssns(10))

print('\ngenerate_unique_ssns -----------------------2')
print(generate_unique_ssns(10, 'F', '1900-01-01', '1999-12-31'))
