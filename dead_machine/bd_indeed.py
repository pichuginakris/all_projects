import psycopg2
import csv


def creating_bd(country):
    try:
        connect_str = "dbname='hey' user='postgres' password='qwerty' host='localhost'"
        # use our connection values to establish a connection
        conn = psycopg2.connect(connect_str)
        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
        # create a new table with a single column called "name"
       # cursor.execute("DROP TABLE " + country + ";")
        conn.commit()
        #cursor.execute("""CREATE TABLE """ + country + """ (
        #            vacancy char(20000),
        #            link_to_a_vacancy char(20000),
        #            salary char(20000),
        #            company char(20000),
        #            short_description char(20000),
        #            location char(20000),
        #            date_from_creation char(10000),
        #            full_description char(30000),
        #            link_to_a_company char(20000)
        #            );""")
        conn.commit()
        with open(country + '.csv', encoding='utf-8') as file:
            order = ['Vacancy', 'Link to a vacancy', 'Salary', 'Company', 'Short description', 'Location',
                     'Date from creation', 'Full description', 'Link to a company']
            reader = csv.DictReader(file)
            number_of_lines = list(reader)
            for line in number_of_lines:
                try:
                    print(line)
                    cursor.execute("INSERT INTO tables_" + country + "(vacancy, link_to_a_vacancy, salary, company, " +
                                                              "short_description, location, date_from_creation, " +
                                                              "full_description, link_to_a_company) values (" +
                                   "'" + (line['Vacancy']).replace("'", "") + "','" + (line['Link to a vacancy']).replace("'", "")
                                   + "','" + (line['Salary']).replace("'", "") + "','" + (line['Company']).replace("'", "")
                                   + "','" + (line['Short description']).replace("'", "") + "','" +
                                   (line['Location']).replace("'", "") + "','" + (line['Date from creation']).replace("'", "") + "','" +
                                   (line['Full description']).replace("'", "") + "','" + (line['Link to a company']).replace("'", "") + "')")
                    conn.commit()
                except Exception as e:
                    print(e)
        cursor.close()
        conn.close()
    except Exception as ex:
        print(ex)


def main():
    list_of_countries = ['India']
   # list_of_countries = ['India', 'Philippines', 'Malaysia', 'Canada', 'New_Zealand', 'Australia', 'Nigeria',
    #                     'South_Africa', 'United_Kingdom', 'Ireland', 'Singapore', 'Pakistan', 'USA']

    for country in list_of_countries:
        country = 'Indeed_' + country
        creating_bd(country)


if __name__ == '__main__':
    main()