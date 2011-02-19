%define real_name URPM

Summary:	URPM module for perl
Name:		perl-%{real_name}
Version:	4.15
Release:	%mkrel 1
License:	GPLv2+ or Artistic
Group:		Development/Perl
Source0:	%{real_name}-%{version}.tar.xz
URL:		http://svn.mandriva.com/cgi-bin/viewvc.cgi/soft/rpm/perl-URPM/
BuildRequires:	perl-devel
BuildRequires:	rpm-devel >= 1:5.3
BuildRequires:	perl(MDV::Packdrakeng)

# we can now expect librpm API to be backward compatible
Requires:	rpm
Conflicts:	rpm < 1:5.3
Conflicts:	urpmi < 6.44
Requires:	perl(MDV::Packdrakeng)
Provides:	perl(URPM::Build) = %{version}-%{release}
Provides:	perl(URPM::Resolve) = %{version}-%{release}
Provides:	perl(URPM::Signature) = %{version}-%{release}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%define _requires_exceptions perl(URPM::DB)\\|perl(URPM::Package)\\|perl(URPM::Transaction)

%description
The URPM module allows you to manipulate rpm files, rpm header files and
hdlist files and manage them in memory.

%prep
%setup -q -n %{real_name}-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
# (tv) fix segfaulting (#61144); -O1 is OK, -O2 is not, the flag that made the difference is -fno-gcse:
# (proyvind): TODO: still valid with rpm 5.3.6?
# (proyvind): really odd, in addition to disabling -fstack-protector (#61690),
#	      if any optimization level is used, it will cause problems, but if
#	      explicitly enabling all the same optimizations manually, it won't
#	      segfault... Just cowardly working around for now...
%make \
%ifarch %{ix86}
OPTIMIZE="$RPM_OPT_FLAGS -fno-stack-protector -O0 `gcc -O2 -Q --help=optimize|grep enabled|cut -d\  -f3| tr '\n' ' '` -fno-gcse"
%else
OPTIMIZE="$RPM_OPT_FLAGS"
%endif

%check
# skip check suite when building on rpm 4, as some parts of it depends on
# rpm 5.3 to be installed
[ "`rpm --version|sed -e  's/^.* \([0-9]\+\).*/\1/'`" != 4 ] && \
make test

%install
rm -rf %{buildroot}
%makeinstall_std

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README ChangeLog
%{_mandir}/man3/*
%{perl_vendorarch}/URPM.pm
%dir %{perl_vendorarch}/URPM
%{perl_vendorarch}/URPM/*.pm
%dir %{perl_vendorarch}/auto/URPM
%{perl_vendorarch}/auto/URPM/URPM.so
