%define _disable_ld_no_undefined 1

%define major 0.6
%define oname camera

%define	libname	%mklibname %{oname}
%define	docname %mklibname %{oname}-doc
%define	ipaname	%mklibname %{oname}-ipa
%define	gstname	%mklibname %{oname}-gstreamer
%define	v4l2name %mklibname %{oname}-v4l2
%define	devname	%mklibname %{oname} -d

#define gitdate 20230110

Name:    libcamera
Version: 0.6.0
Release: 1
Summary: A library to support complex camera ISPs
# Library is LGPLv2.1+ and the cam tool is GPLv2
License: LGPLv2+ and GPLv2
URL:     https://libcamera.org/

# Upstream is still under development but they start tagging releases
# (https://git.linuxtv.org/libcamera.git). Use the following to do
# a rebase to a new tag:
#
# git clone --branch v0.5.0 https://git.linuxtv.org/libcamera.git

# then create archive %{name}-%{gitdate}.tar.xz

Source0: %{name}-%{version}.tar.xz
Source1: qcam.desktop
Source2: qcam.metainfo.xml

BuildRequires: doxygen
BuildRequires: graphviz
BuildRequires: pkgconfig(gtest)
BuildRequires: desktop-file-utils
BuildRequires: meson
BuildRequires: openssl
BuildRequires: ninja
BuildRequires: pkgconfig(python)
BuildRequires: python3dist(jinja2)
BuildRequires: python3dist(ply)
BuildRequires: python3dist(pyyaml)
BuildRequires: python3dist(sphinx)
BuildRequires: pkgconfig(pybind11)
BuildRequires: boost-devel
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gnutls)
BuildRequires: %{_lib}atomic1
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(libevent)
BuildRequires: pkgconfig(libtiff-4)
BuildRequires: pkgconfig(lttng-ust)
BuildRequires: pkgconfig(libudev)
BuildRequires: pkgconfig(sdl2)
BuildRequires: pkgconfig(systemd)
BuildRequires: pkgconfig(yaml-0.1)
BuildRequires: pkgconfig(Qt6Core)
BuildRequires: pkgconfig(Qt6Gui)
BuildRequires: pkgconfig(Qt6OpenGL)
BuildRequires: pkgconfig(Qt6OpenGLWidgets)
BuildRequires: pkgconfig(Qt6Widgets)
BuildRequires: pkgconfig(gstreamer-video-1.0)
BuildRequires: pkgconfig(gstreamer-allocators-1.0)

%description
libcamera is a library that deals with heavy hardware image processing
operations of complex camera devices that are shared between the linux
host all while allowing offload of certain aspects to the control of
complex camera hardware such as ISPs.

Hardware support includes USB UVC cameras, libv4l cameras as well as more
complex ISPs (Image Signal Processor).

%package -n %{libname}
Summary:	Library for %{name}
Group:		System/Libraries

%description -n %{libname}
Dynamic libraries from %{name}.

%package -n %{devname}
Summary:     Development package for %{name}
Requires:    %{libname} = %{EVRD}

%description -n %{devname}
Files for development with %{name}.

#package -n %{docname}
#Summary:     Documentation for %{name}
#BuildArch:   noarch

#description -n %{docname}
#HTML based documentation for %{name} including getting started and API.

%package -n %{ipaname}
Summary:     ISP Image Processing Algorithm Plugins for %{name}
Requires:    %{libname} = %{EVRD}

%description -n %{ipaname}
Image Processing Algorithms plugins for interfacing with device
ISPs for %{name}

%package     tools
Summary:     Tools for %{name}
Requires:    %{libname} = %{EVRD}

%description tools
Command line tools for %{name}

%package     qcam
Summary:     Graphical QCam application for %{name}
Requires:    %{libname} = %{EVRD}

%description qcam
Graphical QCam application for %{name}

%package -n %{gstname}
Summary:     GSTreamer plugin for %{name}
Requires:    %{libname} = %{EVRD}

%description -n %{gstname}
GSTreamer plugins for %{name}

%package -n %{v4l2name}
Summary:     V4L2 compatibility layer
Requires:    %{libname} = %{EVRD}
Requires:    %{name}-tools = %{version}-%{release}

%description -n %{v4l2name}
V4L2 compatibility layer

%package -n python-%{name}
Summary:     Python bindings for %{name}
Requires:    %{libname} = %{EVRD}

%description -n python-%{name}
Python bindings for %{name}


%prep
%autosetup -p1 -n %{name}-%{version}

%build
%meson  \
        -Dwerror=false \
        -Dv4l2=true \
        -Dpipelines=ipu3,rkisp1,simple,uvcvideo,vimc \
        -Dlc-compliance=disabled \
        -Ddocumentation=disabled \
        -Dtracing=disabled
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

%files -n %{libname}
%license COPYING.rst LICENSES/LGPL-2.1-or-later.txt
%{_libdir}/libcamera*.so.%{major}*

%files -n %{devname}
%{_includedir}/%{name}/
%{_libdir}/libcamera*.so
%{_libdir}/pkgconfig/libcamera-base.pc
%{_libdir}/pkgconfig/libcamera.pc

#files -n %{docname}
#doc %{_docdir}/%{name}-*/

%files -n %{ipaname}
%{_datadir}/libcamera/
%{_libdir}/libcamera/
%{_libexecdir}/libcamera/
%exclude %{_libexecdir}/libcamera/v4l2-compat.so

%files -n %{gstname}
%{_libdir}/gstreamer-1.0/libgstlibcamera.so

%files -n %{v4l2name}
%{_libexecdir}/libcamera/v4l2-compat.so

%files qcam
%{_bindir}/qcam
%{_datadir}/applications/qcam.desktop
%{_metainfodir}/qcam.metainfo.xml

%files tools
%license LICENSES/GPL-2.0-only.txt
%{_bindir}/cam
%{_bindir}/libcamerify

%files -n python-%{name}
%{python_sitearch}/* 
