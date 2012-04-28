%{!?phpname: %{expand: %%global phpname    php}}
%{!?__pecl:  %{expand: %%global __pecl     %{_bindir}/pecl}}

%global pecl_name xdebug
%global prever    RC2
%global devver    rc2

Name:           %{phpname}-pecl-xdebug
Summary:        PECL package for debugging PHP scripts
Version:        2.2.0
Release:        0.7.%{prever}%{?dist}
Source0:        http://xdebug.org/files/%{pecl_name}-%{version}%{?prever}.tgz

# The Xdebug License, version 1.01
# (Based on "The PHP License", version 3.0)
License:        PHP
Group:          Development/Languages
URL:            http://xdebug.org/

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{phpname}-pear  >= 1:1.4.9-1.2
BuildRequires:  %{phpname}-devel >= 5.1.0
BuildRequires:  libedit-devel

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:       %{phpname}(zend-abi) = %{php_zend_api}
Requires:       %{phpname}(api) = %{php_core_api}

Provides:       %{phpname}-pecl(Xdebug) = %{version}
Provides:       %{phpname}-pecl(Xdebug)%{?_isa} = %{version}

# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{_libdir}/.*\\.so$


%description
The Xdebug extension helps you debugging your script by providing a lot of
valuable debug information. The debug information that Xdebug can provide
includes the following:

* stack and function traces in error messages with:
  o full parameter display for user defined functions
  o function name, file name and line indications
  o support for member functions
* memory allocation
* protection for infinite recursions

Xdebug also provides:

* profiling information for PHP scripts
* code coverage analysis
* capabilities to debug your scripts interactively with a debug client


%prep
%setup -qc

cd %{pecl_name}-%{version}%{?prever}

# https://bugs.php.net/60330
sed -i -e '/AC_PREREQ/s/2.60/2.59/' debugclient/configure.in
grep AC_PREREQ debugclient/configure.in

# fix rpmlint warnings
iconv -f iso8859-1 -t utf-8 Changelog > Changelog.conv && mv -f Changelog.conv Changelog
chmod -x *.[ch]

# Check extension version
ver=$(sed -n '/XDEBUG_VERSION/{s/.* "//;s/".*$//;p}' php_xdebug.h)
if test "$ver" != "%{version}%{?devver}"; then
   : Error: Upstream XDEBUG_VERSION version is ${ver}, expecting %{version}%{?devver}.
   exit 1
fi

cd ..
cp -r %{pecl_name}-%{version}%{?prever} %{pecl_name}-zts


%build
cd %{pecl_name}-%{version}%{?prever}
%{_bindir}/phpize
%configure --enable-xdebug  --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

# Build debugclient
pushd debugclient
# buildconf only required when build from git snapshot
[ -f configure ] || ./buildconf
%configure --with-libedit
make %{?_smp_mflags}
popd

cd ../%{pecl_name}-zts
%{_bindir}/zts-phpize
%configure --enable-xdebug  --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}

# install NTS extension
make -C %{pecl_name}-%{version}%{?prever} \
     install INSTALL_ROOT=%{buildroot}

# install debugclient
install -Dpm 755 %{pecl_name}-%{version}%{?prever}/debugclient/debugclient \
        %{buildroot}%{_bindir}/debugclient

# install package registration file
install -Dpm 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# install config file
install -d %{buildroot}%{_sysconfdir}/php.d
cat > %{buildroot}%{_sysconfdir}/php.d/%{pecl_name}.ini << 'EOF'
; Enable xdebug extension module
zend_extension=%{php_extdir}/%{pecl_name}.so

; see http://xdebug.org/docs/all_settings
EOF

# Install ZTS extension
make -C %{pecl_name}-zts \
     install INSTALL_ROOT=%{buildroot}

install -d %{buildroot}%{php_ztsinidir}
cat > %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini << 'EOF'
; Enable xdebug extension module
zend_extension=%{php_ztsextdir}/%{pecl_name}.so

; see http://xdebug.org/docs/all_settings
EOF


%check
# only check if build extension can be loaded
%{_bindir}/php \
    --no-php-ini \
    --define zend_extension=%{pecl_name}-%{version}%{?prever}/modules/%{pecl_name}.so \
    --modules | grep Xdebug

%{_bindir}/zts-php \
    --no-php-ini \
    --define zend_extension=%{pecl_name}-zts/modules/%{pecl_name}.so \
    --modules | grep Xdebug


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc  %{pecl_name}-%{version}%{?prever}/{CREDITS,LICENSE,NEWS,README}
%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{_bindir}/debugclient
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_ztsextdir}/%{pecl_name}.so


