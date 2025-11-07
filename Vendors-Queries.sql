-- General inventory queries

----------------------------------------------------------------------

--Most utilized vendors
SELECT v.vendor_name, SUM(o.item_quantity) AS qty
FROM VENDORS AS v
INNER JOIN ORDERS AS o ON v.vendor_id = o.vendor_id
GROUP BY v.vendor_name
ORDER BY qty DESC

----------------------------------------------------------------------

--Most popular movie from each vendor
SELECT
    v.vendor_name,
    i.title as most_popular_movie,
    COUNT(r.inventory_id) AS qty
FROM RENTAL_INVENTORY AS r
INNER JOIN MOVIES AS m ON r.inventory_id = m.inventory_id
INNER JOIN INVENTORY AS i ON m.inventory_id = i.inventory_id
INNER JOIN ORDERS AS o ON i.inventory_id = o.inventory_id
INNER JOIN VENDORS AS v ON o.vendor_id = v.vendor_id
GROUP BY v.vendor_id, v.vendor_name, i.title
HAVING COUNT(r.inventory_id) = (
    SELECT MAX(movie_rentals)
    FROM (
        SELECT
            v.vendor_id,
            COUNT(r.inventory_id) AS movie_rentals
        FROM RENTAL_INVENTORY AS r
        INNER JOIN MOVIES AS m ON r.inventory_id = m.inventory_id
        INNER JOIN INVENTORY AS i ON m.inventory_id = i.inventory_id
        INNER JOIN ORDERS AS o ON i.inventory_id = o.inventory_id
        INNER JOIN VENDORS AS v ON o.vendor_id = v.vendor_id
        GROUP BY v.vendor_id, i.title
    ) AS subquery
    WHERE subquery.vendor_id = v.vendor_id
)
ORDER BY qty DESC

----------------------------------------------------------------------

--Most popular game from each vendor
SELECT
    v.vendor_name,
    i.title as most_popular_game,
    COUNT(r.inventory_id) AS qty
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
ORDER BY qty DESC

----------------------------------------------------------------------

--Top genres from each vendor
SELECT
    v.vendor_name,
    g.genre_desc AS top_genre,
    COUNT(*) AS qty
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
ORDER BY qty DESC

----------------------------------------------------------------------

--Top types from each vendor
SELECT
    v.vendor_name,
    t.type_desc AS top_type,
    COUNT(*) AS qty
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
ORDER BY qty DESC