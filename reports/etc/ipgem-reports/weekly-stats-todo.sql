SELECT tclass, COUNT(*)
FROM (
    SELECT MAX(date), COUNT(*), host, 1, src, srcname, desc, dst, proto, dport, tclass
        FROM resolved_log
        WHERE tclass IN( 'Autre', 'SrvSrv' )
            AND date >= ? AND date < ?
        GROUP BY host, desc, src, srcname, dst, proto, dport, tclass
    UNION ALL
    SELECT MAX(date) AS last_occ, COUNT(*) AS count_occ, host, NULL, '', '', desc, dst, proto, dport, tclass
        FROM resolved_log
        WHERE tclass NOT IN( 'Autre', 'SrvSrv' )
            AND date >= ? AND date < ?
        GROUP BY host, desc, dst, proto, dport, tclass
)
GROUP BY tclass
;


