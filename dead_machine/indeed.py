import requests
import csv
from bs4 import BeautifulSoup
import time


def write_csv_header(filename):   # rewrite a file adding headers
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
        writer.writerow(('Vacancy', 'Link to a vacancy', 'Salary',  'Company', 'Short description', 'Location',
                         'Date from creation', 'Full description', 'Link to a company'))


def write_csv(data,filename):  # write data in a file
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
        #       data['Slug'], data['Format'], data[ 'Template'], data['Parent'], data['Parent Slug'], data['Order'],
        #       data['Comment Status'], data['Ping Status'], data['Post Modified Date'])
        row = (data['vacancy'], data['href'], data['salary'], data['company'], data['short_description'],
               data['location'], data['date'], data['full_description'], data['company_href'])
        writer.writerow(row)


def transfer_to_dollar(salary, all_money):
    all_symbols = ['₹', 'R', '£', '€']
    pointer = "False"
    sum1 = ''
    sum2 = ''
    money = str(salary).replace(',', '')
    print(salary)
    salary_v2 = salary
    if len(money) > 0:
        for one_sym in all_symbols:
            if money[0] == one_sym:
                pointer = 'True'
        if pointer == 'True':
            k = 1
            the_rest = ''
            while k < (len(money)):
                if sum1 == '' and sum2 == '':
                    while '0' <= money[k] <= '9':
                        sum1 = sum1 + (money[k])
                        k = k + 1
                if sum1 != '' and sum2 == '':
                    while '0' <= money[k] <= '9':
                        sum2 = sum2 + (money[k])
                        k = k + 1
                if money[k] != money[0] and money[k] != '-':
                    the_rest = the_rest + money[k]
                k = k + 1
            if money[0] == all_symbols[0]:
                sum1 = float(sum1) * all_money[0] / all_money[4]
                if sum2 != '':
                    sum2 = float(sum2) * all_money[0] / all_money[4]
            if money[0] == all_symbols[1]:
                sum1 = float(sum1) * all_money[1] / all_money[4]
                if sum2 != '':
                    sum2 = float(sum2) * all_money[1] / all_money[4]
            if money[0] == all_symbols[2]:
                sum1 = float(sum1) * all_money[2] / all_money[4]
                if sum2 != '':
                    sum2 = float(sum2) * all_money[2] / all_money[4]
            if money[0] == all_symbols[3]:
                sum1 = float(sum1) * all_money[3] / all_money[4]
                if sum2 != '':
                    sum2 = float(sum2) * all_money[3] / all_money[4]
            sum1 = round(sum1, 0)
            print(sum1)
            if sum2 != '':
                sum2 = round(sum2, 0)
                salary_v2 = '$' + str(sum1) + ' - $' + str(sum2) + the_rest
            else:
                salary_v2 = '$' + str(sum1) + the_rest
    print(salary_v2)
    return salary_v2



def searching(filename, url, all_money):  # parsing
    write_csv_header(filename)
    pattern = url + '/jobs?q=remote+work&start={}'
    p = 0
    while p < 990:
        print(p)
        url1 = pattern.format(str(p))
        print(url1)
        time.sleep(2)
        response = requests.get(url1)
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        vacancies = soup.find_all('div', class_='jobsearch-SerpJobCard unifiedRow row result')
        p = p + 10
        for vacancy in vacancies:
            vacancy_name = vacancy.find('h2').text.replace('\n', '').replace('\r', '')
            reference = url + vacancy.find('h2').find('a').get('href')
            try:
                company = vacancy.find('span', class_='company').text.replace('\n', '').replace('\r', '')
            except:
                company = ''
            try:
                city = (vacancy.find('span', class_='location accessible-contrast-color-location').text).replace('\n', '').replace('\r', '')
            except:
                city = ''
            try:
                salary = vacancy.find('span', class_='salaryText').text.replace('\n', '').replace('\r', '')
                salary = transfer_to_dollar(salary, all_money)
            except:
                salary = ''
            short_desc = vacancy.find('div', class_='summary').text.replace('\n', '').replace('\r', '').replace("'", "")
            date = vacancy.find('span', class_='date').text.replace('\n', '').replace('\r', '')
            print(reference)
            time.sleep(2)
            response2 = requests.get(reference)   # open full vacancy page
            vacancy_html = response2.text
            soup_vacancy = BeautifulSoup(vacancy_html, 'lxml')
            try:
                own_ref = soup_vacancy.find('div', class_='icl-u-lg-inlineBlock').find('a').get('href')
            except:
                own_ref = ''
            try:
                full_description = soup_vacancy.find('div', class_='jobsearch-jobDescriptionText').text.replace('\n', '').replace('\r', '').replace("'", "")
            except:
                full_description = ''
            #data = {'ID': '',
            #        'Title': vacancy_name,
            #        'Content': full_description,
            #        'Excerpt': '',
            #        'Date': date,
            #        'Post Type': 'job_listing',
            #        'Permalink': own_ref,
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
            data = {'vacancy': vacancy_name,
                    'href': reference,
                    'salary': salary,
                    'company': company,
                    'short_description': short_desc,
                    'location': city,
                    'date': date,
                    'full_description': full_description,
                    'company_href': own_ref
                    }
            write_csv(data, filename)
            print(data)


def main():
    url1 = 'http://www.cbr.ru/scripts/XML_daily.asp?'
    response = requests.get(url1)
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    valutes = soup.find('html').find_all('valute')
    for valute in valutes:
        id = valute.find('numcode').text
        nominal = valute.find('nominal').text
        if id == '356':
            rupiy = float(valute.find('value').text.replace(',', '.')) / float(nominal)
        if id == '826':
            funt = float(valute.find('value').text.replace(',', '.')) / float(nominal)
        if id == '978':
            euro = float(valute.find('value').text.replace(',', '.')) / float(nominal)
        if id == '710':
            rend = float(valute.find('value').text.replace(',', '.')) / float(nominal)
        if id == '840':
            dollar = float(valute.find('value').text.replace(',', '.')) / float(nominal)
    all_money = [rupiy, funt, euro, rend, dollar]
    f = open('indeed_list', 'r', encoding='utf', newline='')  # getting a list with countries and links
    lines = f.readlines()
    for line in lines:
        print(line)
        line = line.split()
        file_name = 'Indeed_' + line[0]
        reference = line[1]
        searching(file_name, reference, all_money)


if __name__ == '__main__':
    main()
