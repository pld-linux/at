Summary:	at job spooler
Summary(de):	at-Job-Spooler
Summary(fr):	Gestionnaire de taches at.
Summary(pl):	Demon kontroli zadañ
Summary(tr):	þ düzenleyici
Name:		at
Version:	3.1.8
Release:	8
Copyright:	GPL
Group:		Daemons
Group(pl):	Serwery
Url:		ftp://jurix.jura.uni-sb.de/pub/linux/sources/system/daemons
Source0:	%{name}-%{version}.tar.gz
Source1:	atd.init
Source2:	at.sysconfig
Patch0:		at-lockfile.patch
Patch1:		at-install.patch
Patch2:		at-man.patch
Patch3:		at.patch
Prereq:		fileutils
Prereq:		/sbin/chkconfig
Requires:	mailx
Requires:	rc-scripts
Buildroot:	/tmp/%{name}-%{version}-root

%description
at and batch read commands from standard input or a specified file
which are to be executed at a later time, using /bin/sh.

%description -l de
Stapelverarbeitung von Lesebefehlen von einer Standard- oder einer 
genannten Datei zu einem späteren Zeitpunkt unter Verwendung von /bin/sh.

%description -l fr
at et batch lisent, sur l'entrée standard ou dans un fichier, des
commandes qui doivent être exécutées plus tard en utilisant /bin/sh.

%description -l pl
At i batch czytaj± komendy ze standardowego wej¶cia lub specyficznego pliku,
które s± nastêpnie wykonywane o okre¶lonej godzinie, przy pomocy /bin/sh.

%description -l tr
at ve batch /bin/sh kabuðunu kullanarak, belli bir saatte çalýþtýrmak üzere
standart giriþden ya da bir dosyadan komut okur.

%prep
%setup -q
%patch0 -p1 
%patch1 -p1 
%patch2 -p1 
%patch3 -p1 

%build
aclocal && autoconf
CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s" \
    ./configure \
	--with-atspool=/var/spool/at/spool \
	--with-jobdir=/var/spool/at \
	--with-etcdir=/etc/at \
	--with-daemon_username=root \
	--with-daemon_groupname=root \
	--mandir=%{_mandir} %{_target_platform}
make 

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

make \
    IROOT=$RPM_BUILD_ROOT \
    install

install at.deny $RPM_BUILD_ROOT/etc/at

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/atd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/at

rm -f $RPM_BUILD_ROOT%{_mandir}/man1/{atq,atrm,batch}.1
rm -f $RPM_BUILD_ROOT%{_mandir}/man5/at_deny.5

echo .so at.1 > $RPM_BUILD_ROOT%{_mandir}/man1/atq.1
echo .so at.1 > $RPM_BUILD_ROOT%{_mandir}/man1/atrm.1
echo .so at.1 > $RPM_BUILD_ROOT%{_mandir}/man1/batch.1

echo .so at_allow.5 > $RPM_BUILD_ROOT%{_mandir}/man5/at_deny.5
echo .so at_allow.5 > $RPM_BUILD_ROOT%{_mandir}/man5/at_acces.5

touch $RPM_BUILD_ROOT/var/spool/at/.SEQ

gzip -9fn $RPM_BUILD_ROOT%{_mandir}/man[158]/* \
	ChangeLog README

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add atd
if [ -f /var/lock/subsys/atd ]; then
	/etc/rc.d/init.d/atd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/atd start\" to start atd daemon."
fi

%preun
if [ "$1" = "0" ] ; then
	/sbin/chkconfig --del atd
	/etc/rc.d/init.d/atd stop >&2
fi

%files
%defattr(644,root,root,755) 
%doc {ChangeLog,README}.gz

%attr(750,root,root) %dir /etc/at
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/at/*
%attr(640,root,root) %config %verify(not size mtime md5) /etc/sysconfig/*

%attr(755,root,root) /etc/rc.d/init.d/atd
%attr(755,root,root) %{_sbindir}/*

%attr(4711,root,root) %{_bindir}/at

%attr(755,root,root) %{_bindir}/atq
%attr(755,root,root) %{_bindir}/atrm
%attr(755,root,root) %{_bindir}/batch

%{_mandir}/man[158]/*

%attr(750,root,root) %dir /var/spool/at
%attr(750,root,root) %dir /var/spool/at/spool
%attr(600,root,root) %ghost /var/spool/at/.SEQ
