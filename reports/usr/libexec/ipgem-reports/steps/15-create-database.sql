CREATE TABLE log (date int, host, desc, src, dst, proto, dport, typology);
CREATE TABLE dns (valid int, until int, ip, name);
CREATE VIEW resolved_log AS
    SELECT date, host, desc, src, dns.name AS srcname, dst, proto, dport, typology, log.rowid AS log_id
    FROM log LEFT JOIN dns ON ( log.src = dns.ip AND date >= valid AND date < until )
    GROUP BY log.rowid, date, host, desc, src, dst, proto, dport, dns.name, typology
    HAVING valid IS NULL OR valid = MAX( valid );

