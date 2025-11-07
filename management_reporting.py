# Import dependencies
import pyodbc
from matplotlib import pyplot as plt 
from tabulate import tabulate
import markdown
import pandas as pd

# Instantiate SQL connection
SERVER = 'essql1.walton.uark.edu'
DATABASE = 'ISYS_Spring2024_Nolan_ruthw_db'
USERNAME = 'ruthw'
PASSWORD = 'ISYSPass10997203!'

# Specify the ODBC driver (e.g., SQL Server Native Client)
driver = '{SQL Server}'

# Connection string
conn_str = (
    'DRIVER=' + driver + ';'
    'SERVER=essql1.walton.uark.edu;'
    'DATABASE=ISYS_Spring2024_Nolan_ruthw_db;'
    'UID=ruthw;'
    'PWD=ISYSPass10997203!;'
    'Trusted_Connection=no;'
)

# Establishing the connection
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

def process_query_dict(QUERY) :
    data = {}

    cursor.execute(QUERY)

    for row in cursor.fetchall():
        data[row[0]] = row[1]

    return data

def process_query_two_way(QUERY) :
    cursor.execute(QUERY)

    column_names = [column[0] for column in cursor.description]

    data = [column_names]

    for row in cursor.fetchall():
        results = []
        for i in range(len(row)) :
            results.append(row[i])
        data.append(results)

    return data

def bar_chart_query(data, chart_title, chart_x, chart_y = "Count") :
    plt.figure(figsize=(6, 6))
    plt.subplots_adjust(bottom=0.25)
    plt.bar(data.keys(), data.values(), color='cornflowerblue')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel(chart_x)
    plt.ylabel(chart_y)
    plt.title(chart_title)
    plt.style.use('seaborn-v0_8')

    plt.show()

def list_to_md_table(lst):
    markdown = tabulate(lst[1:], tablefmt="pipe", numalign="left", headers=lst[0])
    return markdown

def dict_to_md_table(dict):
    markdown = tabulate(list(dict.values()), tablefmt="pipe", numalign="left", headers=list(dict.keys()))
    return markdown


CUSTOMER_GENDER = """
SELECT CUSTOMER.customer_gender as "Gender", COUNT(*) as "Count"
FROM CUSTOMER
GROUP BY CUSTOMER.customer_gender
"""

CUSTOMER_AGE_RANGE = """
SELECT CUSTOMER.customer_age_range as "Age_Range", COUNT(*) as "Count"
FROM CUSTOMER
GROUP BY CUSTOMER.customer_age_range
"""

CUSTOMER_MEMBERSHIP = """
SELECT m.membership_status_desc as Membership, COUNT(*) as "Count
FROM CUSTOMER as c
INNER JOIN
    MEMBERSHIP as m ON c.membership_status_id = m.membership_status_id
GROUP BY Membership
"""

GENRE_POPULARITY = """
SELECT g.genre_desc as "Genre", COUNT(*) as "Count of Movies Currently Rented Out"
FROM RENT as r

INNER JOIN
INVENTORY as i
ON r.inventory_id = i.inventory_id

INNER JOIN
MOVIE_GENRE as mg
ON i.inventory_id = mg.inventory_id

INNER JOIN
GENRE AS g
ON mg.genre_id = g.genre_id

GROUP BY g.genre_desc
"""

TYPE_POPULARITY = """
SELECT t.type_desc as "Game Type", COUNT(*) as "Count of Games Currently Rented Out"
FROM RENT as r

INNER JOIN
INVENTORY as i
ON r.inventory_id = i.inventory_id

INNER JOIN
GAME_TYPE as gt
ON i.inventory_id = gt.inventory_id

INNER JOIN
TYPE AS t
ON gt.type_id = t.type_id

GROUP BY t.type_desc
"""

