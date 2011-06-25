Name:           perl-FusionInventory-Agent-Task-ESX
Version:        1.1.1
Release:        1%{?dist}
Summary:        vCenter/ESX/ESXi remote inventory for FusionInventory Agent
License:        GPLv2+
Group:          Development/Libraries

URL:            http://forge.fusioninventory.org/projects/fusioninventory-agent-task-esx
Source0:        http://search.cpan.org/CPAN/authors/id/F/FU/FUSINV/FusionInventory-Agent-Task-ESX-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl >= 1:5.8.0
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(FusionInventory::Agent) >= 2.1.9
BuildRequires:  perl(HTTP::Cookies)
BuildRequires:  perl(LWP::UserAgent)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(XML::TreePP)

Requires:       perl(FusionInventory::Agent) >= 2.1.9
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}


%description
You can import the generated files in:
- GLPI with FusionInventory for GLPI
- ocsinventory
- Uranos


%prep
%setup -q -n FusionInventory-Agent-Task-ESX-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHOR Changes README LICENSE
%{_bindir}/fusioninventory-esx
%{perl_vendorlib}/FusionInventory/Agent/Task/ESX*
%{perl_vendorlib}/FusionInventory/VMware
%{_mandir}/man1/fusioninventory-esx.*


%changelog
* Sat Jun 24 2011 Remi Collet <Fedora@famillecollet.com> 1.1.1-1
- update to 1.1.1
  http://cpansearch.perl.org/src/FUSINV/FusionInventory-Agent-Task-ESX-1.1.1/Changes

* Wed Mar 30 2011 Remi Collet <Fedora@famillecollet.com> 1.0.1-1
- update to 1.0.1 (with LICENSE)

* Wed Mar 30 2011 Remi Collet <Fedora@famillecollet.com> 1.0.0-1
- Specfile autogenerated by cpanspec 1.78.
- spec cleanup

