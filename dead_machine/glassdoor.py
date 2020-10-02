import requests
import csv
from bs4 import BeautifulSoup
import time


def cookie(cook):  # хранит сведения о куки с сайта Яндекс.услуги
    cookies = dict(
        cookies_are=cook)
    return cookies


def user_agent():  # хранит сведения о юзер агента с сайта Яндекс.услуги
    ua = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
}
    return ua


def write_csv_header(filename):  # обновляет файл, добавляя в него заголовки
    with open(filename + '.csv', 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        #writer.writerow(('ID', 'Title', 'Content', 'Excerpt', 'Date', 'Post Type', 'Permalink', 'Image URL',
        #                 'Image Title', 'Image Caption', 'Image Description', 'Image Alt Text', 'Image Featured',
        #                 'Attachment URL', 'Types', 'Categories', 'Locations', 'Tags', '_elementor_controls_usage',
        #                 '_job_application_deadline_date', '_job_apply_type', '_job_apply_url', '_job_apply_email',
        #                 '_job_salary', '_job_max_salary', '_job_salary_type', '_job_featured', '_job_urgent',
        #                 '_job_map_location', '_job_custom_qualification', '_job_address', '_job_map_location_address',
        #                 '_job_map_location_latitude', '_job_map_location_longitude', '_job_views_count',
        #                 '_job_posted_by', '_job_custom_salary', '_job_custom_designation', '_job_custom_experince',
        #                 '_job_expiry_date', '_wp_old_slug', '_job_custom_offerd-salary', '_viewed_count',
        #                 '_views_by_date', '_recently_viewed', '_job_indeed_detail_url', '_job_indeed_company_name',
        #                 '_job_layout_type', 'Status', 'Author ID', 'Author Username', 'Author Email',
        #                 'Author First Name', 'Author Last Name', 'Slug', 'Format', 'Template', 'Parent',
        #                 'Parent Slug', 'Order', 'Comment Status', 'Ping Status', 'Post Modified Date'))
        writer.writerow(('Vacancy', 'Link to a vacancy', 'Salary', 'Company', 'Short description', 'Location',
                            'Date from creation', 'Full description', 'Link to a company'))


def write_csv(data, filename):  # записывает данные в файл csv
    with open(filename + '.csv', 'a', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        #row = (data['ID'], data['Title'], data['Content'], data['Excerpt'], data['Date'],
        #       data['Post Type'], data['Permalink'], data['Image URL'], data['Image Title'], data['Image Caption'],
        #       data['Image Description'], data['Image Alt Text'], data['Image Featured'], data['Attachment URL'],
        #       data['Types'], data['Categories'], data['Locations'], data['Tags'], data['_elementor_controls_usage'],
        #       data['_job_application_deadline_date'], data['_job_apply_type'], data['_job_apply_url'],
        #       data['_job_apply_email'], data['_job_salary'], data['_job_max_salary'], data['_job_salary_type'],
        #       data['_job_featured'], data['_job_urgent'], data['_job_map_location'], data['_job_custom_qualification'],
        #       data['_job_address'], data['_job_map_location_address'], data['_job_map_location_latitude'],
        #       data['_job_map_location_longitude'], data['_job_views_count'], data['_job_posted_by'],
        #       data['_job_custom_salary'], data['_job_custom_designation'], data['_job_custom_experince'],
        #       data['_job_expiry_date'], data['_wp_old_slug'], data['_job_custom_offerd-salary'], data['_viewed_count'],
        #       data['_views_by_date'], data['_recently_viewed'], data['_job_indeed_detail_url'],
        #       data['_job_indeed_company_name'], data['_job_layout_type'], data['Status'], data['Author ID'],
        #       data['Author Username'], data['Author Email'], data['Author First Name'], data['Author Last Name'],
        #       data['Slug'], data['Format'], data['Template'], data['Parent'], data['Parent Slug'], data['Order'],
        #       data['Comment Status'], data['Ping Status'], data['Post Modified Date'])
        row = (data['vacancy'], data['href'], data['salary'], data['company'], data['short_description'],
               data['location'], data['date'], data['full_description'], data['company_href'])
        writer.writerow(row)


def searching(filename, pattern, cook):  # parsing
    write_csv_header(filename)
    cookies = cookie(cook)
    print(cook)
    user_agents = user_agent()
    p = 0
    while p < 31:
        print(p)
        url = pattern.format(str(p)) + '.htm'
        print(url)
        time.sleep(2)
        response = requests.get(url, headers=user_agents, cookies=cookies)
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        vacancies = soup.find_all('li', class_='jl react-job-listing gdGrid')
        p = p + 1
        for vacancy in vacancies:
            try:
                company = vacancy.find('div', class_='jobHeader').text
            except:
                company = ''
            try:
                date = vacancy.find('div', class_='d-flex align-items-end pl-std css-mi55ob').text
            except:
                date = ''
            try:
                city = vacancy.find('div', class_='d-flex flex-wrap css-11d3uq0 e1rrn5ka1').find('span', class_='subtle loc css-nq3w9f pr-xxsm').text
            except:
                city = ''
            try:
                salary = vacancy.find('div', class_='jobFooter d-flex flex-wrap css-o853md e1rrn5ka0').find('span', class_="gray salary").text
            except:
                salary = ''
            reference = vacancy.find('div', class_='jobHeader').find('a').get('href')
            reference = 'https://www.glassdoor.com' + reference
            time.sleep(2)
            vacancy_response = requests.get(reference, headers=user_agents, cookies=cookies)
            vacancy_html = vacancy_response.text
            vacancy_soup = BeautifulSoup(vacancy_html, 'lxml')
            try:
                full_description = vacancy_soup.find('div', class_='desc css-58vpdc ecgq1xb3').text.strip()
            except:
                full_description = ''
            try:
                vacancy_name = vacancy_soup.find('div', class_='css-17x2pwl e11nt52q6').text
            except:
                vacancy_name = ''
            try:
                company_ref = 'https://www.glassdoor.com' + vacancy_soup.find('div', class_='css-0 e1h54cx80').find('a').get('data-job-url')
            except:
                company_ref = ''
            data = {'vacancy': vacancy_name,
                    'href': reference,
                    'salary': salary,
                    'company': company,
                    'short_description': full_description,
                    'location': city,
                    'date': date,
                    'full_description': full_description,
                    'company_href': company_ref
                    }
            #data = {'ID': '',
            #        'Title': vacancy_name,
            #        'Content': full_description,
            #        'Excerpt': '',
            #        'Date': date,
            #        'Post Type': 'job_listing',
            #        'Permalink': company_ref,
            #        'Image URL': '',
            #        'Image Title': '',
            #        'Image Caption': '',
            #        'Image Description': '',
            #        'Image Alt Text': '',
            #        'Image Featured': '',
            #        'Attachment URL': '',
            #        'Types': '',
            #        'Categories': '',
            #        'Locations': city,
            #        'Tags': '',
            #        '_elementor_controls_usage': '',
            #        '_job_application_deadline_date': '',
            #        '_job_apply_type': '',
            #        '_job_apply_url': reference,
            #        '_job_apply_email': '',
            #        '_job_salary': salary,
            #        '_job_max_salary': '',
            #        '_job_salary_type': '',
            #        '_job_featured': '',
            #        '_job_urgent': '',
            #        '_job_map_location': '',
            #        '_job_custom_qualification': '',
            #        '_job_address': city,
            #        '_job_map_location_address': '',
            #        '_job_map_location_latitude': '',
            #        '_job_map_location_longitude': '',
            #        '_job_views_count': '',
            #        '_job_posted_by': '',
            #        '_job_custom_salary': '',
            #        '_job_custom_designation': '',
            #        '_job_custom_experince': '',
            #        '_job_expiry_date': '',
            #        '_wp_old_slug': '',
            #        '_job_custom_offerd-salary': '',
            #        '_viewed_count': '',
            #        '_views_by_date': '',
            #        '_recently_viewed': '',
            #        '_job_indeed_detail_url': '',
            #        '_job_indeed_company_name': '',
            #        '_job_layout_type': '',
            #        'Status': '',
            #        'Author ID': '',
            #        'Author Username': '',
            #        'Author Email': '',
            #        'Author First Name': '',
            #        'Author Last Name': '',
            #        'Slug': vacancy_name,
            #        'Format': '',
            #        'Template': '',
            #        'Parent': '',
            #        'Parent Slug': '',
            #        'Order': '',
            #        'Comment Status': '',
            #        'Ping Status': '',
            #        'Post Modified Date': ''}
            write_csv(data, filename)
            print(data)


def main():
    f = open('glassdoor_list', 'r', encoding='utf', newline='')  # getting a list with countries and links
    lines = f.readlines()
    for line in lines:
        cook = ''
        line = line.split()
        file_name = 'Glassdoor_' + line[0]
        reference = line[1]
        for i in range(2, len(line)):
            cook = cook + line[i] + ' '
        searching(file_name, reference, cook)
        print('--------------------------------------------------------------------------')
        print('--------------------------------------------------------------------------')
        print(str(file_name) + ' DONE')
        print('--------------------------------------------------------------------------')
        print('--------------------------------------------------------------------------')


if __name__ == '__main__':
    main()
