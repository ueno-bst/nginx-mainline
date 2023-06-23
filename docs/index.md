---
layout: default
title: 概要
---

# 概要

NGINXの各種モジュールを RHEL上で使用可能にしたパッケージのレポジトリを提供します。

# インストール方法

次の内容を `/etc/yum.repos.d/nginx-mainline.repo` に記載してください

```text
[nginx-mainline-module]
name=nginx mainline repo
baseurl=https://ueno-bst.github.io/nginx-mainline/$releasever/$basearch/
gpgcheck=0
enabled=1

[nginx-mainline-module-source]
name=nginx mainline repo - Source
baseurl=https://ueno-bst.github.io/nginx-mainline/$releasever/SRPMS/
gpgcheck=0
enabled=0
```

curl を使用して [REPOファイル](nginx-mainline-module.repo) を ダウンロードすることも可能です

```bash
curl -o /etc/yum.repos.d/nginx-mainline-module.repo -LO https://ueno-bst.github.io/nginx-mainline/nginx-mainline-module.repo
```

# レポジトリに含まれるパッケージ一覧

## 公式パッケージ + モジュール

パッケージの内容は[Nginx公式が配布するRHEL用パッケージ](http://nginx.org/packages/centos/)と同一です

| Name              | Package                   |
|-------------------|---------------------------|
| NGINX             | nginx                     |
| GeoIP             | nginx-module-geoip        |
| HTTP Image Filter | nginx-module-image-filter |
| Javascript        | nginx-module-njs          |
| Perl              | nginx-module-perl         |
| XSLT              | nginx-module-xslt         |

[^1]:このパッケージは RHEL8 以降は公式パッケージに含まれません

## サードパーティモジュール

| Name                                                                       | Package                   | Repository                                                                                    |
|----------------------------------------------------------------------------|---------------------------|-----------------------------------------------------------------------------------------------|
| Brotli                                                                     | nginx-module-brotli       | [google/ngx_brotli](https://github.com/google/ngx_brotli)                                     |
| Cache Purge                                                                | nginx-module-cache-purge  | [nginx-modules/ngx_cache_purge](https://github.com/nginx-modules/ngx_cache_purge)             |
| Development Kit (NDK)                                                      | nginx-module-ndk          | [vision5/ngx_devel_kit](https://github.com/vision5/ngx_devel_kit)                             |
| GeoIP2                                                                     | nginx-module-geoip2       | [leev/ngx_http_geoip2_module](https://github.com/leev/ngx_http_geoip2_module)                 |
| [Headers More](https://www.nginx.com/resources/wiki/modules/headers_more/) | nginx-module-headers-more | [openresty/headers-more-nginx-module](https://github.com/openresty/headers-more-nginx-module) |
| [HTTP Echo](https://www.nginx.com/resources/wiki/modules/echo/)            | nginx-module-echo         | [openresty/echo-nginx-module](https://github.com/openresty/echo-nginx-module)                 | 
| [Lua](https://www.nginx.com/resources/wiki/modules/lua/)                   | nginx-module-lua          | [openresty/lua-nginx-module](https://github.com/openresty/lua-nginx-module)                   | 
| [HTTP Redis](https://www.nginx.com/resources/wiki/modules/redis/)          | nginx-module-redis        | [onnimonni/redis-nginx-module](https://github.com/onnimonni/redis-nginx-module)               | 
| [HTTP Redis2](https://www.nginx.com/resources/wiki/modules/redis2/)        | nginx-module-redis2       | [openresty/redis2-nginx-module](https://github.com/openresty/redis2-nginx-module)             | 
| [HTTP Set Misc](https://www.nginx.com/resources/wiki/modules/set_misc/)    | nginx-module-set-misc     | [openresty/set-misc-nginx-module](https://github.com/openresty/set-misc-nginx-module)         | 
| [HTTP SRCache](https://www.nginx.com/resources/wiki/modules/sr_cache/)     | nginx-module-srcache      | [openresty/srcache-nginx-module](https://github.com/openresty/srcache-nginx-module)           | 
| VTS                                                                        | nginx-module-vts          | [vozlt/nginx-module-vts](https://github.com/vozlt/nginx-module-vts)                           |  

## パッケージ備考

- GeoIP
  - RHEL8以降では、公式配布パッケージに含まれなくなりました。
- Cache Purge
  - ワイルドカード(*) によるキャッシュの一括削除を使用できるバージョンです。
  - 一括削除はディスクの負荷が大きいため、推奨できません。
- HTTP Lua
  - パッケージには次のライブラリが含まれます。
  - [lua-resty-redis](https://github.com/openresty/lua-resty-redis)
  - [lua-cjson](https://github.com/openresty/lua-cjson)


