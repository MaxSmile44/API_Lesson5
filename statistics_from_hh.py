from pprint import pprint
from statistics import mean

import requests


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
        salaries = []
        for vacancy in response.json()['items']:
            if not vacancy['salary'] or vacancy['salary']['currency'] != 'RUR':
                salaries.append(None)
            else:
                if not vacancy['salary']['from']:
                    salaries.append(vacancy['salary']['to'] * 0.8)
                elif not vacancy['salary']['to']:
                    salaries.append(vacancy['salary']['from'] * 1.2)
                else:
                    salaries.append((vacancy['salary']['from'] + vacancy['salary']['to']) / 2)
        all_salaries += salaries
        pages_number = response.json()['pages']
        page += 1
    return all_salaries


def get_job_statistics_from_hh(languages):
    all_result = {}

    for language in languages:
        all_salaries = predict_rub_salary_for_hh(language)
        salaries = [i for i in all_salaries if i is not None]

        language_result = {
            'vacancies_found': len(all_salaries),
            'vacancies_processed': len(salaries),
            'average_salary': int(mean(salaries)) if salaries else 0
        }
        all_result[language] = language_result
    return all_result


def main():
    languages = ['JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C', 'Go', 'Swift']
    pprint(get_job_statistics_from_hh(languages), sort_dicts=False)


if __name__ == '__main__':
    main()
