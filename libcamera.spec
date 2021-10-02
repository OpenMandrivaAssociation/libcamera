%define _disable_lto 1

%define gitdate 20210929

Name:    libcamera
Version: 0.0.0.%{gitdate}
Release: 0.git.0
Summary: A library to support complex camera ISPs
# Library is LGPLv2.1+ and the cam tool is GPLv2
License: LGPLv2+ and GPLv2
URL:     http://libcamera.org/

# Upstream is still under development so they are not tagging releases
# yet (https://git.linuxtv.org/libcamera.git). Use the following to do
# a rebase to a new snapshot:
#
# git clone --recursive https://git.linuxtv.org/libcamera.git
# then create archive %{name}-%{gitdate}.tar.xz

Source0: %{name}-%{gitdate}.tar.xz
Source1: qcam.desktop
Source2: qcam.metainfo.xml

BuildRequires: doxygen
BuildRequires: graphviz
#BuildRequires: pkgconfig(gtest)
BuildRequires: desktop-file-utils
BuildRequires: meson
BuildRequires: openssl
BuildRequires: ninja
BuildRequires: python3dist(jinja2)
BuildRequires: python3dist(ply)
BuildRequires: python3dist(pyyaml)
BuildRequires: python3dist(sphinx)
BuildRequires: boost-devel
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gnutls)
BuildRequires: %{_lib}atomic1
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(libevent)
BuildRequires: pkgconfig(libtiff-4)
BuildRequires: pkgconfig(lttng-ust)
BuildRequires: pkgconfig(libudev)
BuildRequires: pkgconfig(systemd)
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
%autosetup -p1 -n %{name}-%{gitdate}

%build
#export CC=gcc
#export CXX=g++
#export CFLAGS="%optflags -Wno-error"
#export CXXFLAGS="$CFLAGS"

# cam/qcam crash with LTO
#global _lto_cflags %{nil}
#export CFLAGS="%{optflags} -Wno-deprecated-declarations"
#export CXXFLAGS="%{optflags} -Wno-deprecated-declarations"

%meson  \
        -Dwerror=false \
        -Dlc-compliance=disabled \
        -Dtracing=disabled \
        -Dv4l2=true
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
