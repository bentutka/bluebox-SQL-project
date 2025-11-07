# Import dependencies
import pyodbc
from matplotlib import pyplot as plt
import seaborn as sns
from tabulate import tabulate
import pandas as pd
import pypandoc

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


# ----------------------------------------------------------------------


POPULAR_MOVIES = """
SELECT TOP 10 
	i.title, 
	COUNT(r.inventory_id) AS "Rentals"
FROM RENTAL_INVENTORY as r

INNER JOIN 
	MOVIES as m
	ON r.inventory_id = m.inventory_id

INNER JOIN 
	INVENTORY as i
	ON m.inventory_id = i.inventory_id

GROUP BY i.title

ORDER BY Rentals DESC"""

POPULAR_GAMES = """
SELECT TOP 10 
	i.title as Title, 
	COUNT(r.inventory_id) AS Rentals
FROM RENTAL_INVENTORY as r

INNER JOIN 
	GAMES as g
	ON r.inventory_id = g.inventory_id

INNER JOIN 
	INVENTORY as i
	ON g.inventory_id = i.inventory_id

GROUP BY i.title

ORDER BY Rentals DESC"""


POPULAR_STUDIO = """
SELECT 
	m.movie_studio as "Studio", 
	COUNT(r.inventory_id) AS "Rentals"
FROM RENTAL_INVENTORY as r

INNER JOIN 
	MOVIES as m
	ON r.inventory_id = m.inventory_id
INNER JOIN 
	INVENTORY as i
	ON m.inventory_id = i.inventory_id
GROUP BY m.movie_studio
ORDER BY Rentals DESC"""

POPULAR_CAST = """
SELECT TOP 10 
	cm.cast_fname as "First Name", 
	cm.cast_lname as "Last Name", 
	cm.role as "Role",
	COUNT(r.inventory_id) AS "Rentals"
FROM RENTAL_INVENTORY as r
INNER JOIN 
	MOVIES as m
	ON r.inventory_id = m.inventory_id
INNER JOIN 
	CAST as c
	ON m.inventory_id = c.inventory_id
INNER JOIN 
	CAST_MEMBERS as cm
	ON c.cast_id = cm.cast_id
GROUP BY cm.cast_fname, cm.cast_lname, cm.role
ORDER BY Rentals DESC"""

POPULAR_ACTORS = """
SELECT TOP 10 
	cm.cast_fname as "First Name", 
	cm.cast_lname as "Last Name", 
	COUNT(r.inventory_id) AS "Rentals"
FROM RENTAL_INVENTORY as r
INNER JOIN 
	MOVIES as m
	ON r.inventory_id = m.inventory_id
INNER JOIN 
	CAST as c
	ON m.inventory_id = c.inventory_id
INNER JOIN 
	CAST_MEMBERS as cm
	ON c.cast_id = cm.cast_id
WHERE cm.role = 'Actor'
GROUP BY cm.cast_fname, cm.cast_lname
ORDER BY Rentals DESC"""

POPULAR_DIRECTORS = """
SELECT TOP 10 
	cm.cast_fname as "First Name", 
	cm.cast_lname as "Last Name", 
	COUNT(r.inventory_id) AS "Rentals"
FROM RENTAL_INVENTORY as r
INNER JOIN 
	MOVIES as m
	ON r.inventory_id = m.inventory_id
INNER JOIN 
	CAST as c
	ON m.inventory_id = c.inventory_id
INNER JOIN 
	CAST_MEMBERS as cm
	ON c.cast_id = cm.cast_id
WHERE cm.role = 'Director'
GROUP BY cm.cast_fname, cm.cast_lname
ORDER BY Rentals DESC"""

POPULAR_WRITERS = """
SELECT TOP 10 
	cm.cast_fname as "First Name", 
	cm.cast_lname as "Last Name", 
	COUNT(r.inventory_id) AS "Rentals"
FROM RENTAL_INVENTORY as r
INNER JOIN 
	MOVIES as m
	ON r.inventory_id = m.inventory_id
INNER JOIN 
	CAST as c
	ON m.inventory_id = c.inventory_id
INNER JOIN 
	CAST_MEMBERS as cm
	ON c.cast_id = cm.cast_id
WHERE cm.role = 'Writer'
GROUP BY cm.cast_fname, cm.cast_lname
ORDER BY Rentals DESC"""


# ----------------------------------------------------------------------


# General inventory queries

