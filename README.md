# Easy Server IPv4 Migration

Change the IPv4 of your servers without side-effects with IPGEM, the IP Gateway
for Easy Migrations.

## How It Works

The IPGEM gateway impersonates the former IPs of your servers and forwards
transparently all the traffic it receives to the new IPs. All the misconfigured
scripts and applications (most notably those using hard-coded IP addresses)
still work and you can fix them at your leisure.

All the traffic that goes through IPGEM is logged, so that you know what you
need to fix.

The IPGEM gateway is implemented using the iptables NAT targets.

## Did You Test It?

Yes! I successfully used this system at Idgroup to painlessly migrate dozens of
servers in three distinct projects, and I'm making it reusable for a similar
migration at Saint Maclou.

This said, this software comes with no warranty of any kind: see the licence
below. You should only use it if you understand the implications. Contact me
for consulting if you need further service.

In particular, the published version that comes with this README is still being
adapted to EL7 and there may be a few rough edges in the conversion from the
quick solution initially written for Idgroup.

## What's Included in IPGEM

- A method (this README)
- Scripts to manage the IP and iptables configurations of the gateway host
- Scripts to report usage of the gateway

## Intended Audience

This software will be best operated by a GNU/Linux system administrator
familiar with Iptables. Furthermore, tuning the reporting module to your needs
requires some knowledge of SQL and Perl.

## Requirements

### Gateway

- A RHEL/CentOS 7 server (EL 5 may still work but is untested), preferably as a
  VM. I highly recommend to dedicate the host to IPGEM, as it'll take over the
  network configuration files.
- The host must be configured with an English locale (`en_US`, `en_GB`, `C`,
  etc)! This is required for parsing dates from the system logs.
- An IP and NIC for IPGEM administration (distinct from the IPs to migrate).
- A (virtual) network card in each network that contains IPs to migrate.
  VLANs could be used instead of whole NICs, but my administration scripts
  don't support them yet (patches welcome) and it's not really useful in a
  virtual environment anyway.
- I recommend a dedicated 2 GB filesystem for /var/log, with room for
  expansion just in case (use a LVM).
- Enabled RHEL/CentOS (as appropriate) and EPEL repositories.

### Gateway (for small projects)

The requirements above are tailored for large projects where IPGEM will
impersonate a lot of hosts on a lot of networks. If you're just migrating a few
hosts on a single network, you can manage your IPs by hand (rather than with
the IPGEM scripts) and use a single NIC for everything.

### Report Host

- A RHEL/CentOS 7 server (EL 5 may still work but is untested).
- Enough space for 2 copies of the logs in /var/cache
- Enabled RHEL/CentOS (as appropriate) and EPEL repositories.

NB: it can be the same server as the gateway.

## Installation

- Check that you meet the requirements laid out above.
- Enable the EPEL repositories: see
  http://fedoraproject.org/wiki/EPEL#How_can_I_use_these_extra_packages.3F .
- Install the RPM packages `ipgem-gateway` and `ipgem-reports` on your
  server(s).
- Go through `/etc/ipgem-gateway/*` and `/etc/ipgem-reports/*`, adapt the
  configuration as needed using the comments.
- Enable the iptables service on the gateway.
- Either reboot the gateway or:
  - restart rsyslogd
  - reapply the sysctl configuration with `sysctl -p --system`

## The Method

### Plan

1. At the very least, make a list of which batches of servers you will
   migrate, what are their current and target IPs.
2. For each server type (physical, virtual), write down the IP change
   procedure (VM reconfiguration, network switch VLAN assignment commands,
   whatever).
3. You also need to know how to (partially) clear the ARP cache of your
   routers.
4. Figure out when you can afford to interrupt service delivery, and notify
   your users.

### Pre-migration fixes

Fix what you can in advance, by creating DNS records
for each involved server and changing known configurations to use the DNS
rather than hard-coded IP addresses. That's as much traffic that won't go
through the IPGEM gateway.

### Migrate

1. Update `/etc/ipgem-gateway/hosts` with the servers you're migrating (but don't
   apply the configuration yet).
2. Reduce the TTL of the involved DNS records to 60 or 300 seconds (you need
   to do this at least _current TTL_ before the migration!).
3. Add the firewall rules for the new IPs, if applicable.
4. Change the IP of the servers
5. Update the DNS records
6. Clear the old IPs from the ARP cache of your routers
7. Enable IPGEM for these servers
8. Confirm that everything important works as planned
9. Restore the DNS TTL

### Post-migration fixes

