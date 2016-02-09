CREATE INDEX dns_ip ON dns (ip, valid);
ANALYZE;
CREATE TABLE resolved_log AS
    SELECT date, host, desc, src, dns.name AS srcname, dst, proto, dport, null AS typology, log.rowid AS log_id
    FROM log LEFT JOIN dns ON ( log.src = dns.ip AND "date" >= valid AND "date" < until )
    GROUP BY log.rowid, "date", host, desc, src, dst, proto, dport, dns.name, typology
    HAVING valid IS NULL OR valid = MAX( valid );
CREATE INDEX resolved_log_typology ON resolved_log (typology);
CREATE INDEX resolved_log_entry ON resolved_log (host, desc, src, srcname, dst, proto, dport, typology);
ANALYZE;
