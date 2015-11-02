SELECT MAX(date), COUNT(*), host, 1, src, srcname, desc, dst, proto, dport, typology
    FROM resolved_log
    WHERE typology IN( 'Autre', 'SrvSrv' )
    GROUP BY host, desc, src, srcname, dst, proto, dport, typology
UNION ALL
SELECT MAX(last_occ), SUM(count_occ), host, COUNT(*), '', '', l.desc, dst, proto, dport, l.typology
    FROM (
        SELECT MAX(date) AS last_occ, COUNT(*) AS count_occ, host, src, desc, dst, proto, dport, typology
            FROM resolved_log
            WHERE typology NOT IN( 'Autre', 'SrvSrv' )
            GROUP BY host, desc, src, dst, proto, dport, typology
        ) AS l
    GROUP BY host, l.desc, dst, proto, dport, l.typology
;

