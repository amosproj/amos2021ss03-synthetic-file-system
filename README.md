



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in bracketChooses [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
<!--[![Last commit][commit-shield]][commit-url]-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Issues][issuesclosed-shield]][issuesclosed-url]
[![Kanban Board][board-shield]][board-url]
[![MIT License][license-shield]][license-url]
[![Open Source Love](https://badges.frapsoft.com/os/v3/open-source.png?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![Tests Passing][test-shield]][test-url]
[![Tests Passing][code-shield]][code-url]


<!-- ![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg?style=for-the-badge)



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/amosproj/amos-ss2021-synthetic-file-system">
    <img src="Deliverables/final_logo.svg" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Synthetic File System</h3>

  <p align="center">
    The student team is to develop a new file system that provides a unified view ona pre-configured set of existing file systems. The new virtual file system is        to:
  <br>●Be implemented as a Linux FUSE (filesystem in user space) module<br />
  <br>●Be POSIX compliant; initially, only read-only functions are needed<br />
  <br>●Integrate NTFS, ext4, and S3 object stores<br />
  <br>●Be able to filter which files are shown using meta-data<br />
  <br>●Be configured from a configuration file during startup time<br />
  <br><br><br /><br />
  <br>Test cases are<br />
  
 <br> ●Browsing using an existing Linux file system browser (e.g. Nautilus)<br />
  <br>●Using cp to copy from the new virtual file system<br />
    <br />
    <a href="https://github.com/amosproj/amos-ss2021-synthetic-file-system"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/amosproj/amos-ss2021-synthetic-file-system">View Demo</a>
    ·
    <a href="https://github.com/amosproj/amos-ss2021-synthetic-file-system/issues">amos-ss2021-synthetic-file-systemrt Bug</a>
    ·
    <a href="https://github.com/amosproj/amos-ss2021-synthetic-file-system/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project


This project implements a so called [FUSE](https://en.wikipedia.org/wiki/Filesystem_in_Userspace), a filesystem in userspace, in order to give a unified filesystem view on data in a [Metadatahub](www.metadatahub.de) database.  
The FUSE also allows for filtering the files it will show according to their metadata

<!-- Here's a blank template to get started:
 To avoid retyping too much info. Do a search and replace with your text editor for the following:
`amosproj`, `amos-ss2021-synthetic-file-system`, `twitter_handle`, `amos-fau-proj3@group.riehle.org`, `Synthetic File System`, `project_description` --> 


### Product Vision

The rapidly growing mass of data requires further refinements and new technologies in order to find the right data in this deluge of information. The creation and management of metadata is decisive for representing the content of stored objects and files. This metadata is held in a database for instant retrieval. Lists can be constructed from these databases to find files and objects in general, but they do not yet afford access to the real data. For this reason, a synthetic file system is considerably useful. A synthetic file system enables to access data, chosen by queries in the database of metadata. Retrieval of project-related data is done through a distributed database and a virtual file system that permits a single namespace for all relevant data designated by their metadata.


### Project Mission

Due to the current Corona pandemic, as much data as possible is to be analyzed and evaluated with the help of artificial intelligence (AI). This requires a central intelligence to collect and interpret all accessible data distributed over several facilities. The key issue is that the data is organized and saved in different systems according to different storage types, structures, formats and criteria. The task, or rather mission is now to first make the data obtainable or readable via a uniform mechanism within the project time-frame. This would have the benefit of not having to adapt each application to the different memory types. The synthetic file system is a so-called adapter for each type of memory, so that a unified namespace can be formed from it.

--- 
<!-- GETTING STARTED -->
## **Getting Started**

<!--To get a local copy up and running follow these simple steps. -->

### Prerequisites

* git
* docker: [follow instructions for your platform](https://docs.docker.com/get-docker/) (Only needed if you want to try the fuse in the docker)
* docker-compose (Only needed if you want to try the fuse in the docker)
* [Metadatahub](www.metadatahub.de)

<!--### Installation -->
### Installation

1. Clone the amos-ss2021-synthetic-file-system
   ```sh
   git clone https://github.com/amosproj/amos-ss2021-synthetic-file-system.git
   ```
2. If you want to try the FUSE in a docker environment, build it with
    ```sh
    cd amos-ss2021-synthetic-file-system
    docker-compose up --build 
    ```
  
   For subsequent uses you can just run
    ```sh
    docker-compose up
    ```
  

   Then you can connect to the docker from a different shell via
    ```sh
    docker exec -it synthetic-file-system tmux
    ```
    where ```tmux``` can also be replaced by ```zsh``` or ```bash```, depending on your preferences.

3. This fileystem will be mounted under ```~/fuse_mount```. Create this folder for later use:
    ```sh
    mkdir ~/fuse_mount
    ```
    

--- 
<!-- USAGE EXAMPLES -->
## Usage
### Basics

1. The FUSE pulls its information from a running [Metadatahub](www.metadatahub.de) service. For more information or documentation refer to the vendor.

2. To run the FUSE, run
   ```sh
    ./mount.sh
   ```
   This will mount the virtual filesystem under ~/fuse_mount

3. Attention when under using docker:
  Since the FUSE blocks the current terminal, a new terminal in the docker has to be opened. For this you can just open a new terminal on the host and connect it again to the docker via ```docker exec -it synthetic-file-system tmux ```, or use tmux in the docker to open a new terminal (```ctrl+b -> ctrl+%```). For more information please refer to the [tmux documentation](https://github.com/tmux/tmux/wiki)

4. Traverse the virtual filesystem via a terminal, or via any file browser like ```nautilus```. 
For docker: The docker container is configured to support X-forwarding, so any UI program opened on the docker will be forwarded to the host. So to traverse the filesystem using a file browser under the docker, just run 
   ```sh
    nautilus
   ```
   from a terminal that is connected to the docker.

### Configuration

The FUSE allows for filtering of the files that it will list via their metadata. For this, a config file, ```config/config.cfg``` is used. When starting, the FUSE reads all the filters from this file and applies them when retrieving the metadata from the Metadatahub.   
The filters are specified as a list of triplets, where the first element of each triplet specifies the name of the metadata that the filter shall use, the second one a value, and as the third some relation specifies how values are compared to the one specified in the filter.  

For example, to tell the FUSE to only show all ".jpg" files with an image height greater 500, a config file could look something like this:
```toml
[FILTER]
filters = [
    ["FileName", "DME-30521-7.jpeg", "EQUAL"] ,
    ["ImageHeight", "500", "GREATER"],
]
```
This filter is applied when the FUSE is first mounted, however, when changing that file at runtime, the filters will be updated. 

**NOTE**  
The way the dynamic configuration works, it is needed, that the config file is written to and closed properly, just for example pressing ```ctrl+s``` won't always work. So when ```VIM``` for example, close the file with ```:wq``` or ```:x```.
   

<!--Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

<!--_For more examples, please refer to the [Documentation](https://example.com)_ -->



----------------------------------------------------------------------- 

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/amosproj/amos-ss2021-synthetic-file-system/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

<!--Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

<!--1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request-->





<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.





<!-- CONTACT -->
## Contact

AMOS PROJECT - amos-fau-proj3@group.riehle.org

Industry Partner - GRAU Data

Project Link: [https://github.com/amosproj/amos-ss2021-synthetic-file-system](https://github.com/amosproj/amos-ss2021-synthetic-file-system)



<!-- ACKNOWLEDGEMENTS 
## Acknowledgements

* []()
* []()
* []() -->





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
<!--[commit-shield]: "https://img.shields.io/github/last-commit/amosproj/amos-ss2021-synthetic-file-system.svg?style=for-the-badge
[commit-url]: https://github.com/amosproj/amos-ss2021-synthetic-file-system/commits/master-->
[contributors-shield]: https://img.shields.io/github/contributors/amosproj/amos-ss2021-synthetic-file-system.svg
[contributors-url]: https://github.com/amosproj/amos-ss2021-synthetic-file-system/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/amosproj/amos-ss2021-synthetic-file-system.svg
[forks-url]: https://github.com/amosproj/amos-ss2021-synthetic-file-system/network/members
[stars-shield]: https://img.shields.io/github/stars/amosproj/amos-ss2021-synthetic-file-system.svg
[stars-url]: https://github.com/amosproj/amos-ss2021-synthetic-file-system/stargazers
[issues-shield]: https://img.shields.io/github/issues/amosproj/amos-ss2021-synthetic-file-system.svg
[issues-url]: https://github.com/amosproj/amos-ss2021-synthetic-file-system/issues
[issuesclosed-shield]: https://img.shields.io/github/issues-closed/amosproj/amos-ss2021-synthetic-file-system.svg
[issuesclosed-url]: https://github.com/amosproj/amos-ss2021-synthetic-file-system/issues?q=is%3Aissue+is%3Aclosed
[board-shield]: https://img.shields.io/badge/Kanban-Board-grey?logo=data:image/svg%2bxml;base64,PHN2ZyB2aWV3Qm94PSIwIDAgMjQgMjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTEzLjM1MiAxNC41ODVsLTQuNTA5IDQuNjE0LjcyLTQuMDYyTDMuNDI4IDcuNTcgMCA3Ljc1MyA3LjU4IDB2Mi45NTNsNy4yMTQgNi42NDYgNC41MTMtMS4xMDUtNC42ODkgNC45ODJMMjQgMjRsLTEwLjY0OC05LjQxNXoiLz48L3N2Zz4=
[board-url]: https://github.com/amosproj/amos-ss2021-synthetic-file-system/projects/1
[license-shield]: https://img.shields.io/github/license/amosproj/amos-ss2021-synthetic-file-system.svg
[license-url]: https://github.com/amosproj/amos-ss2021-synthetic-file-system/blob/main/LICENSE
[test-shield]: https://img.shields.io/github/contributors/amosproj/amos-ss2021-synthetic-file-system.svg
[test-url]: https://github.com/amosproj/amos-ss2021-synthetic-file-system/github-readme-stats/actions
[code-shield]: https://codecov.io/gh/anuraghazra/github-readme-stats/branch/master/graph/badge.svg
[code-url]: https://github.com/amosproj/amos-ss2021-synthetic-file-system/github-readme-stats

