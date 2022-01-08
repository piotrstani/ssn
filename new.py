from faker import Faker
from faker.providers import ssn
import pandas as pd


def generate_ssns(elements):
    fake = Faker(locale='pl_PL')
    list = []
    for i in range(elements):
        list.append(fake.ssn())
        ssns = pd.Series(list)
    return (print(ssns))

generate_ssns(2)

month_to_decode = 41
print(1 + 40 <= month_to_decode < 12+60)


print(65 % 20)








