
Summary: nginx geoip dynamic modules
Name: nginx-module-geoip
Version: ${NGINX_VERSION}
Release: ${NGINX_RELEASE}%{?dist}.ngx
Vendor: NGINX Packaging <nginx-packaging@f5.com>
URL: https://nginx.org/
Group: %{_group}

BuildRequires: GeoIP-devel
Requires: GeoIP

Source0: https://nginx.org/download/nginx-%{base_version}.tar.gz#/nginx-%{base_version}.tar.gz

License: 2-clause BSD-like license

BuildRoot: %{_tmppath}/%{name}-%{base_version}-%{base_release}-root
Requires: nginx-r%{base_version}
Provides: %{name}-r%{base_version}


%description
nginx geoip dynamic modules.

%if 0%{?suse_version}
%debug_package
%endif

%prep
%setup -qcTn %{name}-%{base_version}
tar --strip-components=1 -zxf %{SOURCE0}

ln -s . nginx%{?base_suffix}

%build
cd %{bdir}

./configure %{BASE_CONFIGURE_ARGS} \
  --with-cc-opt="%{WITH_CC_OPT}" \
  --with-ld-opt="%{WITH_LD_OPT}" \
  --with-http_geoip_module=dynamic \
  --with-stream_geoip_module=dynamic \
	--with-debug
make %{?_smp_mflags} modules
for so in `find %{bdir}/objs/ -type f -name "*.so"`; do
  debugso=`echo $so | sed -e 's|\.so$|-debug.so|'`
  mv $so $debugso
done

./configure %{BASE_CONFIGURE_ARGS} \
  --with-cc-opt="%{WITH_CC_OPT}" \
  --with-ld-opt="%{WITH_LD_OPT}" \
  --with-http_geoip_module=dynamic \
  --with-stream_geoip_module=dynamic
make %{?_smp_mflags} modules

$install
cd %{bdir}
%{__rm} -rf $RPM_BUILD_ROOT

%{__mkdir} -p $RPM_BUILD_ROOT%{_libdir}/nginx/modules
for so in `find %{bdir}/objs/ -maxdepth 1 -type f -name "*.so"`; do
%{__install} -m755 $so \
   $RPM_BUILD_ROOT%{_libdir}/nginx/modules/
done

%clean
%{__rm} -rf %{_buildrootdir}

%files
%defattr(-,root,root)
%{_libdir}/nginx/modules/*
