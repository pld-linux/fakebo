Summary:	Fakes trojan servers and logs incoming requests
Summary(pl.UTF-8):	Program udający trojany i logujący nadchodzące połączenia
Name:		fakebo
Version:	0.4.1
Release:	6
License:	GPL v2
Group:		Networking/Daemons
Source0:	ftp://ftp.linux.hr/pub/fakebo/%{name}-%{version}.tar.gz
# Source0-md5:	442b48ba44250104c30a6e7975230b7c
Source1:	%{name}.init
URL:		http://cvs.linux.hr/fakebo/
BuildRequires:	autoconf
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FakeBO fakes trojan server responses (Back Orifice, NetBus, etc.) and
logs every attempt to a logfile or stdout. It is able to send fake
pings and replies back to the client trying to access your system.

%description -l pl.UTF-8
FakeBO udaje odpowiedzi trojanów (Back Orifice, NetBus, itp.) i loguje
każdą próbę do pliku z logiem lub na standardowe wyjście. Jest on
zdolny do wysyłania fałszywych pingów i odpowiedzi z powrotem do
klienta próbującego uzyskać dostęp do twojego systemu.

%prep
%setup -q

%build
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/fakebo

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add fakebo
%service fakebo restart "fakebo daemon"

%preun
if [ "$1" = "0" ]; then
	%service fakebo stop
	/sbin/chkconfig --del fakebo
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog HACKING NEWS README TODO custom.replies
%attr(755,root,root) %{_bindir}/fakebo
%attr(754,root,root) /etc/rc.d/init.d/fakebo
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fakebo.conf
%{_mandir}/man1/fakebo.1*
