#
# Conditional build:
%bcond_without	apidocs	# API documentation
#
Summary:	ZZipLib - libZ-based ZIP-access Library
Summary(pl.UTF-8):	ZZipLib - biblioteka dostępu do archiwów ZIP
Name:		zziplib
Version:	0.13.72
Release:	1
Epoch:		1
License:	LGPL v2 or MPL 1.1
Group:		Libraries
#Source0Download: https://github.com/gdraheim/zziplib/tags
Source0:	https://github.com/gdraheim/zziplib/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	43555e7eafc5c1a1178a35e716c40500
Patch0:		%{name}-fpe.patch
Patch1:		%{name}-manpages.patch
URL:		http://zziplib.sourceforge.net/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake >= 1:1.7
BuildRequires:	docbook-dtd412-xml
BuildRequires:	libtool >= 1:1.4.3
BuildRequires:	pkgconfig
BuildRequires:	python
BuildRequires:	python-modules
BuildRequires:	xmlto
BuildRequires:	zip
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ZZipLib provides read access to zipped files in a zip-archive, using
compression based solely on free algorithms provided by zlib. ZZipLib
provides an additional API to transparently access files being either
real files or zipped files with the same filepath argument. This is
handy to package many files being shared data into a single zip file -
as it is sometimes used with gamedata or script repositories. The
library itself is fully multithreaded, and it is namespace clean using
the zzip_ prefix for its exports and declarations.

%description -l pl.UTF-8
ZZipLib pozwala na odczyt plików skompresowanych w archiwach zip,
używając do dekompresji wolnodostępnych algorytmów z biblioteki zlib.
ZZipLib dostarcza dodatkowe API do przezroczystego dostępu do plików
rzeczywistych lub umieszczonych w archiwach zip przy pomocy takiej
samej ścieżki. Jest to przydatne przy trzymaniu wielu plików w jednym
archiwum, co bywa stosowane w przypadku danych dla gier lub
repozytoriów. Biblioteka jest w pełni wielowątkowa i ma czystą
przestrzeń nazw (używa prefiksu zzip_).

%package devel
Summary:	ZZipLib - Development Files
Summary(pl.UTF-8):	Pliki dla programistów ZZipLib
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
These are the header files needed to develop programs using zziplib.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne do tworzenia programów
korzystających z biblioteki zziplib.

%package static
Summary:	ZZipLib static library
Summary(pl.UTF-8):	Statyczna biblioteka ZZipLib
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
ZZipLib static library.

%description static -l pl.UTF-8
Statyczna biblioteka ZZipLib.

%package apidocs
Summary:	API documentation for ZZipLib library
Summary(pl.UTF-8):	Dokumentacja API biblioteki ZZipLib
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for ZZipLib library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki ZZipLib.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

# stick to autotools for now
%{__mv} old.configure.ac configure.ac
%{__rm} GNUmakefile

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure

%{__make}
%{__make} -j1 check
%if %{with apidocs}
%{__make} doc
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with apidocs}
%{__make} -C docs install-man3 \
	DESTDIR=$RPM_BUILD_ROOT
%endif

# we don't need these compat symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libzzip*-0.so.{10,11,12}
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libzzip*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog README TODO docs/COPYING.ZLIB
%attr(755,root,root) %{_bindir}/zzcat
%attr(755,root,root) %{_bindir}/zzdir
%attr(755,root,root) %{_bindir}/zzxor*
%attr(755,root,root) %{_bindir}/unzip-mem
%attr(755,root,root) %{_bindir}/unzzip*
%attr(755,root,root) %{_libdir}/libzzip-0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libzzip-0.so.13
%attr(755,root,root) %{_libdir}/libzzipfseeko-0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libzzipfseeko-0.so.13
%attr(755,root,root) %{_libdir}/libzzipmmapped-0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libzzipmmapped-0.so.13
%attr(755,root,root) %{_libdir}/libzzipwrap-0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libzzipwrap-0.so.13

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libzzip.so
%attr(755,root,root) %{_libdir}/libzzipfseeko.so
%attr(755,root,root) %{_libdir}/libzzipmmapped.so
%attr(755,root,root) %{_libdir}/libzzipwrap.so
%{_includedir}/zzip
%{_includedir}/zzip*.h
%if %{with apidocs}
%{_mandir}/man3/__zzip_*.3*
%{_mandir}/man3/zzip_*.3*
%endif
%{_pkgconfigdir}/zzip-zlib-config.pc
%{_pkgconfigdir}/zzipfseeko.pc
%{_pkgconfigdir}/zziplib.pc
%{_pkgconfigdir}/zzipmmapped.pc
%{_pkgconfigdir}/zzipwrap.pc
%{_aclocaldir}/zziplib.m4

%files static
%defattr(644,root,root,755)
%{_libdir}/libzzip.a
%{_libdir}/libzzipfseeko.a
%{_libdir}/libzzipmmapped.a
%{_libdir}/libzzipwrap.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc docs/*.{html,css}
%endif
