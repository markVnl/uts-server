
Name:           uts-server
Summary:        Micro RFC 3161 Time-Stamp server
License:        MIT
Group:          Productivity/Networking/Web/Servers
Version:        0.2.0
Release:        0.2
URL:            https://github.com/kakwa/uts-server
Source0:        https://github.com/kakwa/uts-server/archive/%{version}.tar.gz

Requires:       libcivetweb1_13_0

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  openssl-devel
BuildRequires:  civetweb-devel


%description
uts-server is a Micro RFC 3161 Time-Stamp server written in C. 

%prep
%setup -q


%build
%cmake .
%{make_build} 

%install
%{make_install}
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
install -m 640 conf/uts-server.cnf  %{buildroot}%{_sysconfdir}/%{name}/%{name}.cfg
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 664 goodies/rhel/uts-server %{buildroot}%{_sysconfdir}/sysconfig/%{name}
mkdir -p %{buildroot}/%{_unitdir}
install -m 644 goodies/rhel/uts-server.service %{buildroot}%{_unitdir}/%{name}.service

%pre
%{_sbindir}/groupadd -r uts-server 2>/dev/null || :
%{_sbindir}/useradd -g uts-server -c "Uts-Server User" -s /bin/false uts-server 2>/dev/null || :

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service


%files
%license LICENSE
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.cfg
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_unitdir}/%{name}.service

%changelog
* Mon Jan 25 2021 Mark Verlinde <mark.verlinde@gmail.com>
- Rebuild for el7

