SELECT MAX(date), COUNT(*), host, desc, dst
    FROM log
    GROUP BY host, desc, dst