%changelog
* Fri Apr 28 2012 Remi Collet <remi@fedoraproject.org> - 2.2.0-0.7.RC2
- Update to 2.2.0RC2

* Wed Mar 14 2012 Remi Collet <remi@fedoraproject.org> - 2.2.0-0.6.RC1
- Update to 2.2.0RC1

* Sun Mar 11 2012 Remi Collet <remi@fedoraproject.org> - 2.2.0-0.5.git8d9993b
- new git snapshot

* Sat Jan 28 2012 Remi Collet <remi@fedoraproject.org> - 2.2.0-0.4.git7e971c4
- new git snapshot
- fix version reported by pecl list

* Fri Jan 20 2012 Remi Collet <remi@fedoraproject.org> - 2.2.0-0.3.git758d962
- new git snapshot

* Sun Dec 11 2011 Remi Collet <remi@fedoraproject.org> - 2.2.0-0.2.gitd076740
- new git snapshot

* Sun Nov 13 2011 Remi Collet <remi@fedoraproject.org> - 2.2.0-0.1.git535df90
- update to 2.2.0-dev, build against php 5.4

* Tue Oct 04 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.1.2-2
- ZTS extension
- spec cleanups

* Thu Jul 28 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.1.2-1
- update to 2.1.2
- fix provides filter for rpm 4.9
- improved description

* Wed Mar 30 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.1.1-1
- allow relocation

* Wed Mar 30 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.1.1-1
- update to 2.1.1
- patch reported version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct 23 2010 Remi Collet <Fedora@FamilleCollet.com> - 2.1.0-2
- add filter_provides to avoid private-shared-object-provides xdebug.so
- add %%check section (minimal load test)
- always use libedit

* Tue Jun 29 2010 Remi Collet <Fedora@FamilleCollet.com> - 2.1.0-1
- update to 2.1.0

* Mon Sep 14 2009 Christopher Stone <chris.stone@gmail.com> 2.0.5-1
- Upstream sync

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 12 2009 Remi Collet <Fedora@FamilleCollet.com> - 2.0.4-1
- update to 2.0.4 (bugfix + Basic PHP 5.3 support)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Oct 09 2008 Christopher Stone <chris.stone@gmail.com> 2.0.3-4
- Add code coverage patch (bz #460348)
- http://bugs.xdebug.org/bug_view_page.php?bug_id=0000344

* Thu Oct 09 2008 Christopher Stone <chris.stone@gmail.com> 2.0.3-3
- Revert last change

* Thu Oct 09 2008 Christopher Stone <chris.stone@gmail.com> 2.0.3-2
- Add php-xml to Requires (bz #464758)

* Thu May 22 2008 Christopher Stone <chris.stone@gmail.com> 2.0.3-1
- Upstream sync
- Clean up libedit usage
- Minor rpmlint fix

* Sun Mar 02 2008 Christopher Stone <chris.stone@gmail.com> 2.0.2-4
- Add %%{__pecl} to post/postun Requires

* Fri Feb 22 2008 Christopher Stone <chris.stone@gmail.com> 2.0.2-3
- %%define %%pecl_name to properly register package
- Install xml package description
- Add debugclient
- Many thanks to Edward Rudd (eddie@omegaware.com) (bz #432681)

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.0.2-2
- Autorebuild for GCC 4.3

* Sun Nov 25 2007 Christopher Stone <chris.stone@gmail.com> 2.0.2-1
- Upstream sync

* Sun Sep 30 2007 Christopher Stone <chris.stone@gmail.com> 2.0.0-2
- Update to latest standards
- Fix encoding on Changelog

* Sat Sep 08 2007 Christopher Stone <chris.stone@gmail.com> 2.0.0-1
- Upstream sync
- Remove %%{?beta} tags

* Sun Mar 11 2007 Christopher Stone <chris.stone@gmail.com> 2.0.0-0.5.RC2
- Create directory to untar sources
- Use new ABI check for FC6
- Remove %%{release} from Provides

* Mon Jan 29 2007 Christopher Stone <chris.stone@gmail.com> 2.0.0-0.4.RC2
- Compile with $RPM_OPT_FLAGS
- Use $RPM_BUILD_ROOT instead of %%{buildroot}
- Fix license tag

* Mon Jan 15 2007 Christopher Stone <chris.stone@gmail.com> 2.0.0-0.3.RC2
- Upstream sync

* Sun Oct 29 2006 Christopher Stone <chris.stone@gmail.com> 2.0.0-0.2.RC1
- Upstream sync

* Wed Sep 06 2006 Christopher Stone <chris.stone@gmail.com> 2.0.0-0.1.beta6
- Remove Provides php-xdebug
- Fix Release
- Remove prior changelog due to Release number change
