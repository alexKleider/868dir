/* Sql/active.sql */

/* "{today}" needs to be formatted */

SELECT * FROM people as P
JOIN person_status as PS
ON P.id = PS.personID
WHERE PS.statusID IN [1, 3]
AND PS.begin < "2025-01-17"
AND (PS.end = "" OR PS.end > "2025-01-17")
;
