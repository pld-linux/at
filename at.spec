Summary:	at job spooler
Summary(de):	at-Job-Spooler
Summary(fr):	Gestionnaire de taches at
Summary(pl):	Demon kontroli zadañ
Summary(tr):	þ düzenleyici
Name:		at
Version:	3.1.8
Release:	16
License:	GPL
Group:		Daemons
Group(de):	Server
Group(pl):	Serwery
Source0:	ftp://tsx-11.mit.edu/pub/linux/sources/usr.bin/%{name}-%{version}.tar.gz
Source1:	%{name}d.init
Source2:	%{name}.sysconfig
Source3:	%{name}.1.pl
Source4:	%{name}_allow.5.pl
Source5:	%{name}d.8.pl
Source6:	%{name}run.8.pl
Patch0:		%{name}-lockfile.patch
Patch1:		%{name}-install.patch
Patch2:		%{name}-man.patch
Patch3:		%{name}.patch
Patch4:		%{name}-typo.patch
Patch5:		%{name}-sigchld.patch
Patch6:		%{name}-sendmail.patch
Patch7:		%{name}-debian.patch
Patch8:		%{name}-buflen.patch
Prereq:		fileutils
Prereq:		/sbin/chkconfig
Prereq:		rc-scripts >= 0.2.0
Requires:	/usr/lib/sendmail
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/at

%description
At and batch read commands from standard input or from a specified
file. At allows you to specify that a command will be run at a
particular time (now or a specified time in the future). Batch will
execute commands when the system load levels drop to a particular
level. Both commands use /bin/sh to run the commands.

%description -l de
Stapelverarbeitung von Lesebefehlen von einer Standard- oder einer
genannten Datei zu einem späteren Zeitpunkt unter Verwendung von
/bin/sh.

%description -l fr
at et batch lisent, sur l'entrée standard ou dans un fichier, des
commandes qui doivent être exécutées plus tard en utilisant /bin/sh.

%description -l pl
At i batch czytaj± komendy ze standardowego wej¶cia lub specyficznego
pliku, które s± nastêpnie wykonywane o okre¶lonej godzinie, przy
pomocy /bin/sh.

%description -l tr
at ve batch /bin/sh kabuðunu kullanarak, belli bir saatte çalýþtýrmak
üzere standart giriþden ya da bir dosyadan komut okur.

%prep
%setup -q
%patch0 -p1 
%patch1 -p1 
%patch2 -p1 
%patch3 -p1 
%patch4 -p1 
%patch5 -p1 
%patch6 -p1
%patch7 -p1
%patch8 -p1

%build
aclocal
autoconf
%configure \
	--with-atspool=/var/spool/at/spool \
	--with-jobdir=/var/spool/at \
	--with-etcdir=%{_sysconfdir} \
	--with-daemon_username=root \
	--with-daemon_groupname=root
%{__make} 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig},%{_mandir}/pl/man{1,5,8}}

%{__make} IROOT=$RPM_BUILD_ROOT install

install at.deny $RPM_BUILD_ROOT%{_sysconfdir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/atd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/at

rm -f $RPM_BUILD_ROOT%{_mandir}/man1/{atq,atrm,batch}.1
rm -f $RPM_BUILD_ROOT%{_mandir}/man5/at_deny.5

echo .so at.1 > $RPM_BUILD_ROOT%{_mandir}/man1/atq.1
echo .so at.1 > $RPM_BUILD_ROOT%{_mandir}/man1/atrm.1
echo .so at.1 > $RPM_BUILD_ROOT%{_mandir}/man1/batch.1

echo .so at_allow.5 > $RPM_BUILD_ROOT%{_mandir}/man5/at_deny.5
echo .so at_allow.5 > $RPM_BUILD_ROOT%{_mandir}/man5/at_acces.5

install %{SOURCE3} $RPM_BUILD_ROOT%{_mandir}/pl/man1/at.1
echo ".so at.1" > $RPM_BUILD_ROOT%{_mandir}/pl/man1/atq.1
echo ".so at.1" > $RPM_BUILD_ROOT%{_mandir}/pl/man1/atrm.1
echo ".so at.1" > $RPM_BUILD_ROOT%{_mandir}/pl/man1/batch.1
install %{SOURCE4} $RPM_BUILD_ROOT%{_mandir}/pl/man5/at_allow.5
echo ".so at_allow.5" > $RPM_BUILD_ROOT%{_mandir}/pl/man5/at.access.5
echo ".so at_allow.5" > $RPM_BUILD_ROOT%{_mandir}/pl/man5/at.deny.5
install %{SOURCE5} $RPM_BUILD_ROOT%{_mandir}/pl/man8/atd.8
install %{SOURCE6} $RPM_BUILD_ROOT%{_mandir}/pl/man8/atrun.8

touch $RPM_BUILD_ROOT/var/spool/at/.SEQ

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/{man*/*,pl/man?/*} \
	ChangeLog README

%clean
rm -rf $RPM_BUILD_ROOT

%post
NAME=atd; DESC="atd daemon"; %chkconfig_post

%preun
NAME=atd; %chkconfig_preun

%files
%defattr(644,root,root,755)
%doc {ChangeLog,README}.gz

%attr(750,root,root) %dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*
%attr(640,root,root) %config %verify(not size mtime md5) /etc/sysconfig/*

%attr(754,root,root) /etc/rc.d/init.d/atd
%attr(755,root,root) %{_sbindir}/*

%attr(4755,root,root) %{_bindir}/at

%attr(755,root,root) %{_bindir}/atq
%attr(755,root,root) %{_bindir}/atrm
%attr(755,root,root) %{_bindir}/batch

%{_mandir}/man*/*
%lang(pl) %{_mandir}/pl/man*/*

%attr(750,root,root) %dir /var/spool/at
%attr(750,root,root) %dir /var/spool/at/spool
%attr(600,root,root) %ghost /var/spool/at/.SEQ
