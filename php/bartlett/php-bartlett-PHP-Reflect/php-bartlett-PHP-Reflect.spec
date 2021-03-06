%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global channel   bartlett.laurent-laville.org
%global pear_name PHP_Reflect

%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6
%global withhtmldoc 1
%else
%global withhtmldoc 0
%endif


Name:           php-bartlett-PHP-Reflect
Version:        1.0.2
Release:        2%{?dist}
Summary:        Adds the ability to reverse-engineer PHP

Group:          Development/Libraries
License:        BSD
URL:            http://bartlett.laurent-laville.org/
Source0:        http://%{channel}/get/%{pear_name}-%{version}%{?prever}.tgz

# for old asciidoc version https://bugzilla.redhat.com/556171
Patch0:         PHP_Reflect-docs.patch
# Don't install .js (unused)
Patch1:         PHP_Reflect-deljs.patch
# Install generated doc using pear command
Patch2:         PHP_Reflect-addhtml.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.9.0
BuildRequires:  php-channel(%{channel})
# to run test suite
BuildRequires:  php-pear(pear.phpunit.de/PHPUnit) >= 3.5.0
%if %{withhtmldoc}
# to build HTML documentation
BuildRequires:  php-pear(pear.phing.info/phing)
BuildRequires:  asciidoc >= 8.4.0
%endif

Requires:       php-pear(PEAR) >= 1.9.0
Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-channel(%{channel})

Provides:       php-pear(%{channel}/%{pear_name}) = %{version}%{?prever}


%description
PHP_Reflect adds the ability to reverse-engineer classes, interfaces,
functions, constants and more, by connecting php callbacks to other tokens.

%if %{withhtmldoc}
HTML Documentation:  %{pear_docdir}/%{pear_name}/docs/index.html
%endif


%prep
%setup -q -c

# Package is V2
cd %{pear_name}-%{version}%{?prever}
mv -f ../package.xml %{name}.xml

%patch0 -p0 -b .fix
%patch1 -p1 -b .deljs
%if %{withhtmldoc}
%patch2 -p1 -b .addhtml
%endif


%build
cd %{pear_name}-%{version}%{?prever}

%if %{withhtmldoc}
# Generate the HTML documentation
phing -f docs/build-phing.xml \
      -Dhomedir=$PWD \
      -Dasciidoc.home=%{_datadir}/asciidoc \
      make-full-docs

# Asciidoc fails silently
# Check that our patch for installed doc is ok
cpt=$(find docs -name \*.html | wc -l)
echo "File generated:$cpt, expected:9"
[ $cpt -eq 9 ] || exit 1
%endif

# restore unpatched docs (for install and checksum)
mv docs/index.txt.fix docs/index.txt


%install
rm -rf %{buildroot}
cd %{pear_name}-%{version}%{?prever}

%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_phpdir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}



%check
cd %{pear_name}-%{version}%{?prever}

# Version 1.0.2 : OK (25 tests, 42 assertions)
%{_bindir}/phpunit \
  -d date.timezone=UTC \
  --bootstrap %{buildroot}%{pear_phpdir}/Bartlett/PHP/Reflect/Autoload.php \
  tests


%clean
rm -rf %{buildroot}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Bartlett
%{pear_testdir}/PHP_Reflect


%changelog
* Mon Sep 19 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.0.2-2
- remove unused .js and improve installation of generated doc
- use buildroot macro

* Mon Jul 18 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.0.2-1
- Version 1.0.2 (stable) - API 1.0.0 (stable)

* Sat Jun 16 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.0.1-1
- Version 1.0.1 (stable) - API 1.0.0 (stable)

* Sat Jun 02 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.0.0-1
- Version 1.0.0 (stable) - API 1.0.0 (stable)
- add HTML documentation

* Tue Apr 26 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.0.0-0.1.RC1
- Version 1.0.0RC1 (beta) - API 1.0.0 (beta)

* Sat Apr 17 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.7.0-1
- Version 0.7.0 (beta) - API 0.7.0 (beta)

* Mon Apr 11 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.6.0-1
- Version 0.6.0 (beta) - API 0.6.0 (beta)

* Wed Apr 06 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.5.1-1
- Version 0.5.1 (beta) - API 0.5.0 (beta)

* Fri Mar 25 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.5.0-1
- Version 0.5.0 (beta) - API 0.5.0 (beta)

* Wed Feb 25 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.4.0-1
- Version 0.4.0 (beta)
- Initial RPM package

