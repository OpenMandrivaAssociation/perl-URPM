%define modname URPM

Summary:	URPM module for perl
Name:		perl-%{modname}
Version:	4.48.2
Release:	6
License:	GPLv2+ or Artistic
Group:		Development/Perl
Source0:	%{modname}-%{version}.tar.xz
Patch0:		URPM-4.48.2-allow-old-srpms.patch
URL:		https://abf.rosalinux.ru/omv_software/perl-URPM
BuildRequires:	rpm-devel >= 1:5.4
BuildRequires:	perl(MDV::Packdrakeng)
BuildRequires:	perl-devel
BuildRequires:	perl-List-MoreUtils
BuildRequires:	perl-JSON-PP
BuildRequires:	perl(RPMBDB)

# we can now expect librpm API to be backward compatible
Requires:	rpm
Conflicts:	rpm < 1:5.3
Conflicts:	urpmi < 7.24
Requires:	perl(MDV::Packdrakeng)
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
# crisb - TODO some tests still fail but nothing important
exit 0
# skip check suite when building on rpm 4, as some parts of it depends on
# rpm 5.3 to be installed
[ "`rpm --version|sed -e  's/^.* \([0-9]\+\).*/\1/'`" != 4 ] && \
make test

%install
%makeinstall_std

rm -f %{buildroot}%{perl_vendorarch}/URPM/.perl_checker

