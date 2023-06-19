
Summary: nginx lua dynamic modules
Name: nginx-module-lua
Version: ${NGINX_VERSION}+${NGX_LUA_VERSION}
Release: ${NGINX_RELEASE}%{?dist}.ngx
Vendor: NGINX Packaging <nginx-packaging@f5.com>
URL: https://nginx.org/
Group: %{_group}

Source0: https://nginx.org/download/nginx-%{base_version}.tar.gz#/nginx-%{base_version}.tar.gz

Source100: https://github.com/vision5/ngx_devel_kit/archive/v${NGX_NDK_VERSION}.tar.gz#/ngx_devel_kit-${NGX_NDK_VERSION}.tar.gz
Source101: https://github.com/openresty/luajit2/archive/v${LUAJIT_BRANCH}.tar.gz#/luajit2-${LUAJIT_BRANCH}.tar.gz
Source102: https://github.com/openresty/lua-resty-core/archive/v${LUA_RESTRY_CORE_VERSION}.tar.gz#/lua-resty-core-${LUA_RESTRY_CORE_VERSION}.tar.gz
Source103: https://github.com/openresty/lua-resty-lrucache/archive/v${LUA_RESTRY_LRUCACHE_VERSION}.tar.gz#/lua-resty-lrucache-${LUA_RESTRY_LRUCACHE_VERSION}.tar.gz
Source104: https://github.com/openresty/lua-cjson/archive/${LUA_CJSON_VERSION}.tar.gz#/lua-cjson-${LUA_CJSON_VERSION}.tar.gz
Source105: https://github.com/openresty/lua-nginx-module/archive/v${NGX_LUA_VERSION}.tar.gz#/lua-nginx-module-${NGX_LUA_VERSION}.tar.gz
Source106: https://github.com/openresty/stream-lua-nginx-module/archive/v${NGX_STREAM_LUA_VERSION}.tar.gz#/stream-lua-nginx-module-${NGX_LUA_VERSION}.tar.gz

Patch10101: luajit2-2.1-00-makefile.patch
Patch10102: luajit2-2.1-01-luaconf.patch

Patch10501: lua-nginx-module.01.config.patch
Patch10502: lua-nginx-module.02.multiple-headers-changed-i.patch

Patch10601: stream-lua-nginx-module.01.config.patch

License: 2-clause BSD-like license

BuildRequires: pcre-devel

BuildRoot: %{_tmppath}/%{name}-%{base_version}-%{base_release}-root
Requires: nginx-r%{base_version}
Requires: nginx-module-ndk-r%{base_version}
Provides: %{name}-r%{base_version}

%description
nginx lua dynamic modules.

%if 0%{?suse_version}
%debug_package
%endif

%prep
%setup -qcTn %{name}-%{base_version}
tar --strip-components=1 -zxf %{SOURCE0}

ln -s . nginx%{?base_suffix}

mkdir ndk
pushd ndk
tar xvzfo %{SOURCE100} --strip 1
popd

mkdir luajit2
pushd luajit2
tar xvzfo %{SOURCE101} --strip 1
%patch10101 -p1
%patch10102 -p1
popd

mkdir lua-resty-core
pushd lua-resty-core
tar xvzfo %{SOURCE102} --strip 1
popd

mkdir lua-resty-lrucache
pushd lua-resty-lrucache
tar xvzfo %{SOURCE103} --strip 1
popd

mkdir lua-cjson
pushd lua-cjson
tar xvzfo %{SOURCE104} --strip 1
popd

mkdir lua
pushd lua
tar xvzfo %{SOURCE105} --strip 1
%patch10501 -p1
%patch10502 -p1
popd

mkdir stream-lua
pushd stream-lua
tar xvzfo %{SOURCE106} --strip 1
%patch10601 -p1
popd

%build
# build luajit
cd %{bdir}

export LUAJIT_INC="%{bdir}/luajit2-${LUAJIT_VERSION}/usr/include/ngx-luajit-${LUAJIT_VERSION}"
export LUAJIT_LIB="%{bdir}/luajit2-${LUAJIT_VERSION}/usr/lib"

cd %{bdir}/luajit2
DESTDIR="%{bdir}/luajit2-${LUAJIT_VERSION}" CFLAGS="-fPIC" make install

# build & install lua-cjson
cd %{bdir}/lua-cjson \
  && LUA_INCLUDE_DIR="${LUAJIT_INC}" LUA_CMODULE_DIR="/usr/lib/ngx-luajit-${LUAJIT_VERSION}" DESTDIR="%{bdir}/luajit2-${LUAJIT_VERSION}" make install

# build nginx
cd %{bdir}

