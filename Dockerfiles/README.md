Dockerfiles
---

For shared Dockfiles, please check the detail usage in blog or in corresponding repos.

loam_ros: include lego-loam, SC-lego-loam, A-loam
```bash
docker build -t zhangkin/loam .

docker run -it --net=host -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$DISPLAY -v /dev/shm:/dev/shm -v /home/kin/bags:/workspace/data --name loam zhangkin/loam /bin/zsh
```