from bs4 import BeautifulSoup
from lxml import etree
from openpyxl import Workbook
import requests
import random
import json

COURSES_URL = "https://www.coursera.org/sitemap~www~courses.xml"


def get_courses_list(sample_size=20):
    courses_raw_info = requests.get(COURSES_URL).content
    root = etree.fromstring(courses_raw_info)
    return [course_unit[0].text for course_unit in random.sample(list(root), sample_size)]


def fetch_course_start_date(beautiful_soup_object):
    start_date_footprint = 'startDate'
    json_with_possible_start_date = beautiful_soup_object.find('script', {'type': 'application/ld+json'})
    if json_with_possible_start_date and start_date_footprint in json_with_possible_start_date.text:
        datetime = json.loads(json_with_possible_start_date.text)['hasCourseInstance'][0]['startDate']
        return datetime


def fetch_course_name(beautiful_soup_object):
    course_name = beautiful_soup_object.find('div', {'class': 'title display-3-text'})
    if course_name:
        return course_name.text


def fetch_course_language(beautiful_soup_object):
    course_language = beautiful_soup_object.find('div', {'class': 'language-info'})
    if course_language:
        return course_language.text


def fetch_course_rate(beautiful_soup_object):
    course_rate = beautiful_soup_object.find('div', {'class': 'ratings-text bt3-visible-xs'})
    if course_rate:
        return course_rate.text


def get_course_info(course_slug):  # название, язык, ближайшую дату начала, количество недель и среднюю оценку
    for course in course_slug:
        page = requests.get(course).content
        soup_object = BeautifulSoup(page, 'html.parser')
        course_name = fetch_course_name(soup_object)
        course_rate = fetch_course_rate(soup_object)
        course_language = fetch_course_language(soup_object)
        course_duration = len(soup_object.find_all('div', {'class': 'week'}))
        course_start_date = fetch_course_start_date(soup_object)
        print(course_name, course, '    ',course_language, course_start_date, course_duration, course_rate)


def output_courses_info_to_xlsx():
    courses_workbook = Workbook()
    workbook_page = courses_workbook.active
    column_names = ['Course name', 'URL', 'Language', 'Start date', 'Duration', 'Average rating']

    for index, name in enumerate(column_names):
        workbook_page.cell(row=1, column=index+1).value = name

    courses_workbook.save('C:\\Users\\Vadim\\Desktop\\123.xlsx')


if __name__ == '__main__':
    print(get_course_info(get_courses_list()))
    # output_courses_info_to_xlsx()
