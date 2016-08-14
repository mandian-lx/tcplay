%define major 2.0
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Summary:  A free pretty much fully featured and stable TrueCrypt implementation
Name:     tcplay
Version:  2.0
Release:  1
License:  BSD and Public Domain
Group:    File tools
URL:      https://github.com/bwalex/tc-play
Source0:  https://github.com/bwalex/tc-play/archive/v%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  pkgconfig(devmapper)
BuildRequires:  pkgconfig(uuid)
BuildRequires:  pkgconfig(libgcrypt)
BuildRequires:  pkgconfig(openssl)

%description
# from the README.md
tcplay is a free (BSD-licensed), pretty much fully featured (including multiple
keyfiles, cipher cascades, etc) and stable TrueCrypt implementation.

This implementation supports mapping (opening) both system and normal TrueCrypt
volumes, as well as opening hidden volumes and opening an outer volume while
protecting a hidden volume. There is also support to create volumes, including
hidden volumes, etc. Since version 1.1, there is also support for restoring
from the backup header (if present), change passphrase, keyfile and PBKDF2
PRF function.

Since tcplay uses dm-crypt (or dm_target_crypt on DragonFly) it makes full use
of any available hardware encryption/decryption support once the volume has
been mapped.

It is based solely on the documentation available on the TrueCrypt website,
many hours of trial and error and the output of the Linux' TrueCrypt client.
As it turns out, most technical documents on TrueCrypt contain mistakes, hence
the trial and error approach.

%files
%{_bindir}/%{name}
%{_mandir}/man8/%{name}.8*
%doc README.md
%doc CHANGELOG
%doc LICENSE

#--------------------------------------------------------------------

%package -n %{libname}
Summary:   Primary library for %{name}
Group:     System/Libraries

%description -n %{libname}
Primary library for %{name}.

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*
%doc LICENSE

#--------------------------------------------------------------------

%package -n %{devname}
Summary:   Header files and static libraries for %{name}
Group:     Development/C
Requires:  %{libname} = %{version}-%{release}
Provides:  lib%{name}-devel = %{version}-%{release}
Provides:  %{name}-devel = %{version}-%{release}

%description -n %{devname}
Libraries and includes files for developing programs based on %{name}.

%files -n %{devname}
%{_includedir}/tcplay_api.h
%{_libdir}/lib%{name}*.so
%{_libdir}/pkgconfig/*.pc
%doc CHANGELOG
%doc LICENSE

#--------------------------------------------------------------------

%prep
%setup -q -n tc-play-%{version}

%build
%cmake
%make

%install
# NOTE: there is no rule to make target 'install' in Makefile

# binary
%__install -dm 0755 %{buildroot}%{_bindir}/
%__install -pm 0755 build/%{name} %{buildroot}%{_bindir}/

# libs
%__install -dm 0755 %{buildroot}%{_libdir}/
%__install -pm 0755 build/lib%{name}.so.%{major} %{buildroot}%{_libdir}/
%__ln -s libtcplay.so.%{major} %{buildroot}%{_libdir}/lib%{name}.so

# header
%__install -dm 0755 %{buildroot}%{_includedir}/
%__install -pm 0644 tcplay_api.h %{buildroot}%{_includedir}/

# pkgconfig
%__install -dm 0755 %{buildroot}%{_libdir}/pkgconfig/
%__install -pm 0644 build/tcplay.pc %{buildroot}%{_libdir}/pkgconfig/

# manpage
%__install -dm 0755 %{buildroot}%{_mandir}/man8/
%__install -pm 0644 %{name}.8 %{buildroot}%{_mandir}/man8/

