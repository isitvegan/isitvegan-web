#!/usr/bin/env bash

set -e

rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch

cat <<EOF | tee /etc/yum.repos.d/elasticsearch.repo
[elasticsearch-6.x]
name=Elasticsearch repository for 6.x packages
baseurl=https://artifacts.elastic.co/packages/6.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md
EOF

dnf install -y elasticsearch java-openjdk-devel java-openjdk

echo 'network.host: 0.0.0.0' >> /etc/elasticsearch/elasticsearch.yml

systemctl enable --now elasticsearch

firewall-cmd --zone=public --add-port=9200/tcp --permanent
firewall-cmd --reload