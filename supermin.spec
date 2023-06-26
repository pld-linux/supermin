#
# Conditional build:
%bcond_with	rpm5	# build with rpm5

Summary:	Tool for creating supermin appliances
Summary(pl.UTF-8):	Narzędzie do tworzenia minimalistycznych instalacji
Name:		supermin
Version:	5.2.2
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	https://download.libguestfs.org/supermin/5.2-stable/%{name}-%{version}.tar.gz
# Source0-md5:	44cf367b27f645e8db7e8ae3ae5bad02
Patch0:		%{name}-rpm5.patch
Patch1:		pld.patch
URL:		https://people.redhat.com/~rjones/supermin/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	e2fsprogs
BuildRequires:	e2fsprogs-devel
BuildRequires:	gawk
BuildRequires:	glibc-static
BuildRequires:	libcom_err-devel
BuildRequires:	ocaml >= 3.04-7
BuildRequires:	ocaml-findlib
BuildRequires:	pkgconfig
# perldoc checked by configure and required for installation
# pod2man is actually used but not required as release contains
# up-to-date man page
BuildRequires:	perl-perldoc
#BuildRequires:	perl-tools-pod
BuildRequires:	rpm-devel
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
Requires:	cpio
Requires:	e2fsprogs
Requires:	rpm
Requires:	rpm-utils
Suggests:	qemu
Suggests:	dnf
Suggests:	dnf-plugins-core
Suggests:	dnf-utils
Obsoletes:	febootstrap < 4
Obsoletes:	febootstrap-supermin-helper < 4
Obsoletes:	supermin-helper < 5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Supermin is a tool for building supermin appliances. These are tiny
appliances [similar to virtual machines], usually around 100KB in
size, which get fully instantiated on-the-fly in a fraction of a
second when you need to boot one of them.

%description -l pl.UTF-8
Supermin to narzędzie do tworzenia minimalistycznych instalacji
zwanych "appliance". Są to małe instalacje (podobne do maszyn
wirtualnych), zwykle mające ok. 100kB, które można zainstalować w
całości w locie w ciągu ułamku sekundy, kiedy zachodzi potrzeba
uruchomienia takowej.

%prep
%setup -q
%{?with_rpm5:%patch0 -p1}
%patch1 -p1

%build
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	APT_GET="apt-get" \
	APTITUDE="aptitude" \
	CPIO="cpio" \
	DNF="dnf" \
	DPKG="dpkg" \
	MKE2FS=/sbin/mke2fs \
	PACMAN="pacman" \
	RPM="rpm" \
	RPM2CPIO="rpm2cpio" \
	YUMDOWNLOADER="yumdownloader" \
	--disable-network-tests

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
rm -vf $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/Makefile*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README TODO
%attr(755,root,root) %{_bindir}/supermin
%{_mandir}/man1/supermin.1*
%{_examplesdir}/%{name}-%{version}
