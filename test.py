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


def validate_date_format(date_str):
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")


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

    validate_date_format(in_start_dte)
    validate_date_format(in_end_dte)

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
    print(ssn_str)

    validate_date_format(in_birth_dte)

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
        # OUTPUT
        if check_digit == int(ssn_str[10]):
            check_digit_flag = '1'
        else:
            check_digit_flag = '0'

        # TEST SEX
        check_sex_flag = ''
        if sex == 'dowolna':
            check_sex_flag = 'NOT CHECKED'
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
            check_dte_flag = 'NOT CHECKED'
        else:
            true_ssn_date = get_date_from_ssn(ssn_str)
            birth_dte = datetime.strptime(in_birth_dte, '%Y-%m-%d')
            if true_ssn_date == birth_dte:
                check_dte_flag = '1' # date of birth AS expected
            else:
                check_dte_flag = '0' # date of birth OTHER than expected
    # OUTPUT
        return f"Validated {ssn_str}, logic:{check_digit_flag}, {sex}:{check_sex_flag}, {in_birth_dte}:{check_dte_flag}"

    else:
        return f"Validated {ssn_str}, PESEL - must be 11 digits"


#print('\nget_date_from_ssn ---------------------1')
#print(get_date_from_ssn('05250142649'))

print('\ngenerate_ssns -----------------------2')
print(generate_ssns(10))

print('\ngenerate_unique_ssns F, 1900-01-01, 1999-12-31 -------------')
#print(generate_unique_ssns(10, 'F', '1900-01-01', '1999-12-31'))

print('\n validate_ssn -----------------')
#test = generate_unique_ssns(1, 'F', '2000-01-01', '2200-01-01')
#print(test[0])
#print(validate_ssn(test[0], 'F', '2000-01-01'))

test_set0 = ['123456789012', '1234567890', '', 'abcdefghijk','1ikl..+./']
test_set1 = ['86040198264']
test_set2 = ['86040198260']



for test in test_set1:
    print(validate_ssn(test, 'F', '2000-01-01'))


#print(test[1])

# test_set0 = [''12345678901', '123456789012', '1234567890', '', 'abcdefghijk','1ikl..../+']
#
#sex
# test1 = generate_unique_ssns(1, 'dwolna', '1900-01-01', '2100-01-01')
# test2 = generate_unique_ssns(1, 'F, '1900-01-01', '2100-01-01')
# test3 = generate_unique_ssns(1, 'M, '1900-01-01', '2100-01-01')


# test3 = generate_unique_ssns(1, 'F', '1900-01-31', '1999-12-31') poza zakresie
# test5 = generate_unique_ssns(1, 'M', '1901-02-28', '2100-12-31')


# test4 = generate_unique_ssns(1, 'F', '1999-12-31', '1999-12-31')

#for i in test.iteritems():
#    print(i[1] + '  ' + i[1][0:6] + ' ' + i[1][9] + ' ----> ' + validate_ssn(i[1], 'M', '2005-05-01'))