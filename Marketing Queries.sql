-- General marketing queries

-- Customer demographic information
-- CUSTOMER_GENDER 
SELECT CUSTOMER.customer_gender as "Gender", COUNT(*) as "Count"
FROM CUSTOMER
GROUP BY CUSTOMER.customer_gender

----------------------------------------------------------------------

-- CUSTOMER_AGE_RANGE 
SELECT CUSTOMER.customer_age_range as "Age_Range", COUNT(*) as "Count"
FROM CUSTOMER
GROUP BY CUSTOMER.customer_age_range

----------------------------------------------------------------------

-- CUSTOMER_MEMBERSHIP  
SELECT m.membership_status_desc as Membership, COUNT(*) as "Count"
FROM CUSTOMER as c
INNER JOIN
    MEMBERSHIP as m 
    ON c.membership_status_id = m.membership_status_id
GROUP BY m.membership_status_desc

----------------------------------------------------------------------

-- CUSTOMER REGION
SELECT z.region as "Region", COUNT(*) as "Count"
FROM CUSTOMER as c

INNER JOIN
	ZIP as z
	ON c.customer_zip_code = z.zip_code

GROUP BY z.region



----------------------------------------------------------------------
----------------------------------------------------------------------



-- Type and genre rental popularity
-- GENRE_POPULARITY 
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

----------------------------------------------------------------------

-- TYPE_POPULARITY 
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



----------------------------------------------------------------------
----------------------------------------------------------------------



-- Membership status
-- MEMBERSHIP_STATUS_BY_GENDER 
SELECT
	m.membership_status_desc AS "Membership", 
    SUM(CASE WHEN c.customer_gender = 'M' THEN 1 ELSE 0 END) AS "Men",
    SUM(CASE WHEN c.customer_gender = 'F' THEN 1 ELSE 0 END) AS "Women"
FROM CUSTOMER as c

INNER JOIN
    MEMBERSHIP as m 
    ON c.membership_status_id = m.membership_status_id

GROUP BY m.membership_status_desc

----------------------------------------------------------------------

-- MEMBERSHIP_STATUS_BY_AGE 
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

----------------------------------------------------------------------

-- MEMBERSHIP_STATUS_BY_LOCATION
SELECT 
    z.region as "Region",
    SUM(CASE WHEN c.customer_age_range = 'Under 18' THEN 1 ELSE 0 END) AS "Under 18",
    SUM(CASE WHEN c.customer_age_range = '18-24' THEN 1 ELSE 0 END) AS "18-24",
	SUM(CASE WHEN c.customer_age_range = '25-34' THEN 1 ELSE 0 END) AS "25-34",
	SUM(CASE WHEN c.customer_age_range = '35-44' THEN 1 ELSE 0 END) AS "35-44",
	SUM(CASE WHEN c.customer_age_range = '45-54' THEN 1 ELSE 0 END) AS "45-54",
	SUM(CASE WHEN c.customer_age_range = '55-64' THEN 1 ELSE 0 END) AS "55-64",
	SUM(CASE WHEN c.customer_age_range = '65+' THEN 1 ELSE 0 END) AS "65+"
FROM CUSTOMER as c

INNER JOIN
	ZIP as z
	ON c.customer_zip_code = z.zip_code

GROUP BY z.region



----------------------------------------------------------------------
----------------------------------------------------------------------



-- Type demographics
-- TYPE_BY_GENDER 
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

GROUP BY t.type_desc

----------------------------------------------------------------------

-- TYPE_BY_AGE 
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



----------------------------------------------------------------------
----------------------------------------------------------------------



-- Genre demographics
-- GENRE_BY_GENDER 
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

GROUP BY g.genre_desc

----------------------------------------------------------------------

-- GENRE_BY_AGE 
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



----------------------------------------------------------------------
----------------------------------------------------------------------
