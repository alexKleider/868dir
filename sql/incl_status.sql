/*  File: sql/incl_status.sql */

SELECT P.id, P.first, P.last, PS.statusID FROM people AS P
JOIN person_status AS PS
WHERE P.id = PS.personID
AND PS.statusID = 1
;