MEMBERSHIP_STATUS_BY_GENDER = """"
SELECT
	m.membership_status_desc AS "Membership", 
    SUM(CASE WHEN c.customer_gender = 'M' THEN 1 ELSE 0 END) AS "Men",
    SUM(CASE WHEN c.customer_gender = 'F' THEN 1 ELSE 0 END) AS "Women"
FROM CUSTOMER as c

INNER JOIN
    MEMBERSHIP as m 
    ON c.membership_status_id = m.membership_status_id

GROUP BY m.membership_status_desc
"""

MEMBERSHIP_STATUS_BY_AGE = """ 
SELECT
	m.membership_status_desc AS "Membership", 
    SUM(CASE WHEN c.customer_age_range = 'Under 18' THEN 1 ELSE 0 END) AS "Under 18",
    SUM(CASE WHEN c.customer_age_range = '18-24' THEN 1 ELSE 0 END) AS "18-24",
	SUM(CASE WHEN c.customer_age_range = '25-34' THEN 1 ELSE 0 END) AS "25-34",
	SUM(CASE WHEN c.customer_age_range = '35-44' THEN 1 ELSE 0 END) AS "35-44",
	SUM(CASE WHEN c.customer_age_range = '45-54' THEN 1 ELSE 0 END) AS "45-54",
	SUM(CASE WHEN c.customer_age_range = '55-64' THEN 1 ELSE 0 END) AS "55-64",
	SUM(CASE WHEN c.customer_age_range = '65+' THEN 1 ELSE 0 END) AS "65+"
FROM 
    CUSTOMER as c
INNER JOIN
    MEMBERSHIP as m ON c.membership_status_id = m.membership_status_id
GROUP BY 
    m.membership_status_desc;
"""

TYPE_BY_GENDER = """
SELECT
	t.type_desc as "Game Type", 
    SUM(CASE WHEN c.customer_gender = 'M' THEN 1 ELSE 0 END) AS "Men",
    SUM(CASE WHEN c.customer_gender = 'F' THEN 1 ELSE 0 END) AS "Women"
FROM CUSTOMER as c

INNER JOIN
RENT as r
ON c.customer_id = r.customer_id

INNER JOIN
INVENTORY as i
ON r.inventory_id = i.inventory_id

INNER JOIN
GAME_TYPE as gt
ON i.inventory_id = gt.inventory_id

INNER JOIN
TYPE AS t
ON gt.type_id = t.type_id

GROUP BY t.type_desc"""

GENRE_BY_GENDER = """
SELECT
	g.genre_desc as "Genre", 
    SUM(CASE WHEN c.customer_gender = 'M' THEN 1 ELSE 0 END) AS "Men",
    SUM(CASE WHEN c.customer_gender = 'F' THEN 1 ELSE 0 END) AS "Women"
FROM CUSTOMER as c

INNER JOIN
RENT as r
ON c.customer_id = r.customer_id

INNER JOIN
INVENTORY as i
ON r.inventory_id = i.inventory_id

INNER JOIN
MOVIE_GENRE as mg
ON i.inventory_id = mg.inventory_id

INNER JOIN
GENRE AS g
ON mg.genre_id = g.genre_id

GROUP BY g.genre_desc"""

TYPE_BY_AGE = """
SELECT
	t.type_desc AS "Type", 
    SUM(CASE WHEN c.customer_age_range = 'Under 18' THEN 1 ELSE 0 END) AS "Under 18",
    SUM(CASE WHEN c.customer_age_range = '18-24' THEN 1 ELSE 0 END) AS "18-24",
	SUM(CASE WHEN c.customer_age_range = '25-34' THEN 1 ELSE 0 END) AS "25-34",
	SUM(CASE WHEN c.customer_age_range = '35-44' THEN 1 ELSE 0 END) AS "35-44",
	SUM(CASE WHEN c.customer_age_range = '45-54' THEN 1 ELSE 0 END) AS "45-54",
	SUM(CASE WHEN c.customer_age_range = '55-64' THEN 1 ELSE 0 END) AS "55-64",
	SUM(CASE WHEN c.customer_age_range = '65+' THEN 1 ELSE 0 END) AS "65+"
FROM 
    CUSTOMER as c

INNER JOIN
RENT as r
ON c.customer_id = r.customer_id

INNER JOIN
INVENTORY as i
ON r.inventory_id = i.inventory_id

INNER JOIN
GAME_TYPE as gt
ON i.inventory_id = gt.inventory_id

INNER JOIN
TYPE AS t
ON gt.type_id = t.type_id

GROUP BY t.type_desc
"""

