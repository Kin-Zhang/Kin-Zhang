Dockerfiles
---

For shared Dockfiles, please check the detail usage in blog or in corresponding repos.

## SLAM
loam_ros: include lego-loam, SC-lego-loam, A-loam
```bash
docker build -t zhangkin/loam .

docker run -it --net=host -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$DISPLAY -v /dev/shm:/dev/shm -v /home/kin/bags:/workspace/data --name loam zhangkin/loam /bin/zsh
```


## Website

docusaurus: for build the docs webiste, check the official repo here: [https://github.com/facebook/docusaurus](https://github.com/facebook/docusaurus)

Run to start container with `-v` to your docusaurus folder, you can download the file codes here: [https://github.com/facebook/docusaurus/releases](https://github.com/facebook/docusaurus/releases)

```bash
docker run -it --net=host -v /home/kin/Documents/Wiki/docusaurus-2.3.1:/docusaurus --name wiki_docs zhangkin/docusaurus /bin/zsh
```

inside the container run the yarn install and start the server
```bash
yarn install & npm start
```