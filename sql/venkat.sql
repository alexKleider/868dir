/* File: sql/venkat.sql */
-- similar to query used in code/menu.py

    SELECT P.id, PS.statusID,
        P.first, P.mi, P.last, P.suffix, P.phone, P.address,
        P.town, P.state, P.postal_code, P.country, P.email
    FROM people AS P
    JOIN person_status AS PS
        ON P.id = PS.personID
        AND PS.begin <= "{today}"
        AND (PS.end = "" OR PS.end > "{today}")
        ;
