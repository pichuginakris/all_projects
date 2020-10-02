import requests
import csv
from bs4 import BeautifulSoup
import time


def write_csv_header(file):  # rewrite a file adding headers
    with open(file + '.csv', 'w', encoding='utf8', newline='') as f:
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
        writer.writerow(( 'Vacancy', 'Link to a vacancy', 'Salary',  'Company',  'Short description', 'Location',
                         'Date from creation', 'Full description', 'Link to a company'))


def write_csv(data, file):  # write data in a file
    with open(file + '.csv', 'a', encoding='utf8', newline='') as f:
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
               data['location'], data['date'], data['full_description'], data['company_href'])#
        writer.writerow(row)


def searching(filename, url):  # parsing
    write_csv_header(filename)
    pattern = url + '&p={}'
    for i in range(1, 50):
        print(i)
        url = pattern.format(str(i))
        print(url)
        time.sleep(2)
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        vacancies = soup.find_all('div', class_='left-static-block')
        for vacancy in vacancies:
            vacancy_name = vacancy.find('h2', class_='position').text
            vacancy_name = vacancy_name.strip()
            vacancy_href = vacancy.find('a').get('href')
            try:
                b = str(vacancy_href).split('away')
                ref = b[0] + 'desc' + b[1]  # getting full vacancy page in jooble
            except:
                ref = vacancy_href
            time.sleep(2)
            response_two = requests.get(ref)  # open full vacancy page in jooble to get full description
            html_two = response_two.text
            soup_two = BeautifulSoup(html_two, 'lxml')
            description_full = ''
            try:
                reference = soup_two.find('div', class_='bc32c bf012').find('a').get('href')
                response2 = requests.get(reference)  # finding original vacancy link
                html2 = response2.text
                soup2 = BeautifulSoup(html2, 'lxml')

                # get link like Https://www.shine.com/jobs/work-from-home-banking/mumpy-barman/10918498/??vendorid=7071&
                # utm_source=jooble&utm_medium=Organic&utm_campaign=Jooble
                original_link = soup2.find('div', class_='redirect_container').find('a').get('href')
                original_link = 'h' + original_link[1:]
                original_link = original_link.split('utm_source')  # delete jooble from a link
                original_link = original_link[0]
            except:
                reference = ''
            print(reference)
            try:
                full_descriptions = soup_two.find_all('div', class_='a708d')
                for des in full_descriptions:
                    description_full = description_full + (des.text).strip()
                print(description_full)
            except:
                description_full = ''
            try:
                salary = vacancy.find('span', class_='salary').text
            except:
                salary = ''
            try:
                organization = vacancy.find('span', class_='gray_text company-name').text
            except:
                organization = ''
            location = vacancy.find('div', class_='serp_location').find('span').text
            location = location.strip()
            try:
                date = vacancy.find('div', class_='date_from_creation').text
                date = date.strip()
            except:
                date = ''

            #data = {'ID': '',
            #        'Title': vacancy_name,
            #        'Content': description_full,
            #        'Excerpt': '',
            #        'Date': date,
            #        'Post Type': 'job_listing',
            #        'Permalink': reference,
            #        'Image URL': '',
            #        'Image Title': '',
            #        'Image Caption': '',
            #        'Image Description': '',
            #        'Image Alt Text': '',
            #        'Image Featured': '',
            #        'Attachment URL': '',
            #        'Types': '',
            #        'Categories': '',
            #        'Locations': location,
            #        'Tags': '',
            #        '_elementor_controls_usage': '',
            #        '_job_application_deadline_date': '',
            #        '_job_apply_type': '',
            #        '_job_apply_url': vacancy_href,
            #        '_job_apply_email': '',
            #        '_job_salary': salary,
            #        '_job_max_salary': '',
            #        '_job_salary_type': '',
            #        '_job_featured': '',
            #        '_job_urgent': '',
            #        '_job_map_location': '',
            #        '_job_custom_qualification': '',
            #        '_job_address': location,
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
                    'href': ref,
                    'salary': salary,
                    'company': organization,
                    'short_description': description_full,
                    'location': location,
                    'date': date,
                    'full_description': description_full,
                    'company_href': original_link
                    }#
            write_csv(data, filename)
            print(data)


def main():
    f = open('jooble_list', 'r', encoding='utf', newline='')  # getting a list with countries and links
    lines = f.readlines()
    for line in lines:
        line = line.split()
        file_name = 'Jooble_' + line[0]
        reference = line[1]
        searching(file_name, reference)


if __name__ == '__main__':
    main()
