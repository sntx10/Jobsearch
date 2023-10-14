# 🌍 Jobsearch - Ваш мировой сервис по поиску работы

**Jobsearch** предоставляет пользователям мощные инструменты поиска вакансий и резюме по всему миру, а также удобный чат для коммуникации с работодателями и соискателями.

## Особенности:

1. **Анализ предпочтений**: Наша система учитывает интересы, опыт и местоположение пользователей при предложении вакансий.
2. **Геолокационный поиск**: Найдите работу или кандидата в нужном вам городе или даже стране.
3. **Мессенджер**: Общайтесь с потенциальными работодателями или соискателями прямо внутри системы.
4. **Отзывы и обратная связь**: Оставляйте отзывы о компаниях и вакансиях, помогая другим пользователям сделать правильный выбор.

## 🚀 Установка и настройка

### 1. **Клонирование репозитория**:
```bash
git clone https://github.com/sntx10/Jobsearch.git
```
### 2. **Создание виртуального окружения**:
```bash
python3 -m venv <название окружения>
```
### 3. **Активация виртуального окружения**:
```bash
source <название окружения>/bin/activate
```
### 4. **Установка зависимостей**:
```bash
pip3 install -r requirements.txt
```
### 5. **Настройка конфигурации**:
```bash
Переименуйте файл env_example в .env.
Обновите значения в файле .env соответствующим образом.
```
### 6. **Миграция базы данных**:
```bash
python3 manage.py migrate
```
### 7. **Запуск сервера**:
```bash
python3 manage.py runserver
```