SELECT MAX(date), COUNT(*), host, src, srcname, desc, dst, proto, dport, typology
    FROM resolved_log
    GROUP BY host, desc, src, srcname, dst, proto, dport, typology
