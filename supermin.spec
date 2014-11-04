Summary:	Tool for creating supermin appliances
Summary(pl.UTF-8):	Narzędzie do tworzenia minimalistycznych instalacji
Name:		supermin
Version:	5.1.11
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	http://libguestfs.org/download/supermin/%{name}-%{version}.tar.gz
# Source0-md5:	5843cd7016022d4944227c3019c8b225
Patch0:		%{name}-rpm5.patch
URL:		http://people.redhat.com/~rjones/supermin/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	e2fsprogs
BuildRequires:	e2fsprogs-devel
BuildRequires:	gawk
BuildRequires:	libcom_err-devel
BuildRequires:	ocaml >= 3.04-7
BuildRequires:	ocaml-findlib
BuildRequires:	pkgconfig
# not needed in releases (BTW: perldoc is checked, but pod2man is actually used)
#BuildRequires:	perl-perldoc
#BuildRequires:	perl-tools-pod
BuildRequires:	rpm-devel >= 5
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
Requires:	cpio
Requires:	e2fsprogs
Requires:	rpm
Requires:	rpm-utils
Suggests:	filelight
Suggests:	qemu
Suggests:	yum >= 3.2
Suggests:	yum-utils
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
%patch0 -p1

%build
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	APT_CACHE="apt-cache" \
	APTITUDE="aptitude" \
	CPIO="cpio" \
	DPKG="dpkg" \
	MKE2FS=/sbin/mke2fs \
	PACMAN="pacman" \
	RPM="rpm" \
	RPM2CPIO="rpm2cpio" \
	YUM="yum" \
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