UTILIZED_VENDORS = """
SELECT TOP 10 
    v.vendor_name, 
    SUM(o.item_quantity) AS "Quantity",
    SUM(o.total_price) as "Total Cost"
FROM VENDORS AS v

INNER JOIN 
    ORDERS AS o ON 
    v.vendor_id = o.vendor_id
GROUP BY v.vendor_name
ORDER BY Quantity DESC"""

# Most popular movie from each vendor
VENDOR_MOVIE = """
SELECT
    v.vendor_name,
    i.title as most_popular_movie,
    COUNT(r.inventory_id) AS Quantity
FROM RENTAL_INVENTORY AS r

INNER JOIN 
    MOVIES AS m 
    ON r.inventory_id = m.inventory_id
INNER JOIN 
    INVENTORY AS i 
    ON m.inventory_id = i.inventory_id
INNER JOIN 
    ORDERS AS o
    ON i.inventory_id = o.inventory_id
INNER JOIN 
    VENDORS AS v 
    ON o.vendor_id = v.vendor_id

GROUP BY v.vendor_id, v.vendor_name, i.title
HAVING COUNT(r.inventory_id) = (
    SELECT MAX(movie_rentals)
    FROM (SELECT
            v.vendor_id,
            COUNT(r.inventory_id) AS movie_rentals
        FROM RENTAL_INVENTORY AS r
        INNER JOIN 
            MOVIES AS m 
            ON r.inventory_id = m.inventory_id
        INNER JOIN 
            INVENTORY AS i 
            ON m.inventory_id = i.inventory_id
        INNER JOIN 
            ORDERS AS o 
            ON i.inventory_id = o.inventory_id
        INNER JOIN 
            VENDORS AS v 
            ON o.vendor_id = v.vendor_id
        GROUP BY v.vendor_id, i.title
    ) AS subquery
    WHERE subquery.vendor_id = v.vendor_id
)
ORDER BY Quantity DESC"""

# ----------------------------------------------------------------------

# Most popular game from each vendor
VENDOR_GAME = """
SELECT
    v.vendor_name,
    i.title as most_popular_game,
    COUNT(r.inventory_id) AS Quantity
FROM RENTAL_INVENTORY AS r
INNER JOIN GAMES AS g ON r.inventory_id = g.inventory_id
INNER JOIN INVENTORY AS i ON g.inventory_id = i.inventory_id
INNER JOIN ORDERS AS o ON i.inventory_id = o.inventory_id
INNER JOIN VENDORS AS v ON o.vendor_id = v.vendor_id
GROUP BY v.vendor_id, v.vendor_name, i.title
HAVING COUNT(r.inventory_id) = (
    SELECT MAX(game_rentals)
    FROM (
        SELECT
            v.vendor_id,
            COUNT(r.inventory_id) AS game_rentals
        FROM RENTAL_INVENTORY AS r
        INNER JOIN GAMES AS g ON r.inventory_id = g.inventory_id
        INNER JOIN INVENTORY AS i ON g.inventory_id = i.inventory_id
        INNER JOIN ORDERS AS o ON i.inventory_id = o.inventory_id
        INNER JOIN VENDORS AS v ON o.vendor_id = v.vendor_id
        GROUP BY v.vendor_id, i.title
    ) AS subquery
    WHERE subquery.vendor_id = v.vendor_id
)
ORDER BY Quantity DESC"""

# Top genres from each vendor
VENDOR_GENRE = """
SELECT
    v.vendor_name,
    g.genre_desc AS top_genre,
    COUNT(*) AS Quantity
FROM RENT AS r
INNER JOIN INVENTORY AS i ON r.inventory_id = i.inventory_id
INNER JOIN MOVIE_GENRE AS mg ON i.inventory_id = mg.inventory_id
INNER JOIN GENRE AS g ON mg.genre_id = g.genre_id
INNER JOIN ORDERS AS o ON i.inventory_id = o.inventory_id
INNER JOIN VENDORS AS v ON o.vendor_id = v.vendor_id
GROUP BY v.vendor_id, v.vendor_name, g.genre_desc
HAVING COUNT(*) = (
    SELECT MAX(genre_rentals)
    FROM (
        SELECT
            v.vendor_id,
            g.genre_desc,
            COUNT(*) AS genre_rentals
        FROM RENT AS r
        INNER JOIN INVENTORY AS i ON r.inventory_id = i.inventory_id
        INNER JOIN MOVIE_GENRE AS mg ON i.inventory_id = mg.inventory_id
        INNER JOIN GENRE AS g ON mg.genre_id = g.genre_id
        INNER JOIN ORDERS AS o ON i.inventory_id = o.inventory_id
        INNER JOIN VENDORS AS v ON o.vendor_id = v.vendor_id
        GROUP BY v.vendor_id, g.genre_desc
    ) AS subquery
    WHERE subquery.vendor_id = v.vendor_id
)
ORDER BY Quantity DESC"""


