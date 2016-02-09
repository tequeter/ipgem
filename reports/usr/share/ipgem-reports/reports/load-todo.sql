SELECT MAX(date), COUNT(*), host, 1, src, srcname, desc, dst, proto, dport, tclass
    FROM resolved_log
    WHERE tclass IN( 'Autre', 'SrvSrv' )
    GROUP BY host, desc, src, srcname, dst, proto, dport, tclass
UNION ALL
SELECT MAX(last_occ), SUM(count_occ), host, COUNT(*), '', '', l.desc, dst, proto, dport, l.tclass
    FROM (
        SELECT MAX(date) AS last_occ, COUNT(*) AS count_occ, host, src, desc, dst, proto, dport, tclass
            FROM resolved_log
            WHERE tclass NOT IN( 'Autre', 'SrvSrv' )
            GROUP BY host, desc, src, dst, proto, dport, tclass
        ) AS l
    GROUP BY host, l.desc, dst, proto, dport, l.tclass
;

