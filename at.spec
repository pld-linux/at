Summary:     at job spooler
Summary(de): at-Job-Spooler
Summary(fr): Gestionnaire de taches at.
Summary(tr): Ýþ düzenleyici
Name:        at
Version:     3.1.7
Release:     6
Copyright:   GPL
Group:       Daemons
Source0:     ftp://tsx-11.mit.edu/pub/linux/sources/usr.bin/at-3.1.7.tar.gz
Source1:     atd.init
Patch0:      at-3.1.7-lockfile.patch
Patch1:      at-3.1.7-paths.patch
Patch2:      at-makefile.patch
Buildroot:   /tmp/%{name}-%{version}-root
Prereq:      fileutils chkconfig

%description
at and batch read commands from standard input or a specified file
which are to be executed at a later time, using /bin/sh.

%description -l de
Stapelverarbeitung von Lesebefehlen von einer Standard- oder einer 
genannten Datei zu einem späteren Zeitpunkt unter Verwendung von /bin/sh.

%description -l fr
at et batch lisent, sur l'entrée standard ou dans un fichier, des
commandes qui doivent être exécutées plus tard en utilisant /bin/sh.

%description -l tr
at ve batch /bin/sh kabuðunu kullanarak, belli bir saatte çalýþtýrmak üzere
standart giriþden ya da bir dosyadan komut okur.

%prep
%setup -q
%patch0 -p1 -b .lockfile
# The next path is a brute-force fix that will have to be updated
# when new versions of at are released.
%patch1 -p1 -b .paths
%patch2 -p1 -b .makefile

%build
CFLAGS=$RPM_OPT_FLAGS ./configure \
	--with-atspool=/var/spool/at/spool \
	--with-jobdir=/var/spool/at
make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

make install IROOT=$RPM_BUILD_ROOT

echo > $RPM_BUILD_ROOT/etc/at.deny
mv $RPM_BUILD_ROOT/usr/doc/at $RPM_BUILD_ROOT/usr/doc/%{name}-%{version}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/atd

rm -f $RPM_BUILD_ROOT/usr/man/man1/{atq,atrm,batch}.1
echo ".so at.1" > $RPM_BUILD_ROOT/usr/man/man1/atq.1
echo ".so at.1" > $RPM_BUILD_ROOT/usr/man/man1/atrm.1
echo ".so at.1" > $RPM_BUILD_ROOT/usr/man/man1/batch.1

%clean
rm -rf $RPM_BUILD_ROOT

%post
touch /var/spool/at/.SEQ
chmod 600 /var/spool/at/.SEQ
chown daemon.daemon /var/spool/at/.SEQ
/sbin/chkconfig --add atd

%preun
if [ "$1" = 0 ] ; then
  /sbin/chkconfig --del atd
fi

%files
%attr(644, root, root, 755) %doc /usr/doc/%{name}-%{version}
%attr(600, root, root) %config /etc/at.deny
%attr(500, root, root) %config /etc/rc.d/init.d/atd
%attr(500, root, root) /usr/sbin/*
%attr(4711, root, root) /usr/bin/at
%attr(   -, root, root) /usr/bin/atq
%attr(   -, root, root) /usr/bin/atrm
%attr(755, root, root) /usr/bin/batch
%attr(644, root,  man) /usr/man/man[18]/*
%attr(700, daemon, daemon) %dir /var/spool/at
%attr(700, daemon, daemon) %dir /var/spool/at/spool
%attr(600, daemon, daemon) %ghost /var/spool/at/.SEQ

%changelog
* Sat Nov 21 1998 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [3.1.7-6]
- removed "Conflicts: crontabs <= 1.5".

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
- added %attr and %defattr macros in %files (allows build package from
  non-root account).

* Tue May 05 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 22 1998 Michael K. Johnson <johnsonm@redhat.com>
- enhanced initscript

* Sun Nov 09 1997 Michael K. Johnson <johnsonm@redhat.com>
- learned to spell

* Wed Oct 22 1997 Michael K. Johnson <johnsonm@redhat.com>
- updated to at version 3.1.7
- updated lock and sequence file handling with %ghost
- Use chkconfig and atd, now conflicts with old crontabs packages

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc
