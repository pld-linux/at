Summary:	at job spooler
Summary(de):	at-Job-Spooler
Summary(fr):	Gestionnaire de taches at.
Summary(pl):	Demon kontroli zadañ
Summary(tr):	þ düzenleyici
Name:		at
Version:	3.1.8
Release:	7
Copyright:	GPL
Group:		Daemons
Group(pl):	Serwery
Source0:	ftp://jurix.jura.uni-sb.de/pub/linux/sources/system/daemons/%{name}-%{version}.tar.gz
Source1:	atd.init
Patch0:		at-lockfile.patch
Patch1:		at-install.patch
Patch2:		at-man.patch
Patch3:		at-batch.patch
Patch4:		at.patch
Prereq:		fileutils
Prereq:		/sbin/chkconfig
Requires:	mailx
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
%patch4 -p1 

%build
autoconf
CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s" \
./configure %{_target} \
	--with-atspool=/var/spool/at/spool \
	--with-jobdir=/var/spool/at \
	--with-etcdir=/etc/at
make 

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

make install IROOT=$RPM_BUILD_ROOT

install at.deny $RPM_BUILD_ROOT/etc/at/at.deny
touch   $RPM_BUILD_ROOT/etc/at/at.allow

mv $RPM_BUILD_ROOT/usr/doc/at $RPM_BUILD_ROOT/usr/doc/%{name}-%{version}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/atd

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
if test -r /var/run/atd.pid; then
	/etc/rc.d/init.d/atd stop >&2
	/etc/rc.d/init.d/atd start >&2
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
%attr(754,root,root) /etc/rc.d/init.d/atd
%attr(755,root,root) /usr/sbin/*

%attr(4755,root,root) /usr/bin/at

%attr(755,root,root) /usr/bin/atq
%attr(755,root,root) /usr/bin/atrm
%attr(755,root,root) /usr/bin/batch

%{_mandir}/man[158]/*

%attr(700,daemon,daemon) %dir /var/spool/at
%attr(700,daemon,daemon) %dir /var/spool/at/spool
%attr(600,daemon,daemon) %ghost /var/spool/at/.SEQ

%changelog
* Sun May  9 1999 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [3.1.8-7]
- now package is FHS 2.0 compliant,
- recompiled on new rpm.

* Thu Mar 25 1999 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [3.1.7-6]
- added at.patch adopted from latest Debian source which fix man pages,
  lex relayted bugs, displaing corectly dates in am/pm format and fiew
  others,
- modifications %post, %preun for standarizing this section; this allow stop
  service on uninstall and automatic restart on upgrade,
- changed permission (to more liberal).

* Sun Sep 13 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [3.1.7-5d]
- build against glibc-2.1,
- translation modified for pl,
- fixed files permissions,
- macro %%{name}-%%{version} in Source,
- macro %%{name}-%%{version} in Patch,
- removed conflicts: crontabs <= 1.5,
- added %ghost /var/spool/at/.SEQ,
- added %defattr and %doc, 
- minor modifications of spec file.

* Thu Sep  8 1998 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [3.1.7-5]
- added -q %setup parameter,
- changed Buildroot to /tmp/%%{name}-%%{version}-root,
- added using %%{name} and %%{version} in Source,
- added using $RPM_OPT_FLAGS during compile,
- atq(1), atrm(1), batch(1) man pages are now maked as nroff include to at(1)
  instead making sym link to at.1 (this allow compress man pages in future),
- added using %{SOURCE#} macro in %install,
- smarter instaling %doc,
- changed permission on some executables.
- added %attr and %defattr macros in %files (allow build package from
  non-root account),
- start at RH spec.
