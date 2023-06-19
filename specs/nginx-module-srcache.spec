
Summary: nginx srcache dynamic modules
Name: nginx-module-srcache
Version: ${NGINX_VERSION}+${NGX_SRCACHE_VERSION}
Release: ${NGINX_RELEASE}%{?dist}.ngx
Vendor: NGINX Packaging <nginx-packaging@f5.com>
URL: https://nginx.org/
Group: %{_group}

Source0: https://nginx.org/download/nginx-%{base_version}.tar.gz#/nginx-%{base_version}.tar.gz

Source100: https://github.com/openresty/srcache-nginx-module/archive/v${NGX_SRCACHE_VERSION}.tar.gz#/srcache-nginx-module-${NGX_SRCACHE_VERSION}.tar.gz

License: 2-clause BSD-like license

BuildRoot: %{_tmppath}/%{name}-%{base_version}-%{base_release}-root
Requires: nginx-r%{base_version}
Provides: %{name}-r%{base_version}


%description
nginx srcache dynamic modules.

%if 0%{?suse_version}
%debug_package
%endif

%prep
%setup -qcTn %{name}-%{base_version}
tar --strip-components=1 -zxf %{SOURCE0}

ln -s . nginx%{?base_suffix}

mkdir srcache
pushd srcache
tar xvzfo %{SOURCE100} --strip 1
popd

%build
cd %{bdir}

./configure %{BASE_CONFIGURE_ARGS} \
  --with-cc-opt="%{WITH_CC_OPT}" \
  --with-ld-opt="%{WITH_LD_OPT}" \
  --add-dynamic-module=srcache \
	--with-debug
make %{?_smp_mflags} modules
for so in `find %{bdir}/objs/ -type f -name "*.so"`; do
  debugso=`echo $so | sed -e 's|\.so$|-debug.so|'`
  mv $so $debugso
done

./configure %{BASE_CONFIGURE_ARGS} \
  --with-cc-opt="%{WITH_CC_OPT}" \
  --with-ld-opt="%{WITH_LD_OPT}" \
  --add-dynamic-module=srcache
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
