# 概要
3rdParty モジュールも含めた　RHEL向けNginxのレポジトリです

詳細は[こちら](https://ueno-bst.github.io/nginx-mainline/)を参照

# Install

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

nginx パッケージ名が AppStream 内のパッケージと重複するため、除外しておくことを推奨します

```bash
## /etc/yum.repos.d/almalinux.repo
[appstream]
name=AlmaLinux $releasever - AppStream
mirrorlist=https://mirrors.almalinux.org/mirrorlist/$releasever/appstream
# baseurl=https://repo.almalinux.org/almalinux/$releasever/AppStream/$basearch/os/
enabled=1
gpgcheck=1
countme=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-AlmaLinux
exclude=nginx* # 追加
```

DNFコマンドを使用してパッケージをインストールして下さい

```bash
dnf install -y
      nginx \
      nginx-module-brotli \
      nginx-module-cache-purge \
      nginx-module-echo \
      nginx-module-geoip \
      nginx-module-geoip2 \
      nginx-module-headers-more \
      nginx-module-image-filter \
      nginx-module-ndk \
      nginx-module-njs \
      nginx-module-perl \
      nginx-module-lua \
      nginx-module-redis \
      nginx-module-redis2 \
      nginx-module-set-misc \
      nginx-module-srcache \
      nginx-module-vts \
      nginx-module-xslt
```
