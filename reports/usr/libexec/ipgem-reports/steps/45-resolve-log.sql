CREATE TABLE resolved_log AS
    SELECT date, host, desc, src, dns.name AS srcname, dst, proto, dport, null AS tclass, log.rowid AS log_id
    FROM log LEFT JOIN dns ON ( log.src = dns.ip AND "date" >= valid AND "date" < until )
    WHERE "date" <= ( SELECT MAX( until ) FROM dns )
    GROUP BY log.rowid, "date", host, desc, src, dst, proto, dport, dns.name, tclass
    HAVING valid IS NULL OR valid = MAX( valid );
