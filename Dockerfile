## 基于已经构建好的 base 构建，
## 事先使用 Dockerfile-base 构建 lidangqi/django-recruitment-base:0.8 镜像
## 或者从 docker.io pull 0.8 版本的 base镜像，这个镜像中有完整的 python/django 包
FROM lidangqi/django-recruitment-base:0.8
WORKDIR /data/recruitment
ENV server_params=
COPY . .
EXPOSE 8000
CMD ["/bin/sh", "/data/recruitment/start.production.sh"]