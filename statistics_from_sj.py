from pprint import pprint
import requests
import os
from statistics import mean
from dotenv import load_dotenv


def predict_rub_salary_for_sj(language, sj_key):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    page = 0
    pages_number = 5
    all_salaries = []
    while page < pages_number:
        headers = {'X-Api-App-Id': sj_key}
        params = {'keywords': [[1, 10], ['and', 'and'], ['Программист', language]], 'town': 4, 'period': 0, 'count': 100, 'page': page}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        salaries = []
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
    return all_salaries

def get_job_statistics_from_sj(languages, sj_key):
    languages = languages
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
