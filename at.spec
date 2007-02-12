Summary:	at job spooler
Summary(de.UTF-8):   at-Job-Spooler
Summary(es.UTF-8):   Gestionario de tareas
Summary(fr.UTF-8):   Gestionnaire de taches at
Summary(pl.UTF-8):   Demon kontroli zadań
Summary(pt_BR.UTF-8):   Spooler de jobs at
Summary(ru.UTF-8):   Утилиты для отложенного запуска заданий
Summary(tr.UTF-8):   ş düzenleyici
Summary(uk.UTF-8):   Утиліти для відкладеного запуску завдань
Name:		at
Version:	3.1.8
Release:	32
License:	GPL
Group:		Daemons
Source0:	ftp://tsx-11.mit.edu/pub/linux/sources/usr.bin/%{name}-%{version}.tar.gz
# Source0-md5:	ded9b0e4d153cf073349e75027d09e8e
Source1:	%{name}d.init
Source2:	%{name}.sysconfig
Source3:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-non-english-man-pages.tar.bz2
# Source3-md5:	3a35eff8786f0c91cd3193cee9d9a076
Patch0:		%{name}-lockfile.patch
Patch1:		%{name}-install.patch
Patch2:		%{name}-man.patch
Patch3:		%{name}.patch
Patch4:		%{name}-typo.patch
Patch5:		%{name}-sigchld.patch
Patch6:		%{name}-sendmail.patch
Patch7:		%{name}-debian.patch
Patch8:		%{name}-buflen.patch
Patch9:		%{name}-configure-no_cron.patch
Patch10:	%{name}-pld_noenglish_man.patch
Patch11:	%{name}-heapcorruption.patch
Patch12:	%{name}-open.patch
Patch13:	%{name}-dst.patch
Patch14:	%{name}-env-tng.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	flex
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post):	fileutils
Requires(post,preun):	/sbin/chkconfig
Requires:	/usr/lib/sendmail
Requires:	rc-scripts >= 0.2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/at

%description
at and batch read commands from standard input or from a specified
file. at allows you to specify that a command will be run at a
particular time (now or a specified time in the future). Batch will
execute commands when the system load levels drop to a particular
level. Both commands use /bin/sh to run the commands.

%description -l de.UTF-8
Stapelverarbeitung von Lesebefehlen von einer Standard- oder einer
genannten Datei zu einem späteren Zeitpunkt unter Verwendung von
/bin/sh.

%description -l es.UTF-8
At y batch leen comandos de la entrada padrón o de un archivo
especificado que son ejecutados más tarde, usando /bin/sh.

%description -l fr.UTF-8
at et batch lisent, sur l'entrée standard ou dans un fichier, des
commandes qui doivent être exécutées plus tard en utilisant /bin/sh.

%description -l pl.UTF-8
at i batch czytają komendy ze standardowego wejścia lub specyficznego
pliku, które są następnie wykonywane o określonej godzinie, przy
pomocy /bin/sh.

%description -l pt_BR.UTF-8
at e batch lêem comandos da entrada padrão ou de um arquivo
especificado que são executados mais tarde, usando /bin/sh.

%description -l ru.UTF-8
at и batch читают команды со стандартного ввода или указанного файла.
at позволяет запустить команду в определенное время (сейчас или в
будущем). batch исполняет команды когда загрузка системы падает до
определенного значения. Обе программы используют /bin/sh для запуска
других программ.

%description -l tr.UTF-8
at ve batch /bin/sh kabuğunu kullanarak, belli bir saatte çalıştırmak
üzere standart girişden ya da bir dosyadan komut okur.

%description -l uk.UTF-8
at та batch читають команди зі стандартного вводу або зазначеного
файлу. At дозволяє запустити команду в зазначений час (зараз або у
майбутньому). batch виконує команди коли завантаження системи падає до
визначеного значення. Обидві програми використовують /bin/sh для
запуску інших програм.

%prep
%setup -q -a3
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p0
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1

%build
cp -f /usr/share/automake/config.* .
%{__aclocal}
%{__autoconf}
%configure \
	--with-atspool=/var/spool/at/spool \
	--with-jobdir=/var/spool/at \
	--with-etcdir=%{_sysconfdir} \
	--with-daemon_username=root \
	--with-daemon_groupname=root
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	IROOT=$RPM_BUILD_ROOT

install at.deny $RPM_BUILD_ROOT%{_sysconfdir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/atd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/atd

rm -f $RPM_BUILD_ROOT%{_mandir}/man1/{atq,atrm,batch}.1
rm -f $RPM_BUILD_ROOT%{_mandir}/man5/at_deny.5

echo .so at.1 > $RPM_BUILD_ROOT%{_mandir}/man1/atq.1
echo .so at.1 > $RPM_BUILD_ROOT%{_mandir}/man1/atrm.1
echo .so at.1 > $RPM_BUILD_ROOT%{_mandir}/man1/batch.1

echo .so at_allow.5 > $RPM_BUILD_ROOT%{_mandir}/man5/at_deny.5
echo .so at_allow.5 > $RPM_BUILD_ROOT%{_mandir}/man5/at_access.5

for a in es fi fr hu id it ja ko pl; do
	install -d $RPM_BUILD_ROOT%{_mandir}/{$a,$a/man{1,5,8}}
	for b in $a/man[158]/*; do
		install $b $RPM_BUILD_ROOT%{_mandir}/$b
	done
done

touch $RPM_BUILD_ROOT/var/spool/at/.SEQ

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add atd
touch /var/spool/at/.SEQ
%service atd restart "atd daemon"

%preun
if [ "$1" = "0" ] ; then
	%service atd stop
	/sbin/chkconfig --del atd
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog README timespec
%attr(750,root,root) %dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/*
%attr(754,root,root) /etc/rc.d/init.d/atd
%attr(755,root,root) %{_sbindir}/*
%attr(4755,root,root) %{_bindir}/at
%attr(755,root,root) %{_bindir}/atq
%attr(755,root,root) %{_bindir}/atrm
%attr(755,root,root) %{_bindir}/batch
%{_mandir}/man*/*
%lang(es) %{_mandir}/es/man*/*
%lang(fi) %{_mandir}/fi/man*/*
%lang(fr) %{_mandir}/fr/man*/*
%lang(hu) %{_mandir}/hu/man*/*
%lang(id) %{_mandir}/id/man*/*
%lang(it) %{_mandir}/it/man*/*
%lang(ja) %{_mandir}/ja/man*/*
%lang(ko) %{_mandir}/ko/man*/*
%lang(pl) %{_mandir}/pl/man*/*
%attr(750,root,root) %dir /var/spool/at
%attr(750,root,root) %dir /var/spool/at/spool
%attr(600,root,root) %ghost /var/spool/at/.SEQ