# Top types from each vendor
VENDOR_TYPE = """
SELECT
    v.vendor_name,
    t.type_desc AS top_type,
    COUNT(*) AS Quantity
FROM RENT AS r
INNER JOIN INVENTORY AS i ON r.inventory_id = i.inventory_id
INNER JOIN GAME_TYPE AS gt ON i.inventory_id = gt.inventory_id
INNER JOIN TYPE AS t ON gt.type_id = t.type_id
INNER JOIN ORDERS AS o ON i.inventory_id = o.inventory_id
INNER JOIN VENDORS AS v ON o.vendor_id = v.vendor_id
GROUP BY v.vendor_id, v.vendor_name, t.type_desc
HAVING COUNT(*) = (
    SELECT MAX(type_rentals)
    FROM (
        SELECT
            v.vendor_id,
            t.type_desc,
            COUNT(*) AS type_rentals
        FROM RENT AS r
        INNER JOIN INVENTORY AS i ON r.inventory_id = i.inventory_id
        INNER JOIN GAME_TYPE AS gt ON i.inventory_id = gt.inventory_id
        INNER JOIN TYPE AS t ON gt.type_id = t.type_id
        INNER JOIN ORDERS AS o ON i.inventory_id = o.inventory_id
        INNER JOIN VENDORS AS v ON o.vendor_id = v.vendor_id
        GROUP BY v.vendor_id, t.type_desc
    ) AS subquery
    WHERE subquery.vendor_id = v.vendor_id
)
ORDER BY Quantity DESC"""



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

def list_to_md_table(lst):
    markdown = tabulate(lst[1:], tablefmt="pipe", numalign="left", headers=lst[0])
    return markdown

def general_marketing_report(file = 'marketing_report.md') :
    colors = sns.color_palette("Blues")
    plt.style.use('ggplot')

    customer_gender = process_query_two_way(CUSTOMER_GENDER)
    customer_gender_df = pd.DataFrame(customer_gender[1:], columns=customer_gender[0])
    plt.pie(customer_gender_df['Count'], labels= customer_gender_df['Gender'], colors = colors,
             autopct='%.0f%%')
    plt.title("Customer Gender Breakdown")
    plt.savefig('gender_plot.png')
    plt.clf()

    # Customer age range overview
    customer_age_range = process_query_two_way(CUSTOMER_AGE_RANGE)
    customer_age_df = pd.DataFrame(customer_age_range[1:], columns=customer_age_range[0])
    plt.pie(customer_age_df['Count'], labels= customer_age_df['Age_Range'],colors = colors,
             autopct='%.0f%%')
    plt.title("Customer Age Breakdown")
    plt.savefig('age_plot.png')
    plt.clf()

    # Genre popularity
    genre_popularity = process_query_two_way(GENRE_POPULARITY)
    genre_popularity_df = pd.DataFrame(genre_popularity[1:], columns=genre_popularity[0])
    plt.pie(genre_popularity_df['Count of Movies Currently Rented Out'], labels = genre_popularity_df['Genre'],
             colors = colors, autopct='%.0f%%')
    plt.title("Current Genre Popularity")
    plt.savefig('genre_plot.png')
    plt.clf()

    # Type popularity
    type_popularity = process_query_two_way(TYPE_POPULARITY)
    type_popularity_df = pd.DataFrame(type_popularity[1:], columns=type_popularity[0])
    plt.style.use('bmh')
    plt.pie(type_popularity_df['Count of Games Currently Rented Out'], labels=type_popularity_df['Game Type'],
             colors = colors, autopct='%.0f%%')
    plt.title("Current Game Type Popularity")
    plt.savefig('type_plot.png')
    plt.clf()

    with open(file, 'w') as f:
        f.write('# General Marketing Report \n')
        f.write('## Customer Demographics Overview \n')
        f.write('### Customer Gender Breakdown \n')
        f.write(list_to_md_table(customer_gender))
        f.write('\n \n ![Gender Breakdown](gender_plot.png)') # Adding the image using Markdown syntax
        f.write('\n ### Customer Age Breakdown \n')
        f.write(list_to_md_table(customer_age_range))
        f.write('\n \n ![Age Breakdown](age_plot.png)')
        f.write('\n --- \n')
        f.write('\n ## Item Popularity Overview \n')
        f.write('### Movies \n')
        f.write(list_to_md_table(genre_popularity))
        f.write('\n \n ![Genre Popularity](genre_plot.png)')
        f.write('\n ### Video Games \n')
        f.write(list_to_md_table(type_popularity))
        f.write('\n \n ![Type Popularity](type_plot.png) \n \n')

    #md = Path(file)
    #doxc = md.with_suffix('.docx')
    #pypandoc.convert_file(md, 'docx', outputfile=doxc)

