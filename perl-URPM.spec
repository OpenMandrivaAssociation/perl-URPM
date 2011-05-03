%define real_name URPM

Summary:	URPM module for perl
Name:		perl-%{real_name}
Version:	4.25
Release:	1
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

%define _requires_exceptions perl(URPM::DB)\\|perl(URPM::Package)\\|perl(URPM::Transaction)

%description
The URPM module allows you to manipulate rpm files, rpm header files and
hdlist files and manage them in memory.

%prep
%setup -q -n %{real_name}-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
%make

%check
# skip check suite when building on rpm 4, as some parts of it depends on
# rpm 5.3 to be installed
[ "`rpm --version|sed -e  's/^.* \([0-9]\+\).*/\1/'`" != 4 ] && \
make test

%install
%makeinstall_std

%files
%doc README ChangeLog
%{_mandir}/man3/*
%{perl_vendorarch}/URPM.pm
%dir %{perl_vendorarch}/URPM
%{perl_vendorarch}/URPM/*.pm
%dir %{perl_vendorarch}/auto/URPM
%{perl_vendorarch}/auto/URPM/URPM.so