1. Run and review IPGEM reports to identify misconfigured applications and
   scripts.
2. Fix the configurations, wait for some days.
3. Repeat.

### Finish

At some point, the traffic still going through the IPGEM will not be worth
your time (caused by supervision tools, antivirus updates, ...) and you'll
just pull the plug on IPGEM rather than trying to fix the last things.

## Administering the Gateway

### Initial Configuration

Go through `/etc/ipgem-gateway/networking` and follow the instructions in the comments.

Make sure that your management interface has `NM_CONTROLLED=no` in its `ifcfg`
file and that it bears the default route.

There is a resolver that performs periodic reverse name resolution for the
client IPs that go through the IPGEM gateway (this is useful for dynamic IPs,
ie. PCs on DHCP). If you need to bypass the DNS for some IPs, edit the Perl
code in `/etc/ipgem-gateway/resolver`.

### Configuration During the Migration

Edit `/etc/ipgem-gateway/hosts` to match which IPs the gateway will impersonate. Then,
run this to apply the configuration:

    ipgem-apply

NB: there will be a slight service interruption.

If you are impersonating an IP for the first time on IPGEM, you'll need to
remove it from the ARP cache of your router for a fast transition. For
instance, on Cisco it's `clear ip arp X.X.X.X`. It would also be possible to
send some gratuitous ARPs instead, but I did not test it.

You may want to stop relaying hosts or specific services at some point. Edit
`/etc/ipgem-gateway/iptables.prefix` and apply it with `ipgem-regen-iptables`.

## Reporting (Analyzing the Logs)

IPGEM comes with a set of scripts to analyze the logs: you don't want IPGEM
to remain a SPOF in your information system for long, so you need information
on what to fix.

Everything under `/etc/ipgem-reports` is configurable, either as plain files or
as symlinks that you can replace by your own files. Do tune as needed, your
changes will be preserved on package updates.

### File System Layout

Path                             | Usage
---------------------------------|------------------------------------------
/etc/ipgem-reports               | All tunables should be here
/etc/ipgem-reports/steps         | Called in order by ipgem-report (E, T, L)
/etc/ipgem-reports/reports       | SQL for each report
/usr/libexec/ipgem-reports       | Internals
/usr/share/ipgem-reports         | Internals
/usr/bin                         | User-facing scripts
/srv/ipgem/reports               | Result files (CSV)
/var/cache/ipgem/logs/TYPE/HOST/ | Local copy of the gateway logs

### Getting Logs to the Report Host

`/etc/ipgem-gateway/get-logs` is a sample script that gathers logs from the
gateway(s) into `/var/cache/ipgem/logs/TYPE/HOST/`, which TYPE one of:
- linux (connections logged by the gateway),
- resolver (semi-real-time IP-to-name resolutions performed by the gateway to
  identify hosts with dynamic IPs),
- srx or srx-gz (I had to use a Juniper SRX firewall as a gateway once, don't
  do that if you can avoid it).

### Producing Reports

`/usr/bin/ipgem-report` runs scripts in `/etc/ipgem-reports/steps`, extracting the
raw logs into a temporary SQLite database, and (after some work) loading the
end results into CSV files in `/srv/ipgem/reports` (reports that you can
open in Excel).

You can customize this heavily to fit your needs:
- Edit log filters in `/etc/ipgem-reports/extract.conf`.
- Classify connections by editing `/etc/ipgem-reports/classify.conf`
- Add reports to run in `/etc/ipgem-reports/steps/80-load-reports` and/or tweak the
  existing ones in `/etc/ipgem-reports/reports/` (the query is in the .sql, while
  .columns is just the first line to include in the resulting CSV).
- Finally, add/edit links and/or files in `/etc/ipgem-reports/steps` (executable
  files are executed, .sql are interpreted with sqlite3 onto the DB).

### Further Reports to Run Manually

- `/usr/bin/ipgem-report-connection` produces a CSV for a given source and
  destination.
- `/usr/bin/ipgem-weekly-stats` produces a high-level report for a given week
  (amount of connections etc).

## Caveats

See https://github.com/tequeter/ipgem/issues/ .

Some protocols do not work through NAT, most notably FTPS.

## Author, Credits, and Licence

Idea and implementation: Thomas Equeter

Sponsors: Idgroup paid me to write IPGEM and we agreed to contribute it back to
the Free Software community. I did further improvements for Saint Maclou,
included in this release.

    IPGEM - Change the IPv4 of your servers without side-effects
    Copyright (C) 2014  Thomas Equeter.

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software Foundation,
    Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
