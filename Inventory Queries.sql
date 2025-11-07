--- POPULAR_MOVIES = '''
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

ORDER BY Rentals DESC

-- POPULAR_GAMES = '''
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

ORDER BY Rentals DESC


--- POPULAR_STUDIO = '''
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
ORDER BY Rentals DESC

--- POPULAR_CAST
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
ORDER BY Rentals DESC

-- POPULAR_ACTORS
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
ORDER BY Rentals DESC

-- POPULAR_DIRECTORS
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
ORDER BY Rentals DESC

-- POPULAR_WRITERS
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
ORDER BY Rentals DESC

