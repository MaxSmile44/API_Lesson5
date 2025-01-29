import os
from pprint import pprint
from statistics import mean

import requests
from dotenv import load_dotenv

from salary_value import get_salary_value


BLOCK_NUMBER_FOR_POSITION = 1
BLOCK_NUMBER_FOR_LANGUAGE = 10
MOSCOW_AREA_NUMBER = 4
PUBLICATION_PERIOD_FOR_ALL_TIME = 0
COUNT_VACANCIES_IN_PAGE = 100


def predict_rub_salary_for_sj(language, sj_key):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    page = 0
    all_salaries = []
    while True:
        headers = {'X-Api-App-Id': sj_key}
        params = {
            'keywords': [
                [BLOCK_NUMBER_FOR_POSITION, BLOCK_NUMBER_FOR_LANGUAGE],
                ['and', 'and'],
                ['Программист', language]
            ],
            'town': MOSCOW_AREA_NUMBER,
            'period': PUBLICATION_PERIOD_FOR_ALL_TIME,
            'count': COUNT_VACANCIES_IN_PAGE,
            'page': page
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        vacancies = response.json()
        salaries = []
        if vacancies['objects']:
            for vacancy in vacancies['objects']:
                if vacancy['payment_from'] or vacancy['payment_to']:
                    salaries.append(
                        get_salary_value(vacancy['payment_from'],
                                        vacancy['payment_to'])
                    )
            all_salaries += salaries
            page += 1
        else:
            break
    salaries_count = vacancies['total']
    return all_salaries, salaries_count


def get_job_statistics_from_sj(languages, sj_key):
    all_result = {}
    for language in languages:
        salaries, count_salaries = predict_rub_salary_for_sj(language, sj_key)
        language_result = {
            'vacancies_found': count_salaries,
            'vacancies_processed': len(salaries),
            'average_salary': int(mean(salaries)) if salaries else 0
        }
        all_result[language] = language_result
    return all_result


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
    pprint(get_job_statistics_from_sj(languages, sj_key), sort_dicts=False)


if __name__ == '__main__':
    main()
