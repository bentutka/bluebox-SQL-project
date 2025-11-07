-- Fix rental inventory
SELECT ri.kiosk_id
FROM RENTAL_INVENTORY as ri
WHERE ri.kiosk_id NOT IN (
	SELECT k.kiosk_id 
	FROM KIOSK as k)

DELETE FROM RENTAL_INVENTORY
WHERE kiosk_id NOT IN (
	SELECT k.kiosk_id 
	FROM KIOSK as k)

ALTER TABLE RENTAL_INVENTORY
ADD CONSTRAINT kiosk_id FOREIGN KEY (kiosk_id) REFERENCES KIOSK(kiosk_id)


