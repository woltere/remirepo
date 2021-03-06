%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}

%global pear_channel pear.symfony.com
%global pear_name    %(echo %{name} | sed -e 's/^php-symfony2-//' -e 's/-/_/g')
%global php_min_ver  5.3.3

Name:             php-symfony2-Security
Version:          2.1.3
Release:          1%{?dist}
Summary:          Symfony2 %{pear_name} Component

Group:            Development/Libraries
License:          MIT
URL:              http://symfony.com/components
Source0:          http://%{pear_channel}/get/%{pear_name}-%{version}.tgz
Patch0:           %{name}-tests-bootstrap.patch

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:        noarch
BuildRequires:    php-pear(PEAR)
BuildRequires:    php-channel(%{pear_channel})
# Test requires
BuildRequires:    php(language) >= %{php_min_ver}
BuildRequires:    php-pear(pear.phpunit.de/PHPUnit)
BuildRequires:    php-pear(%{pear_channel}/EventDispatcher) >= 2.1.0
BuildRequires:    php-pear(%{pear_channel}/HttpFoundation) >= 2.1.0
BuildRequires:    php-pear(%{pear_channel}/HttpKernel) >= 2.1.0
BuildRequires:    php-pear(%{pear_channel}/Form) >= 2.1.0
BuildRequires:    php-pear(%{pear_channel}/Routing) >= 2.1.0
BuildRequires:    php-pear(%{pear_channel}/Validator) >= 2.1.0
# TODO: Add DoctrineCommon and DoctrineDBAL (>=2.2,<2.4-dev) when available
# Test requires: phpci
BuildRequires:    php-date
BuildRequires:    php-hash
BuildRequires:    php-json
BuildRequires:    php-openssl
BuildRequires:    php-pcre
BuildRequires:    php-pdo
BuildRequires:    php-reflection
BuildRequires:    php-spl

Requires:         php(language) >= %{php_min_ver}
Requires:         php-pear(PEAR)
Requires:         php-channel(%{pear_channel})
Requires:         php-pear(%{pear_channel}/EventDispatcher) >= 2.1.0
Requires:         php-pear(%{pear_channel}/HttpFoundation) >= 2.1.0
Requires:         php-pear(%{pear_channel}/HttpKernel) >= 2.1.0
Requires(post):   %{__pear}
Requires(postun): %{__pear}
# phpci requires
Requires:         php-date
Requires:         php-hash
Requires:         php-json
Requires:         php-openssl
Requires:         php-pcre
Requires:         php-pdo
Requires:         php-reflection
Requires:         php-spl
# Optional requires
Requires:         php-pear(%{pear_channel}/ClassLoader) >= 2.1.0
Requires:         php-pear(%{pear_channel}/Finder) >= 2.1.0
Requires:         php-pear(%{pear_channel}/Form) >= 2.1.0
Requires:         php-pear(%{pear_channel}/Routing) >= 2.1.0
Requires:         php-pear(%{pear_channel}/Validator) >= 2.1.0
# TODO: Add DoctrineDBAL (>=2.2,<2.4-dev) when available

Provides:         php-pear(%{pear_channel}/%{pear_name}) = %{version}

%description
Security provides an infrastructure for sophisticated authorization systems,
which makes it possible to easily separate the actual authorization logic from
so called user providers that hold the users credentials. It is inspired by
the Java Spring framework.

Optional dependencies: DoctrineCommon and DoctrineDBAL


%prep
%setup -q -c

# Patches
cd %{pear_name}-%{version}
%patch0 -p0
cd ..

# Modify PEAR package.xml file:
# - Remove .gitignore file
# - Change role from "php" to "doc" for CHANGELOG.md file
# - Change role from "php" to "test" for all test files
# - Remove md5sum from bootsrap.php file since it was patched
sed -e '/.git/d' \
    -e '/CHANGELOG.md/s/role="php"/role="doc"/' \
    -e '/phpunit.xml.dist/s/role="php"/role="test"/' \
    -e '/Tests/s/role="php"/role="test"/' \
    -e '/bootstrap.php/s/md5sum="[^"]*"\s*//' \
    -i package.xml

# package.xml is version 2.0
mv package.xml %{pear_name}-%{version}/%{name}.xml


%build
# Empty build section, nothing required


%install
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%check
cd %{pear_name}-%{version}/Symfony/Component/%{pear_name}
%{_bindir}/phpunit


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Symfony/Component/%{pear_name}
%{pear_testdir}/%{pear_name}


%changelog
* Tue Oct 30 2012 Remi Collet <RPMS@FamilleCollet.com> 2.1.3-1
- sync with rawhide, update to 2.1.3

* Sat Oct 27 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.1.2-1
- Updated to upstream version 2.1.2
- PHP minimum version 5.3.3 instead of 5.3.2
- Require other components ">= 2.1.0" instead of "= %%{version}"
- Added Validator require
- Added PEAR package.xml modifications
- Added patch for tests' bootstrap.php
- Added tests (%%check)
- Changed RPM_BUILD_ROOT to %%{buildroot}
- Added %%global pear_metadir

* Sat Oct  6 2012 Remi Collet <RPMS@FamilleCollet.com> 2.1.2-1
- update to 2.1.2

* Sat Sep 15 2012 Remi Collet <RPMS@FamilleCollet.com> 2.0.17-1
- Update to 2.0.17, backport for remi repository

* Sat Sep 15 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.17-1
- Updated to upstream version 2.0.17

* Fri Jul 20 2012 Remi Collet <RPMS@FamilleCollet.com> 2.0.16-1
- Update to 2.0.16, backport for remi repository

* Wed Jul 18 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.16-1
- Updated to upstream version 2.0.16
- Removed changed PEAR role of *.sql files from doc to php (fixed upstream)
- Minor syntax updates

* Mon Jul 03 2012 Remi Collet <RPMS@FamilleCollet.com> 2.0.15-3
- backport for remi repository

* Sat Jun 30 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.15-3
- Added php-pdo require
- Updated %%description
- Changed PEAR role of *.sql files from doc to php.

* Mon Jun 11 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.15-2
- Added php-pear(%%{pear_channel}/ClassLoader) require
- Added php-pear(%%{pear_channel}/Finder) require
- Added php-pear(%%{pear_channel}/Form) require
- Added php-pear(%%{pear_channel}/Routing) require

* Wed May 30 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.15-1
- Updated to upstream version 2.0.15
- Removed "BuildRequires: php-pear >= 1:1.4.9-1.2"
- Updated %%prep section
- Removed cleaning buildroot from %%install section
- Removed documentation move from %%install section (fixed upstream)
- Removed %%clean section
- Updated %%doc in %%files section

* Sun May 20 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.14-3
- Moved documentation to correct location

* Sun May 20 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.14-2
- Removed BuildRoot
- Changed php require to php-common
- Added the following requires based on phpci results:
  php-date, php-hash, php-json, php-openssl, php-pcre, php-reflection,
  php-spl
- Removed %%defattr from %%files section
- Removed ownership for directories already owned by required packages

* Fri May 18 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.14-1
- Updated to upstream version 2.0.14
- %%global instead of %%define
- Removed unnecessary cd from %%build section

* Wed May 2 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.13-1
- Updated to upstream version 2.0.13

* Sat Apr 21 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.12-1
- Initial package
