cd ${HOME}

sudo chown builder. -R ${HOME}/rpmbuild/RPMS
sudo chown builder. -R ${HOME}/rpmbuild/SRPMS

nginx -V 2> ${HOME}/nginx.verbose
grep -Eo "configure arguments:(.+)" ${HOME}/nginx.verbose | cut -b22- > nginx.config
export NGINX_CONFIG=$(cat ${HOME}/nginx.config)

arch=$(rpm --eval %{_arch})

# SOURCES ファイルの移動
for dir in `find ${HOME}/sources/ -type f`; do
  file=$(basename $dir)
  echo "Copy Source files: ${file}"
  cp $dir ${HOME}/rpmbuild/SOURCES/$file
done

# SPECファイルの環境変数を変換しつつ 移動
for dir in `find ${HOME}/specs/ -type f -name "*.spec"`; do
  if [ -f "$dir" ]; then
      file=$(basename $dir)
      echo "Convert SPEC files: ${file}"
      cat ${HOME}/specs/nginx.spec-in $dir | envsubst "$(export | sed -E "s/^.* ([A-Za-z_]+?)(=.*)?/\$\1/")" > ${HOME}/rpmbuild/SPECS/$file
  fi
done

## --
## 公式パッケージのソースをインストール
## --
# ソースダウンロード
yumdownloader --source nginx-${NGINX_VERSION}
yumdownloader --source nginx-module-xslt-${NGINX_VERSION}
yumdownloader --source nginx-module-njs-${NGINX_VERSION}+${NJS_VERSION}
yumdownloader --source nginx-module-perl-${NGINX_VERSION}
yumdownloader --source nginx-module-image-filter-${NGINX_VERSION}

# ソースをインストール
rpm -ivh ./*.src.rpm

# ソースを削除
rm -f *.src.rpm

for spec in `find ${HOME}/rpmbuild/SPECS/ -type f -name "*.spec"`; do
  # Source のインストール
  echo "spectool runnning in ${spec}"
  spectool -g -R $spec
  # 必要パッケージのインストール
  sudo yum-builddep -y $spec
  # パッケージのビルド
  rpmbuild -ba --clean $spec
done

if [ -f "${HOME}/rpmbuild/SRPMS/repodata/repomd.xml"]; then
  createrepo --update "${HOME}/rpmbuild/SRPMS"
else
  createrepo "${HOME}/rpmbuild/SRPMS"
fi

if [ -f "${HOME}/rpmbuild/RPMS/repodata/$(rpm --eval %{_arch})/repomd.xml"]; then
  createrepo --update "${HOME}/rpmbuild/RPMS/$(rpm --eval %{_arch})"
else
  createrepo "${HOME}/rpmbuild/RPMS/$(rpm --eval %{_arch})"
fi
