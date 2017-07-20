# 1.0.1-1, 2017-07-20

- Bugfixes for new hosts with no prior IPGEM installation.

# 1.0.0, 2016-02-12

- Force all the relayed trafic to go through the management interface.
- Some incompatible configuration changes to support that (in networking and
  `iptables.*`).
- Improve the reporting performance through database optimizations.
- Rename the "typology" column in `resolved_log` to "tclass" (traffic class).
  This is backward incompatible if you had custom reports.
- Show a timestamp when executing reporting steps, for profiling.
- Reorder the indexing steps (backward incompatible if you had customized the
  database indexing).
- Ensure that old resolver logs are purged from the cache. This saves
  processing time and disk space.
- Added this separate changelog.

# 0.2.4, 2015-11-18

- Reporting improvements.
- Support relaying on the management interface.
- Fixed dry-run for interfaces currently without subinterfaces.
- Fixed removing hosts (bug introduced in v0.2.2).
- Disabled the slow duplicate IPs check.

# 0.2.3, 2015-11-02

- Fixed "database is locked" failure when ipgem-report processes huge logfiles.
- Made cron jobs only send mail when they require attention.
- Fixed the resolver not processing all gateway logs, leaving unresolved
  entries in the reports.

# 0.2.2, 2015-10-20

- Made ipgem-regen-ifcfg more or less transactional.
- Added ipgem-regen-ifcfg --dry-run.
- Made sure that packets towards the real (new) IP are always routed through
  the correct interface.
- Added a "ipgem-apply" script for convenience.

# 0.2.1, 2015-10-05

- Added retroactive-resolve dns source.
- Declared some conffiles as noreplace.

# 0.2.0, 2015-10-05

- Version bump, too many changes to list. See Git log.

# 0.1.0, 2015-07-27

- Initial public release.
