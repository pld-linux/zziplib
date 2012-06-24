Summary:	ZZipLib - libZ-based ZIP-access Library
Summary(pl):	ZZipLib - biblioteka dost�pu do archiw�w ZIP
Name:		zziplib
Version:	0.12.23
Release:	1
Epoch:		1
License:	LGPL with exceptions (see COPYING.ZZIP)
Vendor:		Guido Draheim <guidod@gmx.de>
Group:		Libraries
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5: 693b93a36162d7d3e90f25f5bc71074b
URL:		http://zziplib.sourceforge.net/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libtool >= 1:1.4.3
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
ZZipLib pozwala na odczyt plik�w skompresowanych w archiwach zip,
u�ywaj�c do dekompresji wolnodost�pnych algorytm�w z biblioteki zlib.
ZZipLib dostarcza dodatkowe API do przezroczystego dost�pu do plik�w
rzeczywistych lub umieszczonych w archiwach zip przy pomocy takiej
samej �cie�ki. Jest to przydatne przy trzymaniu wielu plik�w w jednym
archiwum, co bywa stosowane w przypadku danych dla gier lub
repozytori�w. Biblioteka jest w pe�ni wielow�tkowa i ma czyst�
przestrze� nazw (u�ywa prefiksu zzip_).

%package devel
Summary:	ZZipLib - Development Files
Summary(pl):	Pliki dla programist�w ZZipLib
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
These are the header files needed to develop programs using zziplib.

%description devel -l pl
Ten pakiet zawiera plikia nag��wkowe potrzebne do tworzenia program�w
korzystaj�cych z biblioteki zziplib.

%package static
Summary:	ZZipLib static library
Summary(pl):	Statyczna biblioteka ZZipLib
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
ZZipLib static library.

%description static -l pl
Statyczna biblioteka ZZipLib.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure

%{__make}
%{__make} doc

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} install-man3 -C docs \
	DESTDIR=$RPM_BUILD_ROOT

rm -f docs/zziplib[012].html

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog TODO docs/COPYING.Z*
%attr(755,root,root) %{_bindir}/zz[!i]*
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%doc docs/*.html
%attr(755,root,root) %{_bindir}/zzip-config
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*
%{_mandir}/man3/*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
