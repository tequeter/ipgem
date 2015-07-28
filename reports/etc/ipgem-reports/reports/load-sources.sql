SELECT MAX(date), COUNT(*), host, src, srcname
    FROM resolved_log
    GROUP BY host, src, srcname

