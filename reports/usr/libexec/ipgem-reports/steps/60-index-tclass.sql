CREATE INDEX resolved_log_tclass ON resolved_log (tclass);
CREATE INDEX resolved_log_entry ON resolved_log (host, desc, src, srcname, dst, proto, dport, tclass);
ANALYZE;