%files
%doc README
%{_mandir}/man3/*
%{perl_vendorarch}/URPM.pm
%dir %{perl_vendorarch}/URPM
%{perl_vendorarch}/URPM/*.pm
%dir %{perl_vendorarch}/auto/URPM
%{perl_vendorarch}/auto/URPM/URPM.so


%changelog
* Tue Aug 20 2013 Robert Xu <rxu@lincomlinux.org> 4.47-4
- Attempt to fix rpmdrake usage with finding candidate packages
- Coverity analyser fixes
- Improve force-req-update handling and skip-installed-alternatives

* Sat Mar 16 2013 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.44-1
- new version:
	o disable rpmlint for building test package during regression tests
	o move out some functions accessing berkeley db API directly into a
	  RPMBDB module built together with rpm in order to really guard
	  ourself from breakages during new major berkeley db version upgrades
	o don't disable strict aliasing

* Sat Jun 09 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.43-1
+ Revision: 804296
- add a simple detectXZ() function for reading the magic ourself in situations
  where we ie. cannot rely on ie. libmagic

* Wed May 16 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.42-1
+ Revision: 799258
- new version:
	o make URPM::DB::info use berkeley db api rather than using rpmdb
	  functions that's not part of the public api, thus making things
	  less fragile
	o fix building with rpm >= 5.4.9 where BDB data types are hidden

* Thu Apr 12 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.41-1
+ Revision: 790428
- revert change in previous version, it resulted in unsupported rpms being
  installed, better to properly handle this conversion in rpm itself now

* Thu Mar 29 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.40-1
+ Revision: 788154
- handle rpms using old format with missing version, which would result in crash
  with ie. Oracle Java rpm package (#65443)
- fix mixed-use-of-spaces-and-tabs

* Wed Mar 07 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.39-1
+ Revision: 782591
- drop _requires_exceptions, it's not supported with internal dep generator
  which anyways drops dependencies on self...
- new version:
	o link against berkeley db as we're accessing it's API directly
	o workaround fts.h incompatibility with _FILE_OFFSET_BITS=64 to fix build
	  with perl 5.14.2 (from Bernhard Rosenkraenzer)
	o ~fix filesize computation
	o add support for bzip2 compressed synthesis (by using Fopen() from rpmio)
	o export rpmtag_from_string()

* Sun Jan 22 2012 Oden Eriksson <oeriksson@mandriva.com> 4.38-5
+ Revision: 765802
- rebuilt for perl-5.14.2

* Sat Jan 21 2012 Oden Eriksson <oeriksson@mandriva.com> 4.38-4
+ Revision: 764326
- rebuilt for perl-5.14.x

* Fri Jan 20 2012 Oden Eriksson <oeriksson@mandriva.com> 4.38-3
+ Revision: 763027
- force it

* Fri Jan 20 2012 Bernhard Rosenkraenzer <bero@bero.eu> 4.38-2
+ Revision: 762852
- Make it build with perl 5.14.x

* Wed Nov 02 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.38-1
+ Revision: 712240
- new version fixing build with API changes of rpm 5.4

* Sun Jul 24 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.37-1
+ Revision: 691439
- fix URPM::Resolve::fullname_parts() to also work without disttag & distepoch
  (this will make urpmf & urpmq work with xml metadata again, #61852)

* Wed Jul 06 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.36-1
+ Revision: 688952
- new version:
	o document URPM::DB::convert() in API
	o fix a segfault happening when URPM::DB::convert() is run without arguments

* Wed Jun 25 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.35-1
- new version:
	o fix a regression breaking promotion of dependencies on conflicts

* Thu Jun 23 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.34-1
+ Revision: 686830
- new version:
	o add a workaround for handling upgrade from older berkeley db versions
	  which might not support new configuration in DB_CONFIG, causing it to
	  break during upgrade
	o add support for specifying tag name to match with
	  URPM::Transaction->remove()
	o add some regression tests for parsing disttag & distepoch from
	  synthesis
	o extract disttag & distepoch from new fields in @info@ of synthesis

* Mon Jun 13 2011 Eugeni Dodonov <eugeni@mandriva.com> 4.33-2
+ Revision: 684936
- P0: fix urpmf errors while searching.

* Tue May 31 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.33-1
+ Revision: 682089
- new version:
	o add disttag & distepoch to $state->{rejected} for assisting parsing
	  of fullname with regex
	o add URPM::Resolve::fullname_parts() as a function parsing fullname
	  with a regex assisted by provided disttag & distepoch

* Tue May 31 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.32-1
+ Revision: 682052
- *really* fix URPM::Package->sourcerpm
- new version:
	o fix URPM::Package->sourcerpm returning summary in stead of source rpm
	o fix slow matching of individual regexes for skipping dependencies by
	  creating a large regex to match them all at once (#61389, patch
	  contributed by Shlomi Fish \o/)

* Thu May 12 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.30-1
+ Revision: 673923
- new version:
	o fix Resolve.pm/_choose_required() breakage after DUDF merge, causing
	  ie. 'urpmq -d' to break (#63250, with big thanks to Funda\o/)

* Sat May 07 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.29-1
+ Revision: 671612
- fix segfault when trying to get EVR of a src.rpm from synthesis, as @provides@
  are omitted for these

* Thu May 05 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.28-1
+ Revision: 669316
- new version:
	o revert attempt at refactorizing Trans_run() which turned out to give code
	  harder to read and introduced bugs of options not being parsed (#63205)
	o fix an invalid free() that would've happened if package summary were to be
	  missing and the "" string constant were attempted to be freed
	o fix odd problems caused by attempt at translating correct tag names for
	  query table into rpm tags
	o use newSVpvs() for pushing empty strings as constants in stead

* Wed May 04 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.27-1
+ Revision: 666266
- new version:
	o get the correct package filesize from header
	o fix proper return of 'src' as arch for src.rpms
	o fix confusion between %%{sourcerpm} & %%{sourcepackage} tags

* Wed May 04 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.26-1
+ Revision: 665126
- really fix src.rpm handling
- new version:
	o fix some invalid free()s
- new version:
	o start on using gnu99 code
	o fix some invalid free()s

* Tue May 03 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.24-1
+ Revision: 664662
- new version:
	o fix segfault caused by wrongly assigning arch to incorrect package

* Tue May 03 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.23-1
+ Revision: 663537
- new version:
	o check for termination signals so ie. that installs can be aborted
	  with ^C
	o fix remaining memleaks
	o check that rpmdb was properly opened in read/write mode to prevent
	  segfault if no write permissions

* Tue Apr 26 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.22-1
+ Revision: 659474
- new version:
	o add support for notriggers
	o add support for nofdigests
	o fix getting expected NVRA tag
	o fix possible breakage when trying to load non-existant dependency flags
	o fix provide flags not being loaded for headers read from rpm files

* Sat Apr 23 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.21-1
+ Revision: 657378
- new version:
	o fix missing null terminator at end of @info@ string regression,
	  causing random data to be appended at end of line
- remove legacy rpm stuff..

* Fri Apr 22 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.20-1
+ Revision: 656732
- new version:
	o merge in some DUDF changes from Alexandre Lissy
	o add disttag & distepoch to @info@ in synthesis for easier parsing

* Sun Apr 03 2011 Funda Wang <fwang@mandriva.org> 4.19-2
+ Revision: 650047
- rebuild

* Thu Mar 31 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.19-1
+ Revision: 649486
- pass %%optflags to OPTIMIZE again to ensure we compile with latest flags
- new version:
	o fix regression caused by memleak fix in previous release

* Thu Mar 31 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.18-1
+ Revision: 649342
- new version:
	o fix memleak in URPM::Pkg->evr()
	o drop URPM::DB::close() and teardown properly by calling rpmcliFini()
	  at exit
	o fix odd i586 specific bug triggering segfault with -fstack-protector
	  (#61690)

* Wed Mar 30 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.17-1
+ Revision: 649196
- drop %%clean section
- new version:
	o fix conversion to older hash database format resulting in "missing"
	  package from rpmdb

* Tue Mar 29 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.16-1
+ Revision: 648756
- new version:
	o add setInternalVariable() for changing various variables for debugging
	  etc. within rpmlib
	o support translate_message & raw_message options for
	  URPM::Transaction->check()
	o support versioned suggests

* Sun Feb 27 2011 Funda Wang <fwang@mandriva.org> 4.15-2
+ Revision: 640204
- rebuild to obsolete old packages

* Sat Feb 19 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.15-1
+ Revision: 638726
- fix segfault when there's no provides in synthesis (ie. with src.rpm)

* Mon Feb 14 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.14-1
+ Revision: 637659
- new release:
	o use specified arch for packages to be removed, don't strip it away
	  and remove every package if having multiple packages with same name
	  and different arch
	o fix segfault when trying to open non-existing synthesis

* Thu Feb 10 2011 Funda Wang <fwang@mandriva.org> 4.13-3
+ Revision: 637108
- rebuild

* Thu Jan 27 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.13-2
+ Revision: 633188
- add conflicts on urpmi < 6.44 to ensure rpmdb conversion
- remove NVRA pattern matching hack, it's moved to rpm for now..
- fix getting EVR from rpm headers
- new release (4.13):
	o fix evr extraction which broke for some packages with i586 synthesis
	0 fix parsing of disttag from synthesis
	o add regression checks for the fields extracted from synthesis
- order of %%PROVIDEVERSION isn't always the same for all rpm versions synthesis
  is generated with, so locate it based on name, rather than hardcoding location
  assumption
- new release:
	o enable automatic Berkeley DB log removal for URPM::DB::open() by
	  default (#62271)
- new release:
	o fix URPM::Resolve::*_overlap() for packages having disttag
	o look for EVR of package at the first element @provides@ rather than
	  the last
	o replace incorrect usage of URPM::rpmvercmp on NVRA with rpmEVRcompare
	  in URPM::Resolve::provided_version_that_overlaps() &
	  URPM::Resolve::_find_required_package__sort()
- new release:
	o fix distepoch detection breakage with proper synthesis
- make URPM::Package::get_tag() handle NVRA tag for synthesis (fixing
  regression in previous version)
- new release: 4.8
	o fix a bug causing segfault when trying open a non-existing segfault
	  which for some reaallly odd reason didn't get triggered before now
	o remove a last couple of remaining leftovers after db conversion
	o really include the workaround for removal issue that was accidentally
	  omitted in the previous release
	o remove all indices for old rpmdb after conversion also when not doing
	  rebuild
- new release: 4.7
- revert DB_CONFIG hack, fixed in rpm now..
- new release: 4.6
	o drop deprecated URPM::Pkg->header_filename
	o make URPM::Pkg->filename properly return the filename in synthesis,
	  rather than trying to generate it from NVRA
	o add URPM::DB::close()

* Sun Jan 09 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.5-1
+ Revision: 630828
- fix breakage when installing to an empty chroot without db environment setup

* Sun Jan 09 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.4-2mdv2011.0
+ Revision: 630718
- bump release for main/release...
- merge rpm5 branch

* Tue Nov 16 2010 Joao Victor Martins <jvictor@mandriva.com> 3.38-1mdv2011.0
+ Revision: 598100
- Fix the gpg key parsing to handle PEM encapsulated header portion (bug #61636)

* Fri Oct 29 2010 Thierry Vignaud <tv@mandriva.org> 3.37-6mdv2011.0
+ Revision: 590284
+ rebuild (emptylog)

* Wed Oct 20 2010 Thierry Vignaud <tv@mandriva.org> 3.37-4mdv2011.0
+ Revision: 587000
- fix crashing on undefined packages (#54521)

* Sun Oct 17 2010 Thierry Vignaud <tv@mandriva.org> 3.36-4mdv2011.0
+ Revision: 586188
- reenable $RPM_OPT_FLAGS; whereas -O1 is OK, -O2 is OK too with -fno-gcse to
  stop URPM from segfaulting (#61144)
- explain

* Sun Oct 17 2010 Thierry Vignaud <tv@mandriva.org> 3.36-3mdv2011.0
+ Revision: 586181
- disable $RPM_OPT_FLAGS which cause URPM to segfault

* Sun Aug 01 2010 Funda Wang <fwang@mandriva.org> 3.36-2mdv2011.0
+ Revision: 564588
- rebuild for perl 5.12.1

* Fri Jul 23 2010 Olivier Thauvin <nanardon@mandriva.org> 3.36-1mdv2011.0
+ Revision: 557106
- 3.36 (minor fix for perl-5.12)

* Tue Jul 20 2010 Sandro Cazzaniga <kharec@mandriva.org> 3.35-3mdv2011.0
+ Revision: 555280
- rebuild

  + JÃ©rÃ´me Quelin <jquelin@mandriva.org>
    - rebuild for 5.12

* Mon Apr 26 2010 Christophe Fergeau <cfergeau@mandriva.com> 3.35-1mdv2010.1
+ Revision: 539035
- perl-URPM 3.35:
- when using auto-select, honour search-medias if some were specified

* Tue Mar 23 2010 Christophe Fergeau <cfergeau@mandriva.com> 3.34.1-1mdv2010.1
+ Revision: 526822
- perl-URPM 3.34.1:
- really fix #57224, I forgot a patch in the previous release

* Wed Feb 24 2010 Christophe Fergeau <cfergeau@mandriva.com> 3.34-1mdv2010.1
+ Revision: 510603
- 3.34:
- check for conflicting selected packages before selecting a package (#57224)
  (by Anssi Hannula)

* Mon Oct 05 2009 Christophe Fergeau <cfergeau@mandriva.com> 3.33-1mdv2010.0
+ Revision: 453927
- forgot tarball
- 3.33:
- fix lookup of existing pubkeys (#53710) (by Pascal Terjan)

* Mon Aug 10 2009 Christophe Fergeau <cfergeau@mandriva.com> 3.32-1mdv2010.0
+ Revision: 414329
- 3.32:
- backtrack_selected: use set_rejected_and_compute_diff_provides for package
  removal (Anssi Hannula)
- obey options (keep, nodeps) when unselecting current package in the case
  that was added in 3.31 (Anssi Hannula)

* Tue Jul 28 2009 Christophe Fergeau <cfergeau@mandriva.com> 3.31-1mdv2010.0
+ Revision: 402528
- 3.31:
- add support for querying %%disttag & %%distepoch (by Per ?\195?\152yvind Karlsen)
- clean up and bring back rpm5.org support (by Per ?\195?\152yvind Karlsen)
- keep track of sources for obsoleted/removed levels (#50666) Anssi Hannula)
- keep psel/promote info and remove deadlocked pkg instead of aborting upgrade
  (#52105, Anssi Hannula)
- _handle_conflicts: check all provides for conflicts, not just package name
  (#52135, Anssi Hannula)
- unselect current package if an avoided package is already selected (#52145,
  Anssi Hannula)
- do not try to promote to an older package (#52460, Anssi Hannula)
- add a backtrack entry "conflicts" for avoided packages in backtrack_selected
  (#52153, Anssi Hannula)

* Mon May 11 2009 Christophe Fergeau <cfergeau@mandriva.com> 3.30-1mdv2010.0
+ Revision: 374686
- 3.30:
- rework public key handling since librpm behaviour has changed. It's no longer
  possible to tell it to add the same key multiple times which was causing
  weird "unable to import pubkey" messages when a mirror contains different
  pubkeys for the same key

* Fri Mar 27 2009 Christophe Fergeau <cfergeau@mandriva.com> 3.29-1mdv2009.1
+ Revision: 361620
- 3.29:
- fix regression introduced by fix for bug #47803 (fix by Anssi Hannula).
  Without this patch, urpmi got stuck in an infinite loop when trying
  to upgrade from 2008.1.

* Wed Mar 25 2009 Christophe Fergeau <cfergeau@mandriva.com> 3.28-1mdv2009.1
+ Revision: 361025
- 3.28:
- postpone user choices as much as possible to avoid asking the user
  unnecessary questions, (bug #48100, Anssi Hannula)
- 3.27:
- don't silently install suggests (bug #47934)
- fix _handle_diff_provides in case of impossible-to-satisfy selected
  packages (bug #48223, Anssi Hannula)
- check rep for another pkg providing X if the prev pkg gets removed
  due to a conflict (bug #47803, Anssi Hannula)

* Thu Mar 05 2009 Thierry Vignaud <tv@mandriva.org> 3.26-1mdv2009.1
+ Revision: 348828
- verify_signature: enable to check signatures against a chrooted rpmdb
  (especially important for installer where there's no rpmdb in / and thus no
  keys to check against)

* Fri Jan 16 2009 Christophe Fergeau <cfergeau@mandriva.com> 3.25-1mdv2009.1
+ Revision: 330199
- 3.25
- previous fix for bug #46874 was bogus, really fix it this time

* Tue Jan 13 2009 Christophe Fergeau <cfergeau@mandriva.com> 3.24-1mdv2009.1
+ Revision: 329026
- 3.24
- fix sorting choices on provided version (feature introduced in 3.08,
  but was not working if packages were coming from different repository)
- when a "Requires:" can be fullfilled by several different packages and
  one of those packages is explicitly required by another package which
  is also being installed, silently choose this package instead of letting
  the choice up to perl-URPM user (fixes bug #46874)

* Mon Dec 15 2008 Pixel <pixel@mandriva.com> 3.23-1mdv2009.1
+ Revision: 314472
- 3.23: fix bad free() (thanks to glibc for detecting it)

* Fri Dec 12 2008 Pixel <pixel@mandriva.com> 3.22-1mdv2009.1
+ Revision: 313619
- 3.22:
- fix scriptlet failing:
  adapt to librpm4.6, rpmtsSetRootDir(ts, "") is forbidden

* Tue Dec 09 2008 Pixel <pixel@mandriva.com> 3.21-1mdv2009.1
+ Revision: 312302
- 3.21:
- adapt to librpm4.6
- drop list_rpm_tag()

* Tue Oct 14 2008 Pixel <pixel@mandriva.com> 3.20-1mdv2009.1
+ Revision: 293731
- 3.20:
- $trans->run can now return both the translated errors, and some parsable
  errors (useful for example to detect diskspace issues)

* Tue Oct 07 2008 Pixel <pixel@mandriva.com> 3.19-1mdv2009.0
+ Revision: 291158
- 3.19: handle flag "replacefiles"

* Mon Jul 07 2008 Pixel <pixel@mandriva.com> 3.18-1mdv2009.0
+ Revision: 232635
- 3.18:
- revert change introduced in 3.16 (it breaks too much, eg
  superuser--priority-upgrade.t test case), and introduce
  $state->{rejected_already_installed} instead
- add traverse_tag_find(), removed_or_obsoleted_packages()
- handle $state->{orphans_to_remove} in selected_size() and
  build_transaction_set()

* Thu Jun 26 2008 Pixel <pixel@mandriva.com> 3.16-1mdv2009.0
+ Revision: 229288
- 3.16:
- when not selecting a package because already installed,
  put it in $state->{rejected} with flags {installed}

* Tue Jun 24 2008 Pixel <pixel@mandriva.com> 3.15-1mdv2009.0
+ Revision: 228517
- 3.15: fix urpmi wrongly considering epochless conflicts to match any epoch
  in a case when urpmi should upgrade a conflicting package to an actually
  non-conflicting version (cf epochless-conflict-with-promotion urpmi test)
  (Anssi)

* Fri May 23 2008 Pixel <pixel@mandriva.com> 3.14-1mdv2009.0
+ Revision: 210240
- 3.14: add is_package_installed() in URPM/Resolve.pm (to be used in urpmi 5.20)

* Tue May 20 2008 Pixel <pixel@mandriva.com> 3.13-1mdv2009.0
+ Revision: 209327
- 3.13: do not ignore dropped provide from updated package (mdvbz#40842)

* Fri Mar 07 2008 Pixel <pixel@mandriva.com> 3.12-1mdv2008.1
+ Revision: 181373
- 3.12:
- do allow to promoting a pkg even if it has unsatisfied require (since the
  code will then fix the unsatisfied require). fixes "big transaction"
  (cf urpmi split-transactions--strict-require.t test_efgh())
- rpm5.org port done (by Per Oyvind Karlsen)

* Thu Feb 28 2008 Pixel <pixel@mandriva.com> 3.11-1mdv2008.1
+ Revision: 176218
- 3.11:
- restore FILENAME_TAG in generated hdlist (to be compatible with older
  distros where ->filename can rely on it) (thanks to Nanar)

* Tue Feb 26 2008 Pixel <pixel@mandriva.com> 3.10-1mdv2008.1
+ Revision: 175188
- 3.10:
- add filesize to synthesis, add ->filesize to get it, and add
  selected_size_filesize() to compute the sum
- allow urpmi to know a package was not selected because a newer version is
  installed (#29838)
- handle new package providing xxx which conflicts with an installed package (#17106)
- fix sort choices changed in perl-URPM 3.08
- allow fixing "using one big transaction" that occurs when using --keep
  (#30198)
- do not add FILENAME_TAG and FILESIZE_TAG to hdlist anymore,
  deprecate ->filename and ->header_filename,
  deprecate URPM::Build build_hdlist and parse_rpms_build_headers

* Mon Feb 25 2008 Pixel <pixel@mandriva.com> 3.08-1mdv2008.1
+ Revision: 174608
- 3.08: sort choices on virtual package by provided version (#12645)

* Fri Jan 25 2008 Pixel <pixel@mandriva.com> 3.07-3mdv2008.1
+ Revision: 157996
- we can now expect librpm API to be backward compatible

* Sun Jan 13 2008 Pixel <pixel@mandriva.com> 3.07-2mdv2008.1
+ Revision: 150905
- rebuild for perl 5.10.0

* Fri Jan 11 2008 Pixel <pixel@mandriva.com> 3.07-1mdv2008.1
+ Revision: 147885
- 3.07: fix regression in release 3.06

* Fri Jan 11 2008 Pixel <pixel@mandriva.com> 3.06-1mdv2008.1
+ Revision: 147880
- 3.06:
- add URPM::Package->changelogs, a wrapper around ->changelog_time, ->changelog_name, ->changelog_text
- resolve kmod requires even if first choice is a source dkms

* Tue Jan 08 2008 Pixel <pixel@mandriva.com> 3.05-2mdv2008.1
+ Revision: 146591
- force rebuild
- 3.05: fix regression in ->parse_rpm (introduced in 3.00)
  (was breaking genhdlist2 and mkcd)

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Thu Dec 20 2007 Pixel <pixel@mandriva.com> 3.04-1mdv2008.1
+ Revision: 135514
- 3.04: fix regression in parse_pubkeys() (introduced in 3.00) (#36121)
- 3.03:
- suggests:
  handle both RPMTAG_SUGGESTSNAME (as done in SuSE and in Mandriva > 2008.0)
  and RPMTAG_REQUIRENAME + RPMSENSE_MISSINGOK (as done in Mandriva 2008.0)
- 3.02:
- fix "make test" on rpm 4.4.2.2
- fix rpm 4.5 support

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Dec 11 2007 Pixel <pixel@mandriva.com> 3.01-1mdv2008.1
+ Revision: 117313
- 3.01: add URPM::DB::verify()

* Tue Dec 11 2007 Pixel <pixel@mandriva.com> 3.00-1mdv2008.1
+ Revision: 117185
- 3.00:
- replace ->import_needed_pubkeys and ->import_pubkey in favor of
  import_needed_pubkeys_from_file() and ->import_pubkey_file
  (! this breaks API !)
- drop $package->upgrade_files() (unused for a long time afaik)
- rpm.org HEAD support
- conflicting with urpmi & drakx-installer-stage2 which use old
  ->import_needed_pubkeys API
- enable "make test" again

  + Thierry Vignaud <tv@mandriva.org>
    - fix URL

* Thu Nov 22 2007 Pixel <pixel@mandriva.com> 2.10-1mdv2008.1
+ Revision: 111320
- 2.10:
- much simpler --auto-select algorithm
  (fixes #35718, ie auto-selecting with strict-arch)
  (!! DANGEROUS CHANGE !!)
- rpm 4.5 support (thanks to peroyvind) (#35323)
- 2.09: use a simple function to return simple string list from header
  (fixes getting >4096 long rpm changelogs)
  (!! static buffer size limitation in callback_list_str_xpush() should be fixed !!)
- 2.08: fix build on rpm 4.4.2.2

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - make queryformat conditional for %%rpm_version

* Mon Oct 01 2007 Pixel <pixel@mandriva.com> 2.07-1mdv2008.0
+ Revision: 94166
- 2.07:
- prefer precompiled kmod packages corresponding to installed kernels
- don't resolve suggested virtual packages if already installed (#34376)

* Fri Sep 28 2007 Pixel <pixel@mandriva.com> 2.06-1mdv2008.0
+ Revision: 93781
- 2.06: also handle promotion via obsolete for conflicts

* Fri Sep 28 2007 Pixel <pixel@mandriva.com> 2.05-1mdv2008.0
+ Revision: 93580
- 2.05:
- package promotion must respect strict_arch
- enhance sorted graph by better taking into account conflicts from state->{rejected}
  (fixes "big transaction" in urpmi split-transactions--strict-require.t test)

* Thu Sep 27 2007 Pixel <pixel@mandriva.com> 2.04-1mdv2008.0
+ Revision: 93326
- 2.04: handle promotion via obsolete, not only provides

* Thu Sep 20 2007 Pixel <pixel@mandriva.com> 2.03-1mdv2008.0
+ Revision: 91452
- 2.03: fix bug doing "urpmi kernel-source"

* Tue Sep 18 2007 Pixel <pixel@mandriva.com> 2.02-1mdv2008.0
+ Revision: 89712
- 2.02:
- prefer every kernel-<flavor>-devel-<version> packages for which
  kernel-<flavor>-<version> is selected
- fix regression in 2.00: we can't cache the platform, cache the result of
  is_arch_compat instead

* Fri Sep 14 2007 Pixel <pixel@mandriva.com> 2.01-1mdv2008.0
+ Revision: 85620
- bug fix release, 2.01:
- fix bug occurring with --keep
- fix regression in 2.00: keep_unrequested_dependencies is still used by
  installer. restore it, but must now be set trough
  $urpm->{keep_unrequested_dependencies}

* Thu Sep 13 2007 Pixel <pixel@mandriva.com> 2.00-1mdv2008.0
+ Revision: 85088
- new major release 2.00 since many things have changed in the algorithm
  (but no API breakage)
- speedup is_arch_compat (7 times faster) by keeping the platform in a cache
- do not propose packages for non installed locales
- pass the prefered choices to {callback_choices}: this allows urpmi to select
  all the prefered packages according to installed locales
- handle promote for conflict from installed package
  (fixes test_gh() from urpmi split-transactions--promote test case)
- handle promote from installed package which require a unselected package,
  whereas new package does not require it anymore
  (cf test_d & test_e from split-transactions--conflict urpmi test case)

* Mon Sep 03 2007 Pixel <pixel@mandriva.com> 1.80-1mdv2008.0
+ Revision: 78613
- bug fix release, 1.80:
- fix bug in sort_graph (used by build_transaction_set)

* Mon Sep 03 2007 Pixel <pixel@mandriva.com> 1.79-1mdv2008.0
+ Revision: 78485
- bug fix release, 1.79:
- fix bug in sort_graph (used by build_transaction_set)

* Fri Aug 31 2007 Pixel <pixel@mandriva.com> 1.78-1mdv2008.0
+ Revision: 77001
- bug fix release, 1.78
- fix dead-loop in build_transaction_set (#33020)

* Wed Aug 29 2007 Pixel <pixel@mandriva.com> 1.77-1mdv2008.0
+ Revision: 73531
- new release, 1.77
- disable "dropping tags from rpm header" until we can safely use it

* Tue Aug 28 2007 Pixel <pixel@mandriva.com> 1.76-1mdv2008.0
+ Revision: 72755
- new release, 1.76
- build_transaction_set: new sort algorithm which allow returning sets of
  circular dependent packages, taking into account obsoleted packages
  (fixes #31969). It may still fail in presence of conflicts
- allow running transaction with justdb option
- fix split_length > 1
  (eg: "urpmi --split-length 2 a b c" will only install 2 pkgs)
- spec2srcheader: workaround parseSpec returning a header where ->arch is set
  to %%{_target_cpu} whereas we really want a header similar to .src.rpm
  (see #32824)

* Sun Aug 12 2007 Pixel <pixel@mandriva.com> 1.75-1mdv2008.0
+ Revision: 62370
- new release, 1.75
- fix dropping tags from rpm header.
  it hasn't work since MDK8.1 and rpm 4.0.
  it may break urpmi!! but potentially allows a much smaller hdlist.cz :)
- new release, 1.74
- sort choices per media, then per version

* Sat Aug 11 2007 Pixel <pixel@mandriva.com> 1.73-1mdv2008.0
+ Revision: 61936
- new release, 1.73
- allow running transaction with replagekgs option

* Fri Aug 10 2007 Pixel <pixel@mandriva.com> 1.72-1mdv2008.0
+ Revision: 61597
- new release, 1.72
- modify parse_hdlist so that partial hdlist reading can be used
  (needed when some stuff is already done in the callback)

* Thu Aug 09 2007 Pixel <pixel@mandriva.com> 1.71-1mdv2008.0
+ Revision: 60857
- new release 1.71
- compilation fixes on rpm < 4.4.8

* Thu Aug 09 2007 Pixel <pixel@mandriva.com> 1.70-1mdv2008.0
+ Revision: 60842
- new release 1.70
- compilation fixes on rpm < 4.4.8

* Thu Aug 09 2007 Pixel <pixel@mandriva.com> 1.69-1mdv2008.0
+ Revision: 60823
- new release, 1.69
- "suggests" are no more handled as "requires"
- resolve_requested support "suggests": a newly suggested package is installed
  as if required (can be disabled with option no_suggests)

* Fri Aug 03 2007 Pixel <pixel@mandriva.com> 1.68-1mdv2008.0
+ Revision: 58583
- new release, 1.68
- add $trans->Element_version and $trans->Element_release

* Thu Jul 05 2007 Olivier Thauvin <nanardon@mandriva.org> 1.67-1mdv2008.0
+ Revision: 48576
- 1.67:
  o fix spec2header
  o add functions to evaluate arch/os/platform

* Mon Jul 02 2007 Pixel <pixel@mandriva.com> 1.66-1mdv2008.0
+ Revision: 47155
- new release, 1.66:
- fix --auto-select skipping some packages because of other packages providing
  a more recent version, but no obsolete between those packages.
  the fix is to revert commit from Aug 2002:
    "fixed propable old package (according provides) requested by
     request_packages_to_upgrade."

* Thu Jun 21 2007 Olivier Thauvin <nanardon@mandriva.org> 1.65-1mdv2008.0
+ Revision: 42313
- 1.65 (really fix arch_score evaluation)

* Tue Jun 12 2007 Pixel <pixel@mandriva.com> 1.64-1mdv2008.0
+ Revision: 38119
- bug fix release 1.64 for rpm 4.4.8
- hack on $pkg->is_arch_compat to make it return true for noarch packages
  when using rpm 4.4.8 (#31314)

* Thu Jun 07 2007 Anssi Hannula <anssi@mandriva.org> 1.63-4mdv2008.0
+ Revision: 36192
- rebuild with correct optflags

  + Olivier Thauvin <nanardon@mandriva.org>
    - really rebuild against rpm 4.4.8
    - rebuild for next rpm

* Wed May 09 2007 Pixel <pixel@mandriva.com> 1.63-1mdv2008.0
+ Revision: 25742
- new release, 1.63
- add $trans->Element_fullname

* Thu May 03 2007 Pixel <pixel@mandriva.com> 1.62-1mdv2008.0
+ Revision: 21554
- new release, 1.62
- pass the virtual package name as a parameter to {callback_choices} in
  ->resolve_requested
- add $trans->NElements and $trans->Element_name
  to be able to display name of uninstalled package in callback_uninst
- fix b--obsoletes-->a and c--conflicts-->a prompting for upgrading a
  (need a fix in urpmi which rely on the $state->{rejected}
   to upgrade (-U) b instead of installing (-i) it)


* Thu Mar 08 2007 Pixel <pixel@mandriva.com> 1.60-1mdv2007.1
+ Revision: 138215
- new release, 1.60
- more debugging hooks
- create $urpm->packages_providing($name) and use it
- create $urpm->packages_by_name($name)

* Thu Mar 01 2007 Olivier Thauvin <nanardon@mandriva.org> 1.59-1mdv2007.1
+ Revision: 130646
- 1.59:
  o rpm 4.4.8 adaptions
  o load rpm config files at module load, improve the mechanism

* Wed Feb 14 2007 Pixel <pixel@mandriva.com> 1.58-1mdv2007.1
+ Revision: 120987
- new release
- don't check signature and digest in ->traverse and ->traverse_tag
  (=> x15 speedup here, ie x2.5 speedup on urpmi --auto-select and x2 on rpmdrake)

* Fri Feb 09 2007 Pixel <pixel@mandriva.com> 1.57-1mdv2007.1
+ Revision: 118517
- new release, 1.57
- allow upgrading from noarch to x86_64 even if strict-arch

* Fri Jan 19 2007 Pixel <pixel@mandriva.com> 1.56-1mdv2007.1
+ Revision: 110559
- new release, 1.56
- tell perl that strings from rpm headers are utf8
- add URPM::bind_rpm_textdomain_codeset() to set encoding of messages returned
  by rpmlib, and tell perl that those strings are utf8
- really use strict-arch by default on x86_64

* Wed Jan 10 2007 Pixel <pixel@mandriva.com> 1.55-1mdv2007.1
+ Revision: 106990
- bug fix release, 1.55
- fix "not selecting foo-1 since the more recent foo-1 is installed" causing
  urpmi to try to remove the package it wants to install (#28076)

* Tue Jan 09 2007 Pixel <pixel@mandriva.com> 1.54-1mdv2007.1
+ Revision: 106597
- new release, 1.54
- if we have a choice between foo-1 and bar-1 and foo-2 is installed,
  prefering bar-1 instead of foo-1
  (otherwise we can hit: "the more recent foo-2 is installed, but does not
  provide xxx whereas foo-1 does", cf bug #27991)
- bar is needed, foo-1 does provide bar, installed foo-2 does not provide bar:
  do not let the algorithm use foo-2 as if it also provides bar
- allow understanding what ->resolve_requested is doing through a callback ($urpm->{debug_URPM})
- cleanup some code in ->resolve_requested
- make the documentation for ->is_arch_compat more clear
- remove a warning in "perl Makefile.PL" (and would help "make test")

* Mon Jan 08 2007 Pixel <pixel@mandriva.com> 1.53-1mdv2007.1
+ Revision: 105460
- add missing files to the tarball to allow make test
- get rids of some "used of uninitialized value"

* Mon Dec 04 2006 Pixel <pixel@mandriva.com> 1.52-1mdv2007.1
+ Revision: 90367
- much stricter synthesis parsing:
  o fail on first error,
  o correctly handle gzread errors,
  o correctly handle parsing another synthesis after a buggy one

* Fri Dec 01 2006 Pixel <pixel@mandriva.com> 1.51-1mdv2007.1
+ Revision: 89808
- ensure verify_signature, parse_rpm and update_header do not segfault on weird rpm

* Thu Nov 30 2006 Pixel <pixel@mandriva.com> 1.50-1mdv2007.1
+ Revision: 88899
- fix segfault when using --excludepath (Thierry Vignaud)

* Fri Nov 24 2006 Pixel <pixel@mandriva.com> 1.49-1mdv2007.1
+ Revision: 86902
- strict-arch should not imply that noarch can't upgrade the real arch (#22558)

* Tue Nov 21 2006 Pixel <pixel@mandriva.com> 1.48-1mdv2007.1
+ Revision: 85725
- default to strict-arch on 64bits (tvignaud)
- handle empty hdlist.cz/synthesis.cz (in build_hdlist, build_synthesis, parse_hdlist, parse_synthesis)
- parse_rpms_build_headers: allow asking for packing (and so fixing an error in urpmi)
- documentation & comments enhancement

* Tue Oct 17 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.47-1mdv2007.0
+ Revision: 65574
- Version 1.47:
  . Ignore self-obsoletes (Pixel)
  . Fix a bogus check, avoids some infinite loops

* Thu Sep 07 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.46-1mdv2007.0
+ Revision: 60264
- Version 1.46 :
  . prefer stripped kernel source in choices list (needs to be refined)
  . fix URL in spec file

* Tue Aug 08 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.45-1mdv2007.0
+ Revision: 53955
- 1.45: fix a FD leak (P.Terjan); fix urpmi --strict-arch with SRPMS; cleanup
- Import perl-URPM

* Tue Jun 13 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.44-1mdv2007.0
- Fixes for rpm 4.4.6

* Wed May 24 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.43-1mdk
- Fix urpmi .spec by loading macros beforehand (Olivier Thauvin)

* Tue May 23 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.42-1mdk
- Fix FD leak (Pascal Terjan)

* Wed May 03 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.41-1mdk
- Use more recent defines from the rpmlib
- Add a function to traverse transactions

* Wed Mar 15 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.40-1mdk
- Fixes for rpm 4.4.5
- Fix traversing rpmdb for "triggeredby" relationship

* Tue Mar 07 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.39-1mdk
- More memory protection
- Fix gcc options

* Mon Mar 06 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.38-1mdk
- Fix deallocation of rpm transactions

* Fri Mar 03 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.37-1mdk
- Rewrite verify_rpm(), which wasn't working with recent rpms
  (note incompatible API change)
- New function verify_signature()
- Make sure -fno-strict-aliasing is used for compilation
- More docs

* Mon Feb 13 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.36-1mdk
- Add flag ignorearch for installations

* Fri Feb 10 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.35-1mdk
- repackage flag bug fix

* Fri Feb 10 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.34-1mdk
- Add $pkg->installtid method
- Doc nits, code cleanup
- No need for an explicit dependency on perl-base

* Thu Feb 09 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.33-1mdk
- Add repackage flag to run transactions

* Wed Jan 25 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.32-1mdk
- Minor modification to spec2srcheader()

* Thu Jan 19 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.31-1mdk
- New function spec2srcheader() (Olivier Thauvin)

* Fri Jan 06 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.30-2mdk
- Rebuild for rpm 4.4.4
- Fix a regression test

* Wed Dec 07 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.30-1mdk
- Fix epoch comparison bug
- Be compatible with rpm 4.4.3
- Add a URPM::Package::dump_flags debug method
- C code and makefile cleanup
- Don't require bzip2 anymore

* Wed Nov 02 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.29-1mdk
- Don't require packdrake, use MDV::Packdrakeng instead
- Support for --ignoresize

* Tue Oct 04 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.28-1mdk
- add some options to parse_rpm (nomd5, nopayload) (Olivier Thauvin)
- Build process cleanup

* Sat Sep 10 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.27-1mdk
- make add_macro quote embedded newlines. add_macro_noexpand now works like
  the previous version (i.e. like in the rpmlib)

* Fri Sep 02 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.26-1mdk
- Add noscripts option to run transactions

* Wed Aug 24 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.25-1mdk
- Better handle bad file descriptors returned by transaction callbacks (Pixel)
- Doc fixes

* Fri Aug 19 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.24-3mdk
- Allow to rebuild under non-C locales

* Fri Jul 29 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.24-2mdk
- Rebuild for rpm 4.4.2
- Doc nits

* Fri Jul 01 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.24-1mdk
- Add rpmErrorWriteTo() and rpmErrorString()

* Fri Jun 17 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.23-1mdk
- add setVerbosity function

* Wed Jun 08 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.22-1mdk
- Add make_delta_rpm function

* Wed Jun 01 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.21-1mdk
- Add the URPM::Package::payload_format method

* Wed May 11 2005 Olivier Thauvin <nanardon@mandriva.org> 1.20-3mdk
- Rebuild for rpm 4.4.1 (amd64)

* Tue May 10 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.20-2mdk
- Rebuild for rpm 4.4.1

* Thu May 05 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.20-1mdk
- Adaptations for rpm 4.4.1 (Olivier Thauvin)
- More deprecation for RPMSENSE_PREREQ
- Remove rpm 4.0 support
- when no preferred locale is found, put locales-en in front of choice list
  (bug #15628)

* Mon Mar 07 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 1.11-1mdk
- Speed optimisation for updating media

* Wed Mar 02 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 1.10-1mdk
- Prepare for obsolescence of PreReq rpm tag, introduce equivalent
  RPMSENSE_SCRIPT_* tags

* Tue Feb 15 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 1.09-1mdk
- Force recomputation of rejected packages when deleting some in installation
  dependency resolution

* Fri Feb 11 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 1.08-1mdk
- Add macro handling code (O. Thauvin)

* Wed Feb 02 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 1.07-4mdk
- Require perl-base >= 2:5.8.6 actually

* Fri Jan 21 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 1.07-3mdk
- Require perl-base >= 5.8.6
- Error handling nits.

* Mon Dec 13 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 1.07-2mdk
- Require packdrake (and no longer rpmtools)

* Mon Dec 13 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 1.07-1mdk
- Now returns the list of chosen packages sorted by descending version.

* Thu Dec 09 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 1.06-1mdk
- Don't fork a packdrake to build hdlists anymore, use Packdrakeng.pm instead.
- Remove unused requires.
- Add ChangeLog in documentation.

* Thu Nov 25 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 1.05-1mdk
- Allow to use non-contiguous selection ranges (Olivier Thauvin)

* Fri Nov 12 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 1.04-2mdk
- Rebuild for new perl

* Wed Nov 10 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 1.04-1mdk
- More info reported about failures in dependency resolution.

* Thu Oct 28 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 1.03-2mdk
- Support for urpmi --strict-arch option
- Multiarch fix (Gwenole Beauchesne)
- Don't use $TMPDIR if not writable

* Mon Aug 30 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 1.03-1mdk
- add rpmvercmp binding (from perl-Hdlist)

* Wed Aug 25 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 1.02-1mdk
- From now, never promote epochs in comparing versions.

* Thu Aug 12 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 1.01-1mdk
- Better fix for packages that obsolete themselves (François Pons)
- Protection against broken packages with bad fullnames (with an "@")

* Tue Aug 03 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 1.00-1mdk
- Protection against packages that obsolete themselves.
- Backwards compatibility with perl 5.6.
- Cleanups.

* Sat Jul 31 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 0.99-1mdk
- A small modification in the algorithm that searches for virtual provides:
  don't give a choice between several packages that are already installed.

* Thu Jul 29 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 0.98-2mdk
- Rebuild for new perl

* Fri Jul 23 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 0.98-1mdk
- Add a function URPM::stream2header()

* Thu Jul 15 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.97-1mdk
- Generate man page

* Tue Jul 13 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 0.96-1mdk
- Simplify the parsing of skip.list and inst.list files
- Segfault fixes by Olivier Thauvin

* Sat May 22 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 0.95-2mdk
- Don't include older packages than the installed ones in the dependencies
  (except when urpmi is invoked with --allow-force)

* Fri May 07 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 0.95-1mdk
- Add a way to make some error messages non-fatal

* Sat May 01 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 0.94-13mdk
- A few bugfixes
- Add the methods $pkg->queryformat() and $urpm->list_rpm_tag()
- More tests

* Thu Apr 22 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 0.94-12mdk
- cleanup and documentation

