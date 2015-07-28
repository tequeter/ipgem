SELECT typology, COUNT(*)
FROM (
    SELECT MAX(date), COUNT(*), host, 1, src, srcname, desc, dst, proto, dport, typology
        FROM resolved_log
        WHERE typology IN( 'Autre', 'SrvSrv' )
            AND date >= ? AND date < ?
        GROUP BY host, desc, src, srcname, dst, proto, dport, typology
    UNION ALL
    SELECT MAX(date) AS last_occ, COUNT(*) AS count_occ, host, NULL, '', '', desc, dst, proto, dport, typology
        FROM resolved_log
        WHERE typology IN( 'Parc', 'Mag', 'Entrepot' )
            AND date >= ? AND date < ?
        GROUP BY host, desc, dst, proto, dport, typology
)
GROUP BY typology
;


