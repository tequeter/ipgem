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
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/ipgem-gw
cp README.md $RPM_BUILD_ROOT/usr/share/doc/ipgem-gw/
# reporting
cp -a reports/* $RPM_BUILD_ROOT/
( cd reports/usr/lib/ipgem-rp/steps/ && for f in *; do ln -sf "/usr/lib/ipgem-rp/steps/$f" $RPM_BUILD_ROOT/etc/ipgem-rp/steps/; done )
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/ipgem-rp
mkdir -p $RPM_BUILD_ROOT/var/lib/ipgem/reports
cp README.md $RPM_BUILD_ROOT/usr/share/doc/ipgem-rp/


%package gw
Summary:        Easy Server IPv4 Migration - Gateway component
Requires:       rsync

%description gw
Install this package to impersonate the servers on their old IPs and relay the
connections to the new IPs.

%files gw
%doc                            /usr/share/doc/ipgem-gw/README.md
%config(noreplace)              /etc/ipgem-gw/iptables.suffix
%config(noreplace)              /etc/ipgem-gw/networking
%config(noreplace)              /etc/ipgem-gw/resolver
%config(noreplace)              /etc/ipgem-gw/iptables.prefix
%config(noreplace)              /etc/ipgem-gw/hosts
                                /etc/cron.d/ipgem-gw
                                /usr/sbin/ipgem-regen-iptables
                                /usr/sbin/ipgem-ifdown
                                /usr/sbin/ipgem-regen-ifcfg
                                /usr/sbin/ipgem-ifup
                                /usr/bin/ipgem-resolver


%package rp
Summary:        Easy Server IPv4 Migration - Reporting component

%description rp
Install this package to produce CSV activity reports from a Gateway and find
out which clients are still misconfigured.

%files rp
%doc                            /usr/share/doc/ipgem-rp/README.md
                                /etc/cron.d/ipgem-rp
                                /etc/ipgem-rp/steps/10-delete-database
                                /etc/ipgem-rp/steps/15-create-database.sql
                                /etc/ipgem-rp/steps/20-extract
                                /etc/ipgem-rp/steps/40-index-data.sql
                                /etc/ipgem-rp/steps/55-classify-connections
%config(noreplace)              /etc/ipgem-rp/steps/80-load-reports
%config(noreplace)              /etc/ipgem-rp/load.conf
%config(noreplace)              /etc/ipgem-rp/weekly-stats-todo.sql
%config(noreplace)              /etc/ipgem-rp/classify.conf
%config(noreplace)              /etc/ipgem-rp/weekly-stats-uconn.sql
%config(noreplace)              /etc/ipgem-rp/reports/load-destinations.columns
%config(noreplace)              /etc/ipgem-rp/reports/load-sources.sql
%config(noreplace)              /etc/ipgem-rp/reports/load-todo.sql
%config(noreplace)              /etc/ipgem-rp/reports/load-connections.columns
%config(noreplace)              /etc/ipgem-rp/reports/load-todo.columns
%config(noreplace)              /etc/ipgem-rp/reports/load-connections.sql
%config(noreplace)              /etc/ipgem-rp/reports/load-sources.columns
%config(noreplace)              /etc/ipgem-rp/reports/load-destinations.sql
%config(noreplace)              /etc/ipgem-rp/get-logs
%config(noreplace)              /etc/ipgem-rp/extract.conf
                                /usr/lib/ipgem-rp/extract-linux
                                /usr/lib/ipgem-rp/extract-resolver
                                /usr/lib/ipgem-rp/steps/10-delete-database
                                /usr/lib/ipgem-rp/steps/15-create-database.sql
                                /usr/lib/ipgem-rp/steps/20-extract
                                /usr/lib/ipgem-rp/steps/40-index-data.sql
                                /usr/lib/ipgem-rp/steps/55-classify-connections
                                /usr/lib/ipgem-rp/extract-srx
                                /usr/lib/ipgem-rp/load-report
                                /usr/lib/ipgem-rp/extract-srx-gz
                                /usr/lib/ipgem-rp/reports/load-destinations.columns
                                /usr/lib/ipgem-rp/reports/load-sources.sql
                                /usr/lib/ipgem-rp/reports/load-todo.sql
                                /usr/lib/ipgem-rp/reports/load-connections.columns
                                /usr/lib/ipgem-rp/reports/load-todo.columns
                                /usr/lib/ipgem-rp/reports/load-connections.sql
                                /usr/lib/ipgem-rp/reports/load-sources.columns
                                /usr/lib/ipgem-rp/reports/load-destinations.sql
                                /usr/bin/ipgem-weekly-stats
                                /usr/bin/ipgem-rp-load-connection
                                /usr/bin/ipgem-report
                                /var/lib/ipgem/reports



%changelog
* Mon Jul 27 2015 Thomas Equeter <thomas@equeter.com> 0.1.0-1
- Initial packaging
