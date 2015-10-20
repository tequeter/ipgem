Name:           ipgem
Version:        0.2.1
Release:        1%{?dist}
Summary:        Easy Server IPv4 Migration
BuildArch:      noarch
License:        GPLv3+
#URL:            
Source0:        %{name}-%{version}.tar.gz

%description
Change the IPv4 of your servers without side-effects with IPGEM, the IP Gateway
for Easy Migrations.

%prep
%setup -q


%build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
# gateway
cp -a gateway/* $RPM_BUILD_ROOT/
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/ipgem-gateway
cp README.md $RPM_BUILD_ROOT/usr/share/doc/ipgem-gateway/
# reporting
cp -a reports/* $RPM_BUILD_ROOT/
mkdir -p $RPM_BUILD_ROOT/etc/ipgem-reports/{steps,reports,extract}
( cd reports/usr/libexec/ipgem-reports/extract/ && for f in *; do ln -s "/usr/libexec/ipgem-reports/extract/$f" $RPM_BUILD_ROOT/etc/ipgem-reports/extract/; done )
( cd reports/usr/libexec/ipgem-reports/steps/ && for f in *; do ln -s "/usr/libexec/ipgem-reports/steps/$f" $RPM_BUILD_ROOT/etc/ipgem-reports/steps/; done )
( cd reports/usr/share/ipgem-reports/reports/ && for f in *; do ln -s "/usr/share/ipgem-reports/reports/$f" $RPM_BUILD_ROOT/etc/ipgem-reports/reports/; done )
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/ipgem-reports
mkdir -p $RPM_BUILD_ROOT/srv/ipgem/reports
cp README.md $RPM_BUILD_ROOT/usr/share/doc/ipgem-reports/


%package gateway
Summary:        Easy Server IPv4 Migration - Gateway component
%{?el7:Requires: iptables-services}

%description gateway
Install this package to impersonate the servers on their old IPs and relay the
connections to the new IPs.

%files gateway
%doc                            /usr/share/doc/ipgem-gateway/README.md
%config(noreplace)              /etc/ipgem-gateway/iptables.suffix
%config(noreplace)              /etc/ipgem-gateway/networking
%config(noreplace)              /etc/ipgem-gateway/resolver
%config(noreplace)              /etc/ipgem-gateway/iptables.prefix
%config(noreplace)              /etc/ipgem-gateway/hosts
%config(noreplace)              /etc/logrotate.d/ipgem-gateway
%config(noreplace)              /etc/rsyslog.d/ipgem.conf
%config(noreplace)              /etc/sysctl.d/ipgem-gateway.conf
%config(noreplace)              /etc/cron.d/ipgem-gateway
                                /usr/sbin/ipgem-regen-iptables
                                /usr/sbin/ipgem-ifdown
                                /usr/sbin/ipgem-regen-ifcfg
                                /usr/sbin/ipgem-ifup
                                /usr/sbin/ipgem-apply
                                /usr/bin/ipgem-resolver
                                /usr/lib/modules-load.d/ipgem-gateway.conf


%package reports
Summary:        Easy Server IPv4 Migration - Reporting component
Requires:       rsync, sqlite, perl-DBD-SQLite

%description reports
Install this package to produce CSV activity reports from a Gateway and find
out which clients are still misconfigured.

%files reports
%doc                            /usr/share/doc/ipgem-reports/README.md
%config(noreplace)              /etc/cron.d/ipgem-reports
%config(noreplace)              /etc/ipgem-reports/steps/10-delete-database
%config(noreplace)              /etc/ipgem-reports/steps/15-create-database.sql
%config(noreplace)              /etc/ipgem-reports/steps/20-extract
%config(noreplace)              /etc/ipgem-reports/steps/25-retroactive-resolve
%config(noreplace)              /etc/ipgem-reports/steps/40-index-data.sql
%config(noreplace)              /etc/ipgem-reports/steps/55-classify-connections
%config(noreplace)              /etc/ipgem-reports/steps/80-load-reports
%config(noreplace)              /etc/ipgem-reports/load.conf
%config(noreplace)              /etc/ipgem-reports/weekly-stats-todo.sql
%config(noreplace)              /etc/ipgem-reports/classify.conf
%config(noreplace)              /etc/ipgem-reports/weekly-stats-uconn.sql
%config(noreplace)              /etc/ipgem-reports/reports/load-destinations.columns
%config(noreplace)              /etc/ipgem-reports/reports/load-sources.sql
%config(noreplace)              /etc/ipgem-reports/reports/load-todo.sql
%config(noreplace)              /etc/ipgem-reports/reports/load-connections.columns
%config(noreplace)              /etc/ipgem-reports/reports/load-todo.columns
%config(noreplace)              /etc/ipgem-reports/reports/load-connections.sql
%config(noreplace)              /etc/ipgem-reports/reports/load-sources.columns
%config(noreplace)              /etc/ipgem-reports/reports/load-destinations.sql
%config(noreplace)              /etc/ipgem-reports/get-logs
%config(noreplace)              /etc/ipgem-reports/retroactive-resolve.conf
%config(noreplace)              /etc/ipgem-reports/extract.conf
%config(noreplace)              /etc/ipgem-reports/extract/linux
%config(noreplace)              /etc/ipgem-reports/extract/resolver
%config(noreplace)              /etc/ipgem-reports/extract/srx
%config(noreplace)              /etc/ipgem-reports/extract/srx-gz
                                /usr/libexec/ipgem-reports/extract/linux
                                /usr/libexec/ipgem-reports/extract/resolver
                                /usr/libexec/ipgem-reports/extract/srx
                                /usr/libexec/ipgem-reports/extract/srx-gz
                                /usr/libexec/ipgem-reports/load-report
                                /usr/libexec/ipgem-reports/steps/10-delete-database
                                /usr/libexec/ipgem-reports/steps/15-create-database.sql
                                /usr/libexec/ipgem-reports/steps/20-extract
                                /usr/libexec/ipgem-reports/steps/25-retroactive-resolve
                                /usr/libexec/ipgem-reports/steps/40-index-data.sql
                                /usr/libexec/ipgem-reports/steps/55-classify-connections
                                /usr/share/ipgem-reports/reports/load-destinations.columns
                                /usr/share/ipgem-reports/reports/load-sources.sql
                                /usr/share/ipgem-reports/reports/load-todo.sql
                                /usr/share/ipgem-reports/reports/load-connections.columns
                                /usr/share/ipgem-reports/reports/load-todo.columns
                                /usr/share/ipgem-reports/reports/load-connections.sql
                                /usr/share/ipgem-reports/reports/load-sources.columns
                                /usr/share/ipgem-reports/reports/load-destinations.sql
                                /usr/bin/ipgem-weekly-stats
                                /usr/bin/ipgem-report-connection
                                /usr/bin/ipgem-report
                                /srv/ipgem/reports



%changelog
* Mon Oct 05 2015 Thomas Equeter <tequeter@users.noreply.github.com> 0.2.1-1
- Added retroactive-resolve dns source
- Declared some conffiles as noreplace
* Mon Oct 05 2015 Thomas Equeter <tequeter@users.noreply.github.com> 0.2.0-1
- Version bump, too many changes to list. See Git log.
* Mon Jul 27 2015 Thomas Equeter <tequeter@users.noreply.github.com> 0.1.0-1
- Initial packaging
