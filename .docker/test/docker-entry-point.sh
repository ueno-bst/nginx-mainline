#!/usr/bin/env bash

yum install -y --disablerepo=appstream \
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
      nginx-module-redis \
      nginx-module-redis2 \
      nginx-module-set-misc \
      nginx-module-srcache \
      nginx-module-vts \
      nginx-module-xslt

nginx -g daemin off;
