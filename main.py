from statistics_from_hh import get_job_statistics_from_hh
from statistics_from_sj import get_job_statistics_from_sj
from terminaltables import AsciiTable
from dotenv import load_dotenv
import os


def get_table_sj(languages,sj_key):
    statistics = get_job_statistics_from_sj(languages, sj_key)
    title = 'SuperJob Moscow'
    row = []
    table_data = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]
    for item, value in statistics.items():
        row.append(item)
        row.append(value['vacancies_found'])
        row.append(value['vacancies_processed'])
        row.append(value['average_salary'])
        table_data.append(row.copy())
        row = []
    table = AsciiTable(table_data, title)
    print(table.table)

def get_table_hh(languages):
    statistics = get_job_statistics_from_hh(languages)
    title = 'HeadHunter Moscow'
    row = []
    table_data = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]
    for item, value in statistics.items():
        row.append(item)
        row.append(value['vacancies_found'])
        row.append(value['vacancies_processed'])
        row.append(value['average_salary'])
        table_data.append(row.copy())
        row = []
    table = AsciiTable(table_data, title)
    print(table.table)

def main():
    load_dotenv()
    sj_key = os.getenv('SJ_KEY')
    languages = ['JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C', 'Go', 'Swift']
    get_table_sj(languages, sj_key)
    get_table_hh(languages)


if __name__ == '__main__':
    main()