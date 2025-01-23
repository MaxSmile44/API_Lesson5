# Выгрузка статистики зарплат вакансий программистов по популярным языкам программирования в Москве с сайтов SuperJob и HeadHunter.

### Как запустить
#### main.py
Для вывода таблиц статистики зарплат вводим в терминал:
```
python main.py
```

### Структура программы

#### main.py
Содержит функции по преобразованию данных из модулей statistics_from_hh.py и statistics_from_sj.py в таблицы.

#### statistics_from_hh.py
Собирает статистику зарплат вакансий программистов по популярным языкам программирования в Москве с сайта HeadHunter за последнии 30 дней.

Данные хранятся в словаре. Пример словаря: 

{'JavaScript': {'vacancies_found': 8, 'vacancies_processed': 3, 'average_salary': 128666}, 'Java': {'vacancies_found': 5, 'vacancies_processed': 3, 'average_salary': 50666}} 

#### statistics_from_sj.py
Собирает статистику зарплат вакансий программистов по популярным языкам программирования в Москве с сайта SuperJob. 

API SuperJob позволяют собирать только 500 записей (например 5 страниц по 100 записей).

Данные хранятся в словаре. Пример словаря: 

{'JavaScript': {'vacancies_found': 8, 'vacancies_processed': 3, 'average_salary': 128666}, 'Java': {'vacancies_found': 5, 'vacancies_processed': 3, 'average_salary': 50666}} 

### Как установить
Необходимо получить Secret key на сайте SuperJob https://api.superjob.ru/info/.

Создаем файл для переменных окружения `.env` в одной директории с файлом main.py и прописываем в него:
```
SJ_KEY=Secret key с сайта SuperJob без кавычек и пробелов

```

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
