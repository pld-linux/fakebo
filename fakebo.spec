Summary:	Fakes trojan servers and logs incoming requests
Summary(pl):	Program udaj±cy trojany i loguj±cy nadchodz±ce po³±czenia
Name:		fakebo
Version:	0.4.1
Release:	3
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://ftp.linux.hr/pub/fakebo/%{name}-%{version}.tar.gz
Source1:	%{name}.init
URL:		http://cvs.linux.hr/fakebo/
BuildRequires:	autoconf
Prereq:		rc-scripts
Prereq:		/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FakeBO fakes trojan server responses (Back Orifice, NetBus, etc.) and
logs every attempt to a logfile or stdout. It is able to send fake
pings and replies back to the client trying to access your system.

%description -l pl
FakeBO udaje odpowiedzi trojanów (Back Orifice, NetBus, itp.) i loguje
ka¿d± próbê do pliku z logiem lub na standardowe wyj¶cie. Jest on
zdolny do wysy³ania fa³szywych pingów i odpowiedzi z powrotem do
klienta próbuj±cego uzyskaæ dostêp do twojego systemu.

%prep
%setup -q

%build
autoconf
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/fakebo

gzip -9nf HACKING AUTHORS TODO NEWS ChangeLog README custom.replies

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add fakebo
if [ -f /var/lock/subsys/fakebo ]; then
	/etc/rc.d/init.d/fakebo restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/fakebo start\" to start fakebo daemon."
fi


%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/fakebo ]; then
		/etc/rc.d/init.d/fakebo stop 1>&2
	fi
	/sbin/chkconfig --del fakebo
fi

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_bindir}/fakebo
%attr(754,root,root) /etc/rc.d/init.d/fakebo
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/fakebo.conf
%{_mandir}/man1/fakebo.1*
