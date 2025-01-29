import os

from dotenv import load_dotenv
from terminaltables import AsciiTable

from statistics_from_hh import get_job_statistics_from_hh
from statistics_from_sj import get_job_statistics_from_sj


def get_table(title, statistics):
    row = []
    table_data = [
        [
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработано',
            'Средняя зарплата'
        ]
    ]
    for item, value in statistics.items():
        row.append(item)
        row.append(value['vacancies_found'])
        row.append(value['vacancies_processed'])
        row.append(value['average_salary'])
        table_data.append(row.copy())
        row = []
    table = AsciiTable(table_data, title)
    return table.table


def main():
    load_dotenv()
    sj_key = os.getenv('SJ_KEY')
    languages = [
        'JavaScript',
        'Java',
        'Python',
        'Ruby',
        'PHP',
        'C++',
        'C#',
        'C',
        'Go',
        'Swift'
    ]
    sj_statistics = get_job_statistics_from_sj(languages, sj_key)
    hh_statistics = get_job_statistics_from_hh(languages)
    print(get_table('SuperJob Moscow', sj_statistics))
    print(get_table('HeadHunter Moscow', hh_statistics))


if __name__ == '__main__':
    main()