def query_product_specific(product, region = '*', genre = '*', gender = '*', age = '*') :
    region_query = ''
    genre_query = ''
    gender_query = ''
    age_query = ''
        
    if region != '*' :
        region_query = "z.region = '%s'" % region
    
    if genre != '*':
        if product == 'DVD' :
            genre_query = "g.genre_desc = '%s'" % genre
        elif product == 'Video Game' :
            genre_query = "t.type_desc = '%s'" % genre
        
    if gender == 'Male' :
        gender_query = "c.customer_gender = 'M'"
    else : gender_query = "c.customer_gender = 'F'"
        
    if age != '*' :
        age_query = "c.customer_age_range = '%s'" % age
        
    queries = [region_query, genre_query, gender_query, age_query]
        
    master_query = ''

    for i in queries:
        if i != '':
            master_query = master_query + i + ' AND '

    while master_query.endswith('AND ') or master_query.endswith(' AND ') or master_query.endswith(' AND') or master_query.endswith('AND'):
        master_query = master_query[:-4]

    return master_query

def query_product_nonspecific(region = '*', gender = '*', age = '*') :
    region_query = ''
    genre_query = ''
    gender_query = ''
    age_query = ''
        
    if region != '*' :
        region_query = "z.region = '%s'" % region

    if gender == 'Male' :
        gender_query = "c.customer_gender = 'M'"
    else : gender_query = "c.customer_gender = 'F'"
        
    if age != '*' :
        age_query = "c.customer_age_range = '%s'" % age
        
    queries = [region_query, genre_query, gender_query, age_query]
        
    master_query = ''

    for i in queries:
        if i != '':
            master_query = master_query + i + ' AND '

    while master_query.endswith('AND ') or master_query.endswith(' AND ') or master_query.endswith(' AND') or master_query.endswith('AND'):
        master_query = master_query[:-4]

    return master_query

def user_marketing_report(product, file = 'marketing_report.md', region = '*', 
                          genre = '*', gender = '*', age = '*') :
    
    if ((region == '*') and (product == '*') and (genre == '*') and (gender == '*') and (age == '*')):
        general_marketing_report()

    where_clause = query_product_specific(product, region, genre, gender, age)

    USER_TYPE = """
            SELECT t.type_desc as Type, COUNT(*) as Count
            FROM ZIP as z
            INNER JOIN CUSTOMER as c ON z.zip_code = c.customer_zip_code
            INNER JOIN RENT as r ON c.customer_id = r.customer_id
            INNER JOIN INVENTORY as i ON r.inventory_id = i.inventory_id
            INNER JOIN GAME_TYPE as gt ON i.inventory_id = gt.inventory_id
            INNER JOIN TYPE AS t ON gt.type_id = t.type_id
            WHERE {}
            GROUP BY t.type_desc
            """.format(where_clause)
    USER_GENRE = """
                SELECT g.genre_desc as Genre, COUNT(*) as Count
                FROM ZIP as z
                INNER JOIN CUSTOMER as c ON z.zip_code = c.customer_zip_code
                INNER JOIN RENT as r ON c.customer_id = r.customer_id
                INNER JOIN INVENTORY as i ON r.inventory_id = i.inventory_id
                INNER JOIN MOVIE_GENRE as mg ON i.inventory_id = mg.inventory_id
                INNER JOIN GENRE AS g ON mg.genre_id = g.genre_id
                WHERE {}
            GROUP BY g.genre_desc
                """.format(where_clause)
    
    if product == 'Video Game' :
        data = process_query_two_way(USER_TYPE)
    elif product == 'DVD' :
        data = process_query_two_way(USER_GENRE)
    else : print('error')

    with open(file, 'w') as f:
        f.write('# User Marketing Report \n')
        f.write(list_to_md_table(data))

