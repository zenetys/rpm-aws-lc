# Supported targets: el8, el9, el10

%define _prefix /opt/%{name}
%define _docdir_fmt aws-lc

%{!?make_verbose: %define make_verbose 0}

%if 0%{?rhel} <= 8
%undefine __cmake_in_source_build
%endif

%if 0%{?rhel} >= 10
%undefine _auto_set_build_flags
%endif

%global source_date_epoch_from_changelog 0

Name: aws-lc-0z
Version: 1.61.1
Release: 1%{?dist}.zenetys
Summary: AWS-LC cryptographic library
License: Apache-2.0 OR ISC OR BSD-3-Clause OR MIT OR CC0-1.0 OR OpenSSL OR SSLeay-standalone
URL: https://github.com/aws/aws-lc

Source0: https://github.com/aws/aws-lc/archive/refs/tags/v%{version}.tar.gz#/aws-lc-%{version}.tar.gz

BuildRequires: cmake >= 3.0
BuildRequires: gcc
BuildRequires: gcc-c++

%description
AWS-LC is a general-purpose cryptographic library maintained by the
AWS Cryptography team for AWS and their customers. It іs based on code
from the Google BoringSSL project and the OpenSSL project.

%prep
%setup -n aws-lc-%{version}

%build
cmake \
    -S . \
    -B %{__cmake_builddir} \
    %if %{make_verbose}
    -DCMAKE_VERBOSE_MAKEFILE=ON \
    %endif
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DBUILD_SHARED_LIBS=1 \
    -DDISABLE_GO=1 \
    -DDISABLE_PERL=1 \
    -DBUILD_TESTING=0 \
    -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
    -DCMAKE_SHARED_LINKER_FLAGS='-Wl,-rpath,$ORIGIN' \
    -DCMAKE_EXE_LINKER_FLAGS='-Wl,-rpath,$ORIGIN/../%{_lib}'

# use --define 'make_verbose 1' to enable verbose
cmake --build %{__cmake_builddir} %{?_smp_mflags}

%install
%cmake_install
rm -rf %{buildroot}%{_prefix}/%{_lib}/crypto/cmake
rm -rf %{buildroot}%{_prefix}/%{_lib}/ssl/cmake

mkdir -p %{buildroot}%{_rpmmacrodir}
echo '%%%(echo %{name} |tr '-' '_')_prefix %{_prefix}' \
    > %{buildroot}%{_rpmmacrodir}/macros.%{name}

%files
%doc README.md
%doc NOTICE
%license LICENSE

%{_bindir}/bssl
%{_bindir}/c_rehash
%{_bindir}/openssl

%{_libdir}/libcrypto.so
%{_libdir}/libssl.so

%package devel
Summary: AWS-LC development files from package %{name}
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
AWS-LC development files from package %{name}.

%files devel
%{_includedir}/openssl
%{_libdir}/pkgconfig/libcrypto.pc
%{_libdir}/pkgconfig/libssl.pc
%{_libdir}/pkgconfig/openssl.pc
%{_rpmmacrodir}/macros.%{name}
