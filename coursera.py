from bs4 import BeautifulSoup
from lxml import etree
from openpyxl import Workbook
import requests
import random


COURSES_URL = "https://www.coursera.org/sitemap~www~courses.xml"


def get_courses_list(sample_size=20):
    courses_raw_info = requests.get(COURSES_URL).content
    root = etree.fromstring(courses_raw_info)
    return [course_unit[0].text for course_unit in random.sample(list(root), sample_size)]


def fetch_course_start_date(beatiful_soup_object):
    js_data = beatiful_soup_object.find('script', {'type': 'application/ld+json'}).text
    datetime = None
    json_course = beatiful_soup_object.find('script', {'type': 'application/ld+json'}).text
    if json_course:
        datetime = beatiful_soup_object.loads(json_course)['hasCourseInstance'][0]['startDate']
    return datetime




def get_course_info(course_slug):  # название, язык, ближайшую дату начала, количество недель и среднюю оценку
    for course in course_slug:
        page = requests.get(course).content
        soup = BeautifulSoup(page, 'html.parser')
        course_name = soup.find('div', {'class': 'title display-3-text'})
        course_rate = soup.find('div', {'class': 'ratings-text bt3-visible-xs'})
        course_language = soup.find('div', {'class': 'language-info'})
        course_duration = len(soup.find_all('div', {'class': 'week'}))
        course_start_date = fetch_course_start_date()

    return course_name, course_language, course_start_date ,course_duration, course_rate


def get_course_start(course_object):
    class_to_store_lang_info = "basic-info-table bt3-table bt3-table-striped bt3-table-bordered bt3-table-responsive"
    pass


def output_courses_info_to_xlsx():
    courses_workbook = Workbook()
    workbook_page = courses_workbook.active
    column_names = ['Course name', 'URL', 'Language', 'Start date', 'Duration', 'Average rating']

    for index, name in enumerate(column_names):
        workbook_page.cell(row=1, column=index+1).value = name

    courses_workbook.save('C:\\Users\\Vadim\\Desktop\\123.xlsx')


if __name__ == '__main__':
    print(get_courses_list())
    output_courses_info_to_xlsx()
