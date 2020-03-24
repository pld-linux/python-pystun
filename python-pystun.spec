# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

# NOTES:
# - 'module' should match the Python import path (first component?)
# - 'egg_name' should equal to Python egg name
# - 'pypi_name' must match the Python Package Index name
%define		module		stun
%define		egg_name	pystun
%define		pypi_name	pystun
Summary:	A Python STUN client for getting NAT type and external IP
Name:		python-%{pypi_name}
Version:	0.1.0
Release:	1
License:	MIT
Group:		Libraries/Python
Source0:	https://pypi.debian.net/pystun/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	5cefad003e24b1aa04577ddf21a65779
URL:		https://github.com/jtriley/pystun
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
%endif
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Python STUN client for getting NAT type and external IP. PyStun follows RFC 3489.

%package -n python3-%{pypi_name}
Summary:	A Python STUN client for getting NAT type and external IP
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{pypi_name}
A Python STUN client for getting NAT type and external IP. PyStun follows RFC 3489.

%prep
%setup -q -n %{pypi_name}-%{version}

# fix #!/usr/bin/env python -> #!/usr/bin/python:
#%{__sed} -i -e '1s,^#!.*python,#!%{__python},' %{name}.py

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

# when files are installed in other way that standard 'setup.py
# they need to be (re-)compiled
# change %{py_sitedir} to %{py_sitescriptdir} for 'noarch' packages!
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%defattr(644,root,root,755)
%doc README.rst
%attr(755,root,root) %{_bindir}/pystun
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif
