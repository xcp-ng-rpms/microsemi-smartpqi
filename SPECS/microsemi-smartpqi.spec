%global package_speccommit a47856d7a324308d272308edc54bc8f8bc46d251
%global usver 2.1.18_045
%global xsver 1
%global xsrel %{xsver}%{?xscount}%{?xshash}
%global package_srccommit 2.1.18_045

%define vendor_name Microsemi
%define vendor_label microsemi
%define driver_name smartpqi

%if %undefined module_dir
%define module_dir updates
%endif

## Keeps rpmlint happy
%{!?kernel_version: %global kernel_version dummy}


Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}
Version: 2.1.18_045
Release: %{?xsrel}%{?dist}
License: GPL
Source0: microsemi-smartpqi-2.1.18_045.tar.gz

BuildRequires: gcc
BuildRequires: kernel-devel
%{?_cov_buildrequires}
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod


%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}


%prep
%setup -n %{name}-%{version}
%{?_cov_prepare}

%build
%{?_cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd) KSRC=/lib/modules/%{kernel_version}/build modules EXTRA_CFLAGS+=-DKCLASS4C

%install
%{?_cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build M=$(pwd) INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%{?_cov_install}

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

%{?_cov_results_package}


%changelog
* Sun Sep 11 2022 Zhuangxuan Fei <zhuangxuan.fei@citrix.com> - 2.1.18_045-1
- CP-40167: Upgrade smartpqi driver to version 2.1.18_045

* Mon Feb 14 2022 Ross Lagerwall <ross.lagerwall@citrix.com> - 1.2.10_025-4
- CP-38416: Enable static analysis

* Wed Dec 02 2020 Tim Smith <tim.smith@citrix.com> - 1.2.10_025-3
- CP-35517 Fix build and silence RPM warning

* Tue May 12 2020 Tom Goring <tom.goring@citrix.com> - 1.2.10_025-2
- CP-32938: Upgrade smartpqi driver to version 1.2.10-025-2