def general_inventory_report(file = 'inventory_report.md') :
    colors = sns.color_palette("Blues")
    plt.style.use('ggplot')

    popular_movies = process_query_two_way(POPULAR_MOVIES)
    popular_games = process_query_two_way(POPULAR_GAMES)
    popular_studio = process_query_two_way(POPULAR_STUDIO)
    popular_cast = process_query_two_way(POPULAR_CAST)
    popular_actors = process_query_two_way(POPULAR_ACTORS)
    popular_directors = process_query_two_way(POPULAR_DIRECTORS)
    popular_writers = process_query_two_way(POPULAR_WRITERS)

    popular_studio_df = pd.DataFrame(popular_studio[1:], columns=popular_studio[0])
    plt.pie(popular_studio_df['Rentals'], labels=popular_studio_df['Studio'],
             colors = colors, autopct='%.0f%%')
    plt.title("Current Game Type Popularity")
    plt.savefig('studio_plot.png')
    plt.clf()

    with open(file, 'w') as f:
        f.write('# General Inventory Report \n')
        f.write('## Popular Items Overview \n')
        f.write('### Popular Movies \n')
        f.write(list_to_md_table(popular_movies))
        f.write('\n \n ### Popular Video Games \n')
        f.write(list_to_md_table(popular_games))
        f.write('\n \n ## Popular Studios \n')
        f.write(list_to_md_table(popular_studio))
        f.write('\n \n ![Studio Plot](studio_plot.png) \n \n')
        f.write('\n \n ## Popular Cast Members \n')
        f.write(list_to_md_table(popular_cast))
        f.write('\n \n ### Popular Writers \n')
        f.write(list_to_md_table(popular_writers))
        f.write('\n \n ### Popular Actors \n')
        f.write(list_to_md_table(popular_actors))
        f.write('\n \n ### Popular Directors \n')
        f.write(list_to_md_table(popular_directors))

def user_inventory_report(file = 'inventory.md', region = '*', 
                          genre = '*', gender = '*', age = '*') :
    
    if ((region == '*') and (genre == '*') and (gender == '*') and (age == '*')):
        general_inventory_report()

    where_clause = query_product_nonspecific(region, gender, age)

    POPULAR_CAST_USER = """
        SELECT TOP 10 
            cm.cast_fname as "First Name", 
            cm.cast_lname as "Last Name", 
            cm.role as "Role",
            COUNT(ri.inventory_id) AS "Rentals"
        FROM RENTAL_INVENTORY as ri

        INNER JOIN 
            MOVIES as m
            ON ri.inventory_id = m.inventory_id
        INNER JOIN 
            CAST as cast
            ON m.inventory_id = cast.inventory_id
        INNER JOIN 
            CAST_MEMBERS as cm
            ON cast.cast_id = cm.cast_id
        INNER JOIN 
            RENT as r
            ON ri.inventory_id = r.inventory_id
        INNER JOIN 
            CUSTOMER as c
            ON r.customer_id = c.customer_id
        INNER JOIN
            ZIP as z
            ON c.customer_zip_code = z.zip_code

        WHERE {}

        GROUP BY cm.cast_fname, cm.cast_lname, cm.role
        ORDER BY Rentals DESC
        """.format(where_clause)
    
    popular_cast_user = process_query_two_way(POPULAR_CAST_USER)
    print(popular_cast_user)

    with open(file, 'w') as f:
        f.write('# User Marketing Report \n')
        f.write(list_to_md_table(popular_cast_user))

def general_vendor_report(file = 'vendor_report.md') :
    utilized_vendors = process_query_two_way(UTILIZED_VENDORS)
    vendor_movie = process_query_two_way(VENDOR_MOVIE)
    vendor_game = process_query_two_way(VENDOR_GAME)
    vendor_genre = process_query_two_way(VENDOR_GENRE)
    vendor_type = process_query_two_way(VENDOR_TYPE)

    with open(file, 'w') as f:
        f.write('# General Vendor Report \n')
        f.write('## Our Most Utilized Vendors \n')
        f.write(list_to_md_table(utilized_vendors))
        f.write('\n \n ## Popular Items from Each Vendor \n')
        f.write('### Vendors Popular Movies \n')
        f.write(list_to_md_table(vendor_movie))
        f.write("\n \n ### Vendors' Popular Games \n")
        f.write(list_to_md_table(vendor_game))
        f.write("\n \n ### Vendors' Popular Genres \n")
        f.write(list_to_md_table(vendor_genre))
        f.write("\n \n ### Vendors' Popular Game Types \n")
        f.write(list_to_md_table(vendor_type))


