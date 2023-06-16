
Summary: nginx set-misc dynamic modules
Name: nginx-module-set-misc
Version: ${NGINX_VERSION}+${NGX_SET_MISC_VERSION}
Release: ${NGINX_RELEASE}%{?dist}.ngx
Vendor: NGINX Packaging <nginx-packaging@f5.com>
URL: https://nginx.org/
Group: %{_group}

Source0: https://nginx.org/download/nginx-%{base_version}.tar.gz#/nginx-%{base_version}.tar.gz

Source100: https://github.com/openresty/set-misc-nginx-module/archive/v${NGX_SET_MISC_VERSION}.tar.gz#/set-misc-nginx-module-${NGX_SET_MISC_VERSION}.tar.gz
Source101: https://github.com/vision5/ngx_devel_kit/archive/v${NGX_NDK_VERSION}.tar.gz#/ngx_devel_kit-${NGX_NDK_VERSION}.tar.gz

License: 2-clause BSD-like license

BuildRoot: %{_tmppath}/%{name}-%{base_version}-%{base_release}-root
Requires: nginx-r%{base_version}
Provides: %{name}-r%{base_version}


%description
nginx development kit dynamic modules.

%if 0%{?suse_version}
%debug_package
%endif

%prep
%setup -qcTn %{name}-%{base_version}
tar --strip-components=1 -zxf %{SOURCE0}

ln -s . nginx%{?base_suffix}

mkdir set-misc
pushd set-misc
  tar xvzfo %{SOURCE100} --strip 1
popd

mkdir ndk
pushd ndk
  tar xvzfo %{SOURCE101} --strip 1
popd

%build
cd %{bdir}

./configure %{NGINX_CONFIG_ARGS} --add-dynamic-module=ndk --add-dynamic-module=set-misc \
	--with-debug
make %{?_smp_mflags} modules
for so in `find %{bdir}/objs/ -type f -name "*.so"`; do
  debugso=`echo $so | sed -e 's|\.so$|-debug.so|'`
  mv $so $debugso
done

./configure %{NGINX_CONFIG_ARGS} --add-dynamic-module=ndk --add-dynamic-module=set-misc
make %{?_smp_mflags} modules

$install
cd %{bdir}
%{__rm} -rf $RPM_BUILD_ROOT

%{__mkdir} -p $RPM_BUILD_ROOT%{_libdir}/nginx/modules

for so in `find %{bdir}/objs/ -maxdepth 1 -type f -name "ngx_http_set_misc_*.so"`; do
%{__install} -m755 $so \
   $RPM_BUILD_ROOT%{_libdir}/nginx/modules/
done

%clean
%{__rm} -rf %{_buildrootdir}

%files
%defattr(-,root,root)
%{_libdir}/nginx/modules/*