./configure %{BASE_CONFIGURE_ARGS} \
  --with-cc-opt="%{WITH_CC_OPT}" \
  --with-ld-opt="%{WITH_LD_OPT}" \
  --add-dynamic-module=ndk \
  --add-dynamic-module=lua \
  --add-dynamic-module=stream-lua \
	--with-debug
make %{?_smp_mflags} modules
for so in `find %{bdir}/objs/ -type f -name "*.so"`; do
  debugso=`echo $so | sed -e 's|\.so$|-debug.so|'`
  mv $so $debugso
done

./configure %{BASE_CONFIGURE_ARGS} \
  --with-cc-opt="%{WITH_CC_OPT}" \
  --with-ld-opt="-lpcre %{WITH_LD_OPT}" \
  --add-dynamic-module=ndk \
  --add-dynamic-module=lua \
  --add-dynamic-module=stream-lua
make %{?_smp_mflags} modules

$install
cd %{bdir}
%{__rm} -rf $RPM_BUILD_ROOT

%{__mkdir} -p $RPM_BUILD_ROOT%{_libdir}/nginx/modules

%{__rm} -f %{bdir}/objs/ndk*.so

for so in `find %{bdir}/objs/ -maxdepth 1 -type f -name "*.so"`; do
%{__install} -m755 $so \
   $RPM_BUILD_ROOT%{_libdir}/nginx/modules/
done

# Install luajit
%{__mkdir} -p $RPM_BUILD_ROOT%{_bindir}
%{__install} -m 755 %{bdir}/luajit2-${LUAJIT_VERSION}/usr/bin/ngx-luajit-${LUAJIT_VERSION} $RPM_BUILD_ROOT%{_bindir}/
%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/ngx-luajit-${LUAJIT_VERSION}/jit
for f in `find %{bdir}/luajit2-${LUAJIT_VERSION}/usr/share/ngx-luajit-${LUAJIT_VERSION}/jit/ -type f`; do
    %{__install} -m644 ${f} $RPM_BUILD_ROOT%{_datadir}/ngx-luajit-${LUAJIT_VERSION}/jit/
done

%{__mkdir} -p $RPM_BUILD_ROOT%{_includedir}/ngx-luajit-${LUAJIT_VERSION}
for f in `find %{bdir}/luajit2-${LUAJIT_VERSION}/usr/include/ngx-luajit-${LUAJIT_VERSION}/ -type f`; do
    %{__install} -m644 ${f} $RPM_BUILD_ROOT%{_includedir}/ngx-luajit-${LUAJIT_VERSION}/
done

%{__mkdir} -p $RPM_BUILD_ROOT/usr/lib/ngx-luajit-${LUAJIT_VERSION}
for f in `find %{bdir}/luajit2-${LUAJIT_VERSION}/usr/lib/ngx-luajit-${LUAJIT_VERSION}/ -type f`; do
    %{__install} -m644 ${f} $RPM_BUILD_ROOT/usr/lib/ngx-luajit-${LUAJIT_VERSION}/
done

# Install lua-resty / lua-resty-lrucache
%{__mkdir} -p $RPM_BUILD_ROOT%{_includedir}/ngx-luajit-${LUAJIT_VERSION}/resty
cd %{bdir}/lua-resty-core \
    && LUA_LIB_DIR=$RPM_BUILD_ROOT%{_datadir}/ngx-luajit-${LUAJIT_VERSION} make install
cd %{bdir}/lua-resty-lrucache \
    && LUA_LIB_DIR=$RPM_BUILD_ROOT%{_datadir}/ngx-luajit-${LUAJIT_VERSION} make install

%clean
%{__rm} -rf %{_buildrootdir}

%files
%defattr(-,root,root)
%{_libdir}/nginx/modules/*


%{_bindir}/ngx-luajit-${LUAJIT_VERSION}
%dir %{_datadir}/ngx-luajit-${LUAJIT_VERSION}/jit
%{_datadir}/ngx-luajit-${LUAJIT_VERSION}/jit/*
%dir %{_datadir}/ngx-luajit-${LUAJIT_VERSION}/ngx
%{_datadir}/ngx-luajit-${LUAJIT_VERSION}/ngx/*
%dir %{_datadir}/ngx-luajit-${LUAJIT_VERSION}/resty
%{_datadir}/ngx-luajit-${LUAJIT_VERSION}/resty/*
%dir %{_includedir}/ngx-luajit-${LUAJIT_VERSION}
%{_includedir}/ngx-luajit-${LUAJIT_VERSION}/*
%dir /usr/lib/ngx-luajit-${LUAJIT_VERSION}
/usr/lib/ngx-luajit-${LUAJIT_VERSION}/*
