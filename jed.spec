%define name	jed
%define version	0.99.19
%define sversion 0.99-19
%define release	%mkrel 5

Summary:	A fast, compact editor based on the slang screen library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPLv2+
Group:		Editors
Requires:	jed-common = %{version}
Requires:	slang-slsh
BuildRequires:	libx11-devel
BuildRequires:	libxft-devel
BuildRequires:	libxt-devel
BuildRequires:	gpm-devel
BuildRequires:	slang-devel
URL:		http://www.jedsoft.org/jed/
Source0:	ftp://space.mit.edu/pub/davis/jed/v0.99/jed-%{sversion}.tar.bz2
Patch0:		jed-0.99.19-fed-multilib-newauto.patch
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
%setup -q -n jed-%{sversion}
%ifarch x86_64
%patch0 -p1
%endif

cd autoconf
autoconf
mv configure ..
cd .. 

%build
sed -i 's|cd ..;pwd|pwd|g' configure
export JED_ROOT="%{_datadir}/jed"
%configure2_5x
%make clean
%make all
%make rgrep
%make xjed

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_infodir}
mkdir -p %{buildroot}%{_datadir}/jed
mkdir -p %{buildroot}%{_mandir}/man1

cp -r lib %{buildroot}%{_datadir}/jed
cp -r info/jed* %{buildroot}%{_infodir}

cd src/objs
install -m 0755 -s jed %{buildroot}%{_bindir}
install -m 0755 -s xjed %{buildroot}%{_bindir}
install -m 0755 -s rgrep %{buildroot}%{_bindir}

JED_ROOT=%{buildroot}%{_datadir}/jed %{buildroot}%{_bindir}/jed -batch -n -l preparse.sl
# wait till jed finishes
while ps -C jed > /dev/null; do sleep 1; done 

cd ../../doc/manual
install -m 644 jed.1 %{buildroot}%{_mandir}/man1
install -m 644 rgrep.1 %{buildroot}%{_mandir}/man1

%clean
rm -rf %{buildroot}

%post common
%_install_info %{name}.info

%postun common
%_remove_install_info %{name}.info

%files
%defattr(-,root,root)
%{_bindir}/jed

%files common
%defattr(-,root,root)
%doc COPYRIGHT INSTALL INSTALL.unx README changes.txt
%doc doc/txt/*
%{_infodir}/*
%{_mandir}/man1/jed*
%{_datadir}/jed

%files xjed
%defattr(-,root,root)
%{_bindir}/xjed

%files -n rgrep
%defattr(-,root,root)
%doc COPYRIGHT INSTALL INSTALL.unx README changes.txt
%{_bindir}/rgrep
%{_mandir}/man1/rgrep.1*

