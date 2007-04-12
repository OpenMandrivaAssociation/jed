%define name	jed
%define version	0.99.18
%define sversion 0.99-18
%define release	%mkrel 1
%define slang_version 2.0.7
%define _requires_exceptions \\(ld-linux.*\\.so\\.2\\|ld.*\\.so\\.1\\)

Summary:	A fast, compact editor based on the slang screen library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Editors
Requires:	jed-common = %{version}
BuildRequires:	XFree86-devel
BuildRequires:  chrpath
BuildConflicts: slang-devel
URL:		http://www.jedsoft.org/jed/
Source0:	ftp://space.mit.edu/pub/davis/jed/v0.99/jed-%{sversion}.tar.bz2
Source1:	ftp://space.mit.edu/pub/davis/slang/slang-%{slang_version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
%description
Jed is a fast, compact editor based on the slang screen library.  Jed
features include emulation of the Emacs, EDT, WordStar and Brief editors;
support for extensive customization with slang macros, colors,
keybindings, etc.; and a variety of programming modes with syntax
highlighting.

You should install jed if you've used it before and you like it, or if you
haven't used any text editors before and you're still deciding what you'd
like to use.  You'll also need to have slang installed.

%package common
Summary:	Files needed by any Jed editor
Group:		Editors
%description common
The jed-common package contains files (such as .sl files) that are
needed by any jed binary in order to run.

%package xjed
Requires:	jed-common = %{version}
Summary:	The X Window System version of the Jed text editor
Group:		Editors

%description xjed
Xjed is a version of the Jed text editor that will work with the X Window
System.
  
You should install xjed if you like Jed and you'd like to use it with X.
You'll also need to have the X Window System installed.

%package -n rgrep
Summary:	A grep utility which can recursively descend through directories
Group:		Text tools

%description -n rgrep
The rgrep utility can recursively descend through directories as
it greps for the specified pattern.  Note that this ability does
take a toll on rgrep's performance, which is somewhat slow.  Rgrep
will also highlight the matching expression.

Install the rgrep package if you need a recursive grep which can
highlight the matching expression.

%prep
%setup -q -n jed-%{sversion} -a 1

%build
sed -i 's|cd ..;pwd|pwd|g' configure
pushd slang-%{slang_version}
%configure
%make
popd
export JED_ROOT="%{_datadir}/jed"
%configure --with-slanglib=`pwd`/slang-%{slang_version}/src/objs --with-slanginc=`pwd`/slang-%{slang_version}/src
%make clean
%make all
%make rgrep
%make xjed

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_infodir}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/jed
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT%{_prefix}/X11R6/bin

cp -r lib $RPM_BUILD_ROOT%{_datadir}/jed
cp -r info/jed* $RPM_BUILD_ROOT%{_infodir}

cd src/objs
install -m 0755 -s jed $RPM_BUILD_ROOT%{_bindir}
install -m 0755 -s xjed $RPM_BUILD_ROOT%{_prefix}/X11R6/bin
install -m 0755 -s rgrep $RPM_BUILD_ROOT%{_bindir}
JED_ROOT=$RPM_BUILD_ROOT%{_datadir}/jed $RPM_BUILD_ROOT%{_bindir}/jed -batch -n -l preparse.sl
chrpath -d $RPM_BUILD_ROOT%{_bindir}/*
chrpath -d $RPM_BUILD_ROOT%{_prefix}/X11R6/bin/xjed

cd ../../doc/manual
install -m 644 jed.1 $RPM_BUILD_ROOT%{_mandir}/man1
install -m 644 rgrep.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%post common
%_install_info %{name}.info

%postun common
%_remove_install_info %{name}.info

%files
%defattr(-,root,root)
%doc COPYING
%{_bindir}/jed

%files common
%defattr(-,root,root)
%doc COPYING COPYRIGHT INSTALL INSTALL.unx README changes.txt
%doc doc/txt/*
%{_infodir}/*
%{_mandir}/man1/jed*
%{_datadir}/jed

%files xjed
%defattr(-,root,root)
%doc COPYING
%{_prefix}/X11R6/bin/xjed

%files -n rgrep
%defattr(-,root,root)
%doc COPYING COPYRIGHT INSTALL INSTALL.unx README changes.txt
%{_bindir}/rgrep
%{_mandir}/man1/rgrep.1*

