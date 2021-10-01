Name:    libcamera
	
Version: 0.0.0~git.%{commitdate}.%{shortcommit}
	
Release: 1%{?dist}
	
Summary: A library to support complex camera ISPs
	
# Library is LGPLv2.1+ and the cam tool is GPLv2
	
License: LGPLv2+ and GPLv2
	
URL:     http://libcamera.org/
	
 
	
# Upstream is still under development so they are not tagging releases
	
# yet (https://git.linuxtv.org/libcamera.git). Use the following to do
	
# a rebase to a new snapshot:
	
#
	
# git archive --format=tar --prefix=%%{name}-%%{shortcommit}/ %%{shortcommit} | xz > %%{name}-%%{shortcommit}.tar.xz
	
Source0: %{name}-%{shortcommit}.tar.xz
	
Source1: qcam.desktop
	
Source2: qcam.metainfo.xml
	
 
	
BuildRequires: doxygen
	
BuildRequires: gcc-c++
	
BuildRequires: gtest-devel
	
BuildRequires: desktop-file-utils
	
BuildRequires: meson
	
BuildRequires: openssl
	
BuildRequires: ninja-build
	
BuildRequires: python3-jinja2
	
BuildRequires: python3-ply
	
BuildRequires: python3-pyyaml
	
BuildRequires: python3-sphinx
	
BuildRequires: boost-devel
	
BuildRequires: pkgconfig(glib-2.0)
	
BuildRequires: gnutls-devel
	
BuildRequires: libatomic
	
BuildRequires: libevent-devel
	
BuildRequires: libtiff-devel
	
BuildRequires: lttng-ust-devel
	
BuildRequires: systemd-devel
	
BuildRequires: pkgconfig(Qt5Core)
	
BuildRequires: pkgconfig(Qt5Gui)
	
BuildRequires: pkgconfig(Qt5Widgets)
	
BuildRequires: pkgconfig(gstreamer-video-1.0)
	
BuildRequires: pkgconfig(gstreamer-allocators-1.0)
	
 
	
%description
	
libcamera is a library that deals with heavy hardware image processing
	
operations of complex camera devices that are shared between the linux
	
host all while allowing offload of certain aspects to the control of
	
complex camera hardware such as ISPs.
	
 
	
Hardware support includes USB UVC cameras, libv4l cameras as well as more
	
complex ISPs (Image Signal Processor).
	
 
	
%package     devel
	
Summary:     Development package for %{name}
	
Requires:    %{name}%{?_isa} = %{version}-%{release}
	
 
	
%description devel
	
Files for development with %{name}.
	
 
	
%package     doc
	
Summary:     Documentation for %{name}
	
BuildArch:   noarch
	
 
	
%description doc
	
HTML based documentation for %{name} including getting started and API.
	
 
	
%package     ipa
	
Summary:     ISP Image Processing Algorithm Plugins for %{name}
	
Requires:    %{name}%{?_isa} = %{version}-%{release}
	
 
	
%description ipa
	
Image Processing Algorithms plugins for interfacing with device
	
ISPs for %{name}
	
 
	
%package     tools
	
Summary:     Tools for %{name}
	
Requires:    %{name}%{?_isa} = %{version}-%{release}
	
 
	
%description tools
	
Command line tools for %{name}
	
 
	
%package     qcam
	
Summary:     Graphical QCam application for %{name}
	
Requires:    %{name}%{?_isa} = %{version}-%{release}
	
 
	
%description qcam
	
Graphical QCam application for %{name}
	
 
	
%package     gstreamer
	
Summary:     GSTreamer plugin for %{name}
	
Requires:    %{name}%{?_isa} = %{version}-%{release}
	
 
	
%description gstreamer
	
GSTreamer plugins for %{name}
	
 
	
%prep
	
%autosetup -p1 -n %{name}-%{shortcommit}
	
 
	
%build
	
# cam/qcam crash with LTO
	
%global _lto_cflags %{nil}
	
export CFLAGS="%{optflags} -Wno-deprecated-declarations"
	
export CXXFLAGS="%{optflags} -Wno-deprecated-declarations"
	
 
	
%ifarch ppc64le
	
# 64-bit POWER LE does not use the IEEE long double ABI but
	
# instead a custom one by default. This leads to libcamera
	
# failing to build, use IEEE long double ABI to prevent it.
	
#
	
# https://bugzilla.redhat.com/show_bug.cgi?id=1538817
	
export CFLAGS="${CFLAGS} -mabi=ieeelongdouble"
	
export CXXFLAGS="${CXXFLAGS} -mabi=ieeelongdouble"
	
%endif
	
 
	
%meson
	
%meson_build
	
	
%install
	
%meson_install
	
	
# Install Desktop Entry file
	
desktop-file-install --dir=%{buildroot}%{_datadir}/applications \
	
                     %SOURCE1
	
	
# Install AppStream metainfo file
	
mkdir -p %{buildroot}/%{_metainfodir}/
	
cp -a %SOURCE2 %{buildroot}/%{_metainfodir}/
	
 
	
# Remove the Sphinx build leftovers
	
rm -rf ${RPM_BUILD_ROOT}/%{_docdir}/%{name}-*/html/.buildinfo
	
rm -rf ${RPM_BUILD_ROOT}/%{_docdir}/%{name}-*/html/.doctrees
	
 
	
%files
	
%license COPYING.rst LICENSES/LGPL-2.1-or-later.txt
	
%{_libdir}/libcamera*.so.*
	
 
	
%files devel
	
%{_includedir}/%{name}/
	
%{_libdir}/libcamera*.so
	
%{_libdir}/pkgconfig/libcamera-base.pc
	
%{_libdir}/pkgconfig/libcamera.pc
	
 
	
%files doc
	
%doc %{_docdir}/%{name}-*/
	
 
	
%files ipa
	
%{_datadir}/libcamera/
	
%{_libdir}/libcamera/
	
%{_libexecdir}/libcamera/
	
 
	
%files gstreamer
	
%{_libdir}/gstreamer-1.0/libgstlibcamera.so
	
 
	
%files qcam
	
%{_bindir}/qcam
	
%{_datadir}/applications/qcam.desktop
	
%{_metainfodir}/qcam.metainfo.xml
	
 
	
%files tools
	
%license LICENSES/GPL-2.0-only.txt
	
%{_bindir}/cam
	
%{_bindir}/lc-compliance
