CREATE INDEX log_date ON log (date);
CREATE INDEX log_entry ON log (host, desc, src, dst, proto, dport, typology);
CREATE INDEX log_dest ON log (host, dst, proto, dport);
CREATE INDEX log_typo ON log (typology);
CREATE INDEX dns_ip ON dns (ip, valid);

