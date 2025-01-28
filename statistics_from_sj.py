import os
from pprint import pprint
from statistics import mean

import requests
from dotenv import load_dotenv


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
        salaries = []
        if response.json()['objects']:
            for item in response.json()['objects']:
                if item['payment_from'] == 0 and item['payment_to'] == 0:
                    salaries.append(None)
                else:
                    if item['payment_from'] == 0:
                        salaries.append(item['payment_to'] * 0.8)
                    elif item['payment_to'] == 0:
                        salaries.append(item['payment_from'] * 1.2)
                    else:
                        salaries.append((item['payment_from'] + item['payment_to']) / 2)
            all_salaries += salaries
            page += 1
        else:
            break
    return all_salaries


def get_job_statistics_from_sj(languages, sj_key):
    all_result = {}

    for language in languages:
        all_salaries = predict_rub_salary_for_sj(language, sj_key)
        salaries = [i for i in all_salaries if i is not None]

        language_result = {
            'vacancies_found': len(all_salaries),
            'vacancies_processed': len(salaries),
            'average_salary': int(mean(salaries)) if salaries else 0
        }
        all_result[language] = language_result
    return all_result


def main():
    load_dotenv()
    sj_key = os.getenv('SJ_KEY')
    languages = ['JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C', 'Go', 'Swift']
    pprint(get_job_statistics_from_sj(languages, sj_key), sort_dicts=False)


if __name__ == '__main__':
    main()
