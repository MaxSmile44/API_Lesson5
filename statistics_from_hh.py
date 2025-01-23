from pprint import pprint
import requests
from statistics import mean


def predict_rub_salary_for_hh(language):
    url = 'https://api.hh.ru/vacancies'
    page = 0
    pages_number = 1
    all_salaries = []
    while page < pages_number:
        payload = {'professional_role': '96', 'area': '1', 'period': '30', 'text': language, 'page': page, 'per_page': 100}
        response = requests.get(url, params=payload)
        response.raise_for_status()
        salaries = []
        for item in response.json()['items']:
            if item['salary'] is None or item['salary']['currency'] != 'RUR':
                salaries.append(None)
            else:
                if item['salary']['from'] is None:
                    salaries.append(item['salary']['to'] * 0.8)
                elif item['salary']['to'] is None:
                    salaries.append(item['salary']['from'] * 1.2)
                else:
                    salaries.append((item['salary']['from'] + item['salary']['to']) / 2)
        all_salaries += salaries
        pages_number = response.json()['pages']
        page += 1
    return all_salaries

def get_job_statistics_from_hh(languages):
    languages = languages
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