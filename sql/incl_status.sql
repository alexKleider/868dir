/*  File: sql/incl_status.sql */

SELECT P.id, PS.statusID,
    P.first, P.mi, P.last, P.suffix, P.phone, P.address, P.town,
    P.town, P.state, P.postal_code, P.country, P.email
FROM people AS P
JOIN person_status AS PS
WHERE P.id = PS.personID
;
