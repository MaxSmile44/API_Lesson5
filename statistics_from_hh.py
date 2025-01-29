from pprint import pprint
from statistics import mean

import requests

from salary_value import counting_salary


PROGRAMMER_ROLE_NUMBER = '96'
MOSCOW_AREA_NUMBER = '1'
COUNT_DAYS_OF_PERIOD = '30'
COUNT_VACANCIES_IN_PAGE = 100


def predict_rub_salary_for_hh(language):
    url = 'https://api.hh.ru/vacancies'
    page = 0
    pages_number = 1
    all_salaries = []
    while page < pages_number:
        payload = {
            'professional_role': PROGRAMMER_ROLE_NUMBER,
            'area': MOSCOW_AREA_NUMBER,
            'period': COUNT_DAYS_OF_PERIOD,
            'text': language,
            'page': page,
            'per_page': COUNT_VACANCIES_IN_PAGE
        }
        response = requests.get(url, params=payload)
        response.raise_for_status()
        vacancies = response.json()
        salaries = []
        for vacancy in vacancies['items']:
            if vacancy['salary'] and vacancy['salary']['currency'] == 'RUR':
                salaries.append(
                    counting_salary(vacancy['salary']['from'],
                                    vacancy['salary']['to'])
                )
        all_salaries += salaries
        if not page:
            pages_number = vacancies['pages']
        page += 1
    count_salaries = int(vacancies['found'])
    return all_salaries, count_salaries


def get_job_statistics_from_hh(languages):
    all_result = {}
    for language in languages:
        salaries, count_salaries = predict_rub_salary_for_hh(language)
        language_result = {
            'vacancies_found': count_salaries,
            'vacancies_processed': len(salaries),
            'average_salary': int(mean(salaries)) if salaries else 0
        }
        all_result[language] = language_result
    return all_result


def main():
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
    pprint(get_job_statistics_from_hh(languages), sort_dicts=False)


if __name__ == '__main__':
    main()
