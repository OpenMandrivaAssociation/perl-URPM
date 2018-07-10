%define modname URPM

Summary:	URPM module for perl
Name:		perl-%{modname}
Version:	4.65.1
Release:	6
License:	GPLv2+ or Artistic
Group:		Development/Perl
Source0:	%{modname}-%{version}.tar.xz
URL:		https://abf.io/omv_software/perl-URPM
BuildRequires:	rpm-devel >= 1:5.4.10-3
BuildRequires:	perl(MDV::Packdrakeng)
BuildRequires:	perl-devel
BuildRequires:	perl(List::MoreUtils)
BuildRequires:	perl(JSON::PP)
BuildRequires:	perl(RPMBDB)

# splitted perl is not yet ready so revert some changes
#BuildRequires:	perl(DynaLoader) >= 5.20.3-1.2
#BuildRequires:	perl(ExtUtils::Install)
#BuildRequires:	perl(ExtUtils::MM_Unix)
#BuildRequires:	perl(ExtUtils::Manifest)
#BuildRequires:	perl(ExtUtils::Command)
#BuildRequires:	perl(ExtUtils::Typemaps)
#BuildRequires:	perl(ExtUtils::Mkbootstrap)
#BuildRequires:	perl(ExtUtils::Command::MM)
#BuildRequires:	perl(File::Glob)
#BuildRequires:	perl(Test::Harness)
#BuildRequires:	perl(Test::More)
#BuildRequires:	perl(File::Copy)
#BuildRequires:	perl(File::Path)
#BuildRequires:	perl(TAP::Formatter::File)

# we can now expect librpm API to be backward compatible
Requires:	rpm
Conflicts:	rpm < 1:5.3
Conflicts:	urpmi < 7.24
Requires:	perl(MDV::Packdrakeng)
# splitted perl is not yet ready so revert some changes
#Requires:	perl(DynaLoader) >= 5.20.3-1.2
Provides:	perl(URPM::Build) = %{version}-%{release}
Provides:	perl(URPM::Resolve) = %{version}-%{release}
Provides:	perl(URPM::Signature) = %{version}-%{release}

%description
The URPM module allows you to manipulate rpm files, rpm header files and
hdlist files and manage them in memory.

%prep
%setup -q -n %{modname}-%{version}
%apply_patches

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
%doc README
%{_mandir}/man3/*
%{perl_vendorarch}/URPM.pm
%dir %{perl_vendorarch}/URPM
%{perl_vendorarch}/URPM/*.pm
%dir %{perl_vendorarch}/auto/URPM
%{perl_vendorarch}/auto/URPM/URPM.so