def management_report() :
  while True:
    print('\n ------------------------- \n')

    print('Select a reporting department, or quit.')
    print(' 0. Quit')
    print(' 1. Marketing')
    print(' 2. Inventory')
    print(' 3. Vendors')
    print('> ', end='')

    choice = input()

    match choice:
      case '0' : break
      case '1' :
        print('Would you like to generate a general report, or input parameters?')
        print( '0. Quit')
        print(' 1. General')
        print(' 2. Input Parameters')

        marketing_choice = input()

        match marketing_choice :
          case '0' : break
          case '1' :
            print('Generating general marketing report...')
            general_marketing_report(file = 'marketing.md')
            print('Done! File name: marketing.md')
          case '2' :

            # Pick product type
            product_chosen = False
            while product_chosen == False :

              print('Select a product: ')
              print(' 0. Quit')
              print(' 1. DVDs')
              print(' 2. Video Games')

              product_choice = input()

              match product_choice:
                case '0' : break
                case '1' :
                  product = 'DVD'
                  product_chosen = True
                case '2' :
                  product = 'Video Games'
                  product_chosen = True
                case _ : print(f'Error: Unrecognized option: {product_choice}.')

            # Pick region
            region_chosen = False
            while region_chosen == False :
              print('Select a region: ')
              print(' 0. Quit')
              print(' 1. Southern')
              print(' 2. Central')
              print(' 3. West Pacific')
              print(' 4. Atlantic')
              print(' 5. All')

              region_choice = input()

              match region_choice:
                case '0' : break
                case '1' :
                  region = 'SOUTHERN'
                  region_chosen = True
                case '2' :
                  region = 'CENTRAL'
                  region_chosen = True
                case '3' :
                  region = 'WESTPAC'
                  region_chosen = True
                case '4' :
                  region = 'ATLATIC'
                  region_chosen = True
                case '5' :
                  region = '*'
                  region_chosen = True
                case _ : print(f'Error: Unrecognized option: {region_choice}.')

              gender_chosen = False
              while gender_chosen == False :

                print('Select a gender: ')
                print(' 0. Quit')
                print(' 1. Male')
                print(' 2. Female')
                print(' 3. All')

                gender_choice = input()

                match gender_choice :
                  case '0' : break
                  case '1' :
                    gender = 'M'
                    gender_chosen = True
                  case '2' :
                    gender = 'F'
                    gender_chosen = True
                  case '3' :
                    gender = '*'
                    gender_chosen = True
                  case _ : print(f'Error: Unrecognized option: {gender_choice}.')

              age_chosen = False
              while age_chosen == False :

                print('Select a age range: ')
                print(' 1. Under 18')
                print(' 2. 18-24')
                print(' 3. 25-34')
                print(' 4. 35-44')
                print(' 5. 45-54')
                print(' 6. 55-64')
                print(' 7. 65+')

                age_choice = input()

                match age_choice :
                  case '0' : break
                  case '1' :
                    age = 'Under 18'
                    age_chosen = True
                  case '2' :
                    age = '18-24'
                    age_chosen = True
                  case '3' :
                    age = '25-34'
                    age_chosen = True
                  case '4' :
                    age = '35-44'
                    age_chosen = True
                  case '5' :
                    age = '45-54'
                    age_chosen = True
                  case '6' :
                    age = '55-64'
                    age_chosen = True
                  case '7' :
                    age = '65+'
                    age_chosen = True
                  case _ : print(f'Error: Unrecognized option: {age_choice}.')

            print(f'User marketing report: {product}, {region}, {gender}, {age}')
            print('Generating user marketing report...')
            user_marketing_report(product = product, file = 'marketing.md', region = region,
                                  gender = gender, age = age)
            print('Done! File name: marketing.md')

      case '2' :
        print('Generating inventory report...')
        general_inventory_report(file = 'inventory.md')
        print('Done! File name: inventory.md')
      case '3':
        print('Generating inventory report...')
        general_vendor_report(file = 'vendor.md')
        print('Done! File name: vendor.md')
      case _ : print(f'Error: Unrecognized option: {choice}.')

#anagement_report()
management_report()

cursor.close()
conn.close()



