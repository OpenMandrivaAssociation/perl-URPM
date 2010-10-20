# $Id: perl-URPM.spec 36978 2006-06-12 10:31:28Z rafael $

%define name perl-URPM
%define real_name URPM
%define version 3.37
%define release %mkrel 4

%define group %(perl -e 'printf "%%s\\n", "%_vendor" =~ /\\bmandr/i ? "Development/Perl" : "Applications/CPAN"')
%define rpm_version %(rpm -q --queryformat '%|EPOCH?{[%{EPOCH}:%{VERSION}]}:{%{VERSION}}|' rpm)

%{expand:%%define compat_makeinstall_std %(perl -e 'printf "%%s\n", "%{?makeinstall_std:1}" ? "%%makeinstall_std" : "%%{__make} install PREFIX=%%{buildroot}%%{_prefix}"')}
%{expand:%%define compat_perl_vendorarch %(perl -MConfig -e 'printf "%%s\n", "%{?perl_vendorarch:1}" ? "%%{perl_vendorarch}" : "$Config{installvendorarch}"')}
%{expand:%%define real_release %%(perl -e 'printf "%%s\\n", ("%_vendor" !~ /\\bmandr/i && ("%release" =~ /(.*?)mdk/)[0] || "%release")')}

Summary:	URPM module for perl
Name:		%{name}
Version:	%{version}
Release:	%{real_release}
License:	GPL or Artistic
Group:		%{group}
Source:		%{real_name}-%{version}.tar.bz2
URL:		http://svn.mandriva.com/cgi-bin/viewvc.cgi/soft/rpm/perl-URPM/
BuildRequires:	perl%{?mdkversion:-devel}
BuildRequires:	rpm-devel >= 4.2.3
BuildRequires:	perl(MDV::Packdrakeng)

# we can now expect librpm API to be backward compatible
Requires:	rpm >= %{rpm_version}
Requires:	perl(MDV::Packdrakeng)
Provides:	perl(URPM::Build) = %{version}-%{release}
Provides:	perl(URPM::Resolve) = %{version}-%{release}
Provides:	perl(URPM::Signature) = %{version}-%{release}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

Conflicts:	urpmi <= 4.10.17
Conflicts:	drakx-installer-stage2 <= 10.5.6

%define _requires_exceptions perl(URPM::DB)\\|perl(URPM::Package)\\|perl(URPM::Transaction)

%description
The URPM module allows you to manipulate rpm files, rpm header files and
hdlist files and manage them in memory.

%prep
%setup -q -n %{real_name}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
# (tv) fix segfaulting (#61144); -O1 is OK, -O2 is not, the flag that made the difference is -fno-gcse:
%{__make} OPTIMIZE="$RPM_OPT_FLAGS -fno-gcse"

%check
%{__make} test

%install
%{__rm} -rf %{buildroot}
%{compat_makeinstall_std}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README ChangeLog
%{_mandir}/man3/*
%{compat_perl_vendorarch}/URPM.pm
%{compat_perl_vendorarch}/URPM
%dir %{compat_perl_vendorarch}/auto/URPM
%{compat_perl_vendorarch}/auto/URPM/URPM.so



