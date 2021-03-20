docker build -f Dockerfile-base -t lidangqi/django-recruitment-base:0.8 .

 ## or just docker pull already built image from docker hub:
 # docker pull lidangqi/django-recruitment-base:0.8

## 构建包含 local.py 文件的 0.9 版本镜像（基于0.8镜像构建）：
docker build -f Dockerfile -t lidangqi/django-recruitment:0.9 .

docker tag lidangqi/django-recruitment:0.9 registry.cn-beijing.aliyuncs.com/lidangqi/django-recruitment:0.9
docker push registry.cn-beijing.aliyuncs.com/lidangqi/django-recruitment:0.9


## k8s 部署
## 部署前先替换 k8s/xxx-deployment.yaml 中的 {{BUILD_NUMBER}} 为版本号
## 然后运行 apply
## kubectl apply -f k8s
