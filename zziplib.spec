#
# Conditional build:
%bcond_without	doc	# build without documentation
#
Summary:	ZZipLib - libZ-based ZIP-access Library
Summary(pl.UTF-8):	ZZipLib - biblioteka dostępu do archiwów ZIP
Name:		zziplib
Version:	0.13.58
Release:	1
Epoch:		1
License:	LGPL with exceptions (see COPYING.ZZIP)
Group:		Libraries
Source0:	http://dl.sourceforge.net/zziplib/%{name}-%{version}.tar.bz2
# Source0-md5:	a0f743a5a42ca245b2003ecaea958487
Patch0:		%{name}-ac.patch
Patch1:		%{name}-manpages.patch
Patch2:		%{name}-fetch.patch
URL:		http://zziplib.sourceforge.net/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libtool >= 1:1.4.3
BuildRequires:	xmlto
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
Ten pakiet zawiera plikia nagłówkowe potrzebne do tworzenia programów
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

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-builddir

%{__make}
%{__make} check
%if %{with doc}
%{__make} doc
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with doc}
%{__make} install-man3 -C docs \
	DESTDIR=$RPM_BUILD_ROOT

rm -f docs/zziplib[012].html
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog TODO docs/COPYING.Z*
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
%if %{with doc}
%doc docs/*.html
%endif
%attr(755,root,root) %{_libdir}/libzzip.so
%attr(755,root,root) %{_libdir}/libzzipfseeko.so
%attr(755,root,root) %{_libdir}/libzzipmmapped.so
%attr(755,root,root) %{_libdir}/libzzipwrap.so
%{_libdir}/libzzip.la
%{_libdir}/libzzipfseeko.la
%{_libdir}/libzzipmmapped.la
%{_libdir}/libzzipwrap.la
%{_includedir}/zzip
%{_includedir}/zzip*.h
%if %{with doc}
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
