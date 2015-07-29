Name:           ipgem
Version:        0.1.0
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
mkdir -p $RPM_BUILD_ROOT/etc/ipgem-reports/steps $RPM_BUILD_ROOT/etc/ipgem-reports/reports
( cd reports/usr/lib/ipgem-reports/steps/ && for f in *; do ln -s "/usr/lib/ipgem-reports/steps/$f" $RPM_BUILD_ROOT/etc/ipgem-reports/steps/; done )
( cd reports/usr/lib/ipgem-reports/reports/ && for f in *; do ln -s "/usr/lib/ipgem-reports/reports/$f" $RPM_BUILD_ROOT/etc/ipgem-reports/reports/; done )
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/ipgem-reports
mkdir -p $RPM_BUILD_ROOT/var/lib/ipgem/reports
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
                                /etc/cron.d/ipgem-gateway
                                /usr/sbin/ipgem-regen-iptables
                                /usr/sbin/ipgem-ifdown
                                /usr/sbin/ipgem-regen-ifcfg
                                /usr/sbin/ipgem-ifup
                                /usr/bin/ipgem-resolver


%package reports
Summary:        Easy Server IPv4 Migration - Reporting component
Requires:       rsync, sqlite

%description reports
Install this package to produce CSV activity reports from a Gateway and find
out which clients are still misconfigured.

%files reports
%doc                            /usr/share/doc/ipgem-reports/README.md
                                /etc/cron.d/ipgem-reports
                                /etc/ipgem-reports/steps/10-delete-database
                                /etc/ipgem-reports/steps/15-create-database.sql
                                /etc/ipgem-reports/steps/20-extract
                                /etc/ipgem-reports/steps/40-index-data.sql
                                /etc/ipgem-reports/steps/55-classify-connections
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
%config(noreplace)              /etc/ipgem-reports/extract.conf
                                /usr/lib/ipgem-reports/extract-linux
                                /usr/lib/ipgem-reports/extract-resolver
                                /usr/lib/ipgem-reports/steps/10-delete-database
                                /usr/lib/ipgem-reports/steps/15-create-database.sql
                                /usr/lib/ipgem-reports/steps/20-extract
                                /usr/lib/ipgem-reports/steps/40-index-data.sql
                                /usr/lib/ipgem-reports/steps/55-classify-connections
                                /usr/lib/ipgem-reports/extract-srx
                                /usr/lib/ipgem-reports/load-report
                                /usr/lib/ipgem-reports/extract-srx-gz
                                /usr/lib/ipgem-reports/reports/load-destinations.columns
                                /usr/lib/ipgem-reports/reports/load-sources.sql
                                /usr/lib/ipgem-reports/reports/load-todo.sql
                                /usr/lib/ipgem-reports/reports/load-connections.columns
                                /usr/lib/ipgem-reports/reports/load-todo.columns
                                /usr/lib/ipgem-reports/reports/load-connections.sql
                                /usr/lib/ipgem-reports/reports/load-sources.columns
                                /usr/lib/ipgem-reports/reports/load-destinations.sql
                                /usr/bin/ipgem-weekly-stats
                                /usr/bin/ipgem-report-connection
                                /usr/bin/ipgem-report
                                /var/lib/ipgem/reports



%changelog
* Mon Jul 27 2015 Thomas Equeter <thomas@equeter.com> 0.1.0-1
- Initial packaging
