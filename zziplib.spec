#
# Conditional build:
%bcond_without	doc	# - build witout documentation
#
Summary:	ZZipLib - libZ-based ZIP-access Library
Summary(pl):	ZZipLib - biblioteka dostêpu do archiwów ZIP
Name:		zziplib
Version:	0.13.36
Release:	1
Epoch:		1
License:	LGPL with exceptions (see COPYING.ZZIP)
Vendor:		Guido Draheim <guidod@gmx.de>
Group:		Libraries
Source0:	http://dl.sourceforge.net/zziplib/%{name}-%{version}.tar.bz2
# Source0-md5:	263f642825b8a9d56f7bfc26404e965d
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

%description -l pl
ZZipLib pozwala na odczyt plików skompresowanych w archiwach zip,
u¿ywaj±c do dekompresji wolnodostêpnych algorytmów z biblioteki zlib.
ZZipLib dostarcza dodatkowe API do przezroczystego dostêpu do plików
rzeczywistych lub umieszczonych w archiwach zip przy pomocy takiej
samej ¶cie¿ki. Jest to przydatne przy trzymaniu wielu plików w jednym
archiwum, co bywa stosowane w przypadku danych dla gier lub
repozytoriów. Biblioteka jest w pe³ni wielow±tkowa i ma czyst±
przestrzeñ nazw (u¿ywa prefiksu zzip_).

%package devel
Summary:	ZZipLib - Development Files
Summary(pl):	Pliki dla programistów ZZipLib
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
These are the header files needed to develop programs using zziplib.

%description devel -l pl
Ten pakiet zawiera plikia nag³ówkowe potrzebne do tworzenia programów
korzystaj±cych z biblioteki zziplib.

%package static
Summary:	ZZipLib static library
Summary(pl):	Statyczna biblioteka ZZipLib
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
ZZipLib static library.

%description static -l pl
Statyczna biblioteka ZZipLib.

%prep
%setup -q

%{__perl} -pi -e 's/use strict/#&/' docs/*.pl

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-builddir

%{__make}
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
%attr(755,root,root) %{_bindir}/zz[!i]*
%attr(755,root,root) %{_bindir}/unzz*
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%if %{with doc}
%doc docs/*.html
%endif
#%attr(755,root,root) %{_bindir}/zzip-config
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*
%if %{with doc}
%{_mandir}/man3/*.3*
%endif
%{_pkgconfigdir}/*.pc
%{_aclocaldir}/*.m4

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
