# Knowledge base 知识库

This repo is created to share/back up some knowledge/interesting stuff for having fun.  
本仓库作为个人的编程游乐场，存放个人的知识积累和新鲜尝试。
## Development environment 开发环境
To eusure an independent and reproducible developemnt environment, mainly I will use **Docker container** plus some other useful tools, which are easy and conventient to use and maintain.

开发环境的关键要素为**独立性**和**易重现性**，为此，我将使用以**Docker container**为主的一系列实用工具，以保证其在使用和维护上的便利性。

### Python
[Jupyter notebook](https://jupyter.org/) is an amazing and also common tool for python to do experiments and save the results.  
For python, I use *docker container* + *jupyer-lab* as the playground, which provides a wide potentialities to do anything you want.  
Also, I promote using lastest stuff(That's why people put their effort for them, isn't it?). So now the versions are:
- [Python 3.9](https://docs.python.org/3/whatsnew/3.9.html)
- [Jupyter-lab 3.0](https://jupyterlab.readthedocs.io/en/stable/getting_started/overview.html)  

对于Python而言，[Jupyter notebook](https://jupyter.org/)是一款出色的工具来用于实验和结果的保存展示。  
基于此，我使用*docker container* + *jupyer-lab*作为主要的实验田，作为开发者可以在上面任意发挥，实现无穷的可能。  
同时，我也推动和鼓励大家使用最新版本的软件/工具（不少人在致力于将它们一点点做得更好,不是吗？）。目前支持的版本如下：
- [Python 3.9](https://docs.python.org/3/whatsnew/3.9.html)
- [Jupyter-lab 3.0](https://jupyterlab.readthedocs.io/en/stable/getting_started/overview.html)  

#### Setup
- Put all Python packages into [requirements.txt](requirments.txt)
- `make init`: Build/rebuild the container.
- `make notebook`: Spin up the jupyter-lab built in the container.
- `make dash`: Go into the bash of the running container.  
