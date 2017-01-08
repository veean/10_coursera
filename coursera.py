import bs4
from lxml import etree
import openpyxl
import requests


COURSES_URL = "https://www.coursera.org/sitemap~www~courses.xml"

def get_courses_list():
    response = requests.get(COURSES_URL)
    root = etree.fromstring(response.content)
    return [url.text for url in root.iter("{*}loc")]


def get_course_info(course_slug):
    pass


def output_courses_info_to_xlsx(filepath):
    pass


if __name__ == '__main__':
    pass
