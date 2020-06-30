%define vendor_name Microsemi
%define vendor_label microsemi
%define driver_name smartpqi

%if %undefined module_dir
%define module_dir updates
%endif

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}
Version: 1.2.10_025
Release: 2
License: GPL

Source0: https://code.citrite.net/rest/archive/latest/projects/XS/repos/driver-microsemi-smartpqi/archive?at=1.2.10_025-2&format=tgz&prefix=driver-microsemi-smartpqi-1.2.10_025#/microsemi-smartpqi-1.2.10_025.tar.gz


Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XS/repos/driver-microsemi-smartpqi/archive?at=1.2.10_025-2&format=tgz&prefix=driver-microsemi-smartpqi-1.2.10_025#/microsemi-smartpqi-1.2.10_025.tar.gz) = 84282f5ac74b855cd7de516e248280205c2a71d8

BuildRequires: gcc
BuildRequires: kernel-devel
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod


%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}


%prep
%setup -n driver-%{name}-%{version}

%build
%{?cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd) KSRC=/lib/modules/%{kernel_version}/build modules EXTRA_CFLAGS+=-DRHEL8

%install
%{?cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build M=$(pwd) INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{kernel_version}/*/*.ko


%changelog
* Tue May 12 2020 Tom Goring <tom.goring@citrix.com> - 1.2.10_025-2
- CP-32938: Upgrade smartpqi driver to version 1.2.10-025-2