GENRE_BY_AGE = """
SELECT
	g.genre_desc AS "Type", 
    SUM(CASE WHEN c.customer_age_range = 'Under 18' THEN 1 ELSE 0 END) AS "Under 18",
    SUM(CASE WHEN c.customer_age_range = '18-24' THEN 1 ELSE 0 END) AS "18-24",
	SUM(CASE WHEN c.customer_age_range = '25-34' THEN 1 ELSE 0 END) AS "25-34",
	SUM(CASE WHEN c.customer_age_range = '35-44' THEN 1 ELSE 0 END) AS "35-44",
	SUM(CASE WHEN c.customer_age_range = '45-54' THEN 1 ELSE 0 END) AS "45-54",
	SUM(CASE WHEN c.customer_age_range = '55-64' THEN 1 ELSE 0 END) AS "55-64",
	SUM(CASE WHEN c.customer_age_range = '65+' THEN 1 ELSE 0 END) AS "65+"
FROM 
    CUSTOMER as c

INNER JOIN
RENT as r
ON c.customer_id = r.customer_id
    
INNER JOIN
INVENTORY as i
ON r.inventory_id = i.inventory_id

INNER JOIN
MOVIE_GENRE as mg
ON i.inventory_id = mg.inventory_id

INNER JOIN
GENRE AS g
ON mg.genre_id = g.genre_id

GROUP BY g.genre_desc
"""

customer_gender = process_query_two_way(CUSTOMER_GENDER)
customer_age_range = process_query_two_way(CUSTOMER_AGE_RANGE)
#customer_membership = process_query_two_way(CUSTOMER_MEMBERSHIP)
genre_popularity = process_query_two_way(GENRE_POPULARITY)
type_popularity = process_query_two_way(TYPE_POPULARITY)

membership_by_age = process_query_two_way(MEMBERSHIP_STATUS_BY_AGE)
#membership_by_gender = process_query_two_way(MEMBERSHIP_STATUS_BY_GENDER)


type_by_gender = process_query_two_way(TYPE_BY_GENDER)
genre_by_gender = process_query_two_way(GENRE_BY_GENDER)

type_by_age = process_query_two_way(TYPE_BY_AGE)
genre_by_age = process_query_two_way(GENRE_BY_AGE)


customer_gender_df = pd.DataFrame()
plt.figure(figsize=(6, 6))
plt.pie(customer_gender[1], labels=customer_gender[0], autopct='%.0f%%')
#plt.xlabel(chart_x)
#plt.ylabel(chart_y)
#plt.title(chart_title)
plt.style.use('seaborn-v0_8')

plt.savefig('gender_plot.png')

with open('sample.md', 'w') as f:
    f.write('# General Marketing Report \n')
    f.write('## Customer Demographics Overview \n')
    f.write('### Customer Gender Breakdown \n')
    f.write(list_to_md_table(customer_gender))
    f.write('![Gender Plot](gender_plot.png)\n')  # Adding the image using Markdown syntax
    f.write('\n ### Customer Age Breakdown \n')
    f.write(list_to_md_table(customer_age_range))
    f.write('\n ## Item Popularity Overview \n')
    f.write('### Movies \n')
    f.write(list_to_md_table(genre_popularity))
    f.write('\n ### Video Games \n')
    f.write(list_to_md_table(type_popularity))

#print(dict_to_md_table(customer_age_range))

cursor.close()
conn.close()

