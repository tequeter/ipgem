SELECT COUNT(*) FROM (
    SELECT date FROM log WHERE date >= ? AND date < ?
    GROUP BY host, desc, src, dst, proto, dport
)

