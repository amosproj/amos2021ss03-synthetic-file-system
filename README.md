



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

[![Product Name Screen Shot][product-screenshot]](https://example.com)

<!-- Here's a blank template to get started:
 To avoid retyping too much info. Do a search and replace with your text editor for the following:
`amosproj`, `amos-ss2021-synthetic-file-system`, `twitter_handle`, `amos-fau-proj3@group.riehle.org`, `Synthetic File System`, `project_description` --> 


### Built With

* []()
* []()
* []()

### Product Vision

The rapidly growing mass of data requires further refinements and new technologies in order to find the right data in this deluge of information. The creation and management of metadata is decisive for representing the content of stored objects and files. This metadata is held in a database for instant retrieval. Lists can be constructed from these databases to find files and objects in general, but they do not yet afford access to the real data. For this reason, a synthetic file system is considerably useful. A synthetic file system enables to access data, chosen by queries in the database of metadata. Retrieval of project-related data is done through a distributed database and a virtual file system that permits a single namespace for all relevant data designated by their metadata.


### Project Mission

Due to the current Corona pandemic, as much data as possible is to be analyzed and evaluated with the help of artificial intelligence (AI). This requires a central intelligence to collect and interpret all accessible data distributed over several facilities. The key issue is that the data is organized and saved in different systems according to different storage types, structures, formats and criteria. The task, or rather mission is now to first make the data obtainable or readable via a uniform mechanism within the project time-frame. This would have the benefit of not having to adapt each application to the different memory types. The synthetic file system is a so-called adapter for each type of memory, so that a unified namespace can be formed from it.


<!-- GETTING STARTED -->
## Getting Started

<!--To get a local copy up and running follow these simple steps. -->

### Prerequisites

* git
* docker: [follow instructions for your platform](https://docs.docker.com/get-docker/)

<!--### Installation -->
### Installation

1. Clone the amos-ss2021-synthetic-file-system
   ```sh
   git clone https://github.com/amosproj/amos-ss2021-synthetic-file-system.git
   ```
2. The cloned repository contains two files needed to set up the docker containers (but this can also be done manually if you can't run them for some reason):
    Automatic:
        `.\init.sh   # Builds the docker container and downloads/sets up the metadatahub`
    Manually:
      Set up our docker and metadahub-docker:
      ```sh
      git clone https://github.com/amos-project2/metadata-hub
      cd metadata-hub
      docker pull amosproject2/metadatahub:latest
      docker volume create --name metadatahub-database -d local
      ```

      Run the metadatahub container container:
      ```sh
      docker run \
          -p 8080:8080 \
          -v /home/data:/filesystem  \
          -v metadatahub-database:/var/lib/postgresql/12/main \
          amosproject2/metadatahub &>/dev/null & disown;
      ```
      
      Run our container:
      ```sh
      docker run -it --net="host" --cap-add=SYS_ADMIN --device=/dev/fuse --security-opt apparmor:unconfined --tty fuse_skeleton
      ```
    


<!-- USAGE EXAMPLES -->
## Usage

1. The FUSE pulls its information from the running metadatahub webservice. This can be found at http://localhost:8080
   To fill in some dummy data go to "http://localhost:8080/?p=treewalk-controller" and start an action that parses some directory
    Notes:
    * You should set a date way in the past because the container may be running with a different date 
    * for some reason the treewalker sometimes does not parse directories when running a job (or I've been using it wrong).
          What always works is just giving it the root directory: "/, True"
    To verify that some files have been parsed go to http://localhost:8080/?p=graphiql-console and run the following query:
    ```query{searchForFileMetadata {numberOfTotalFiles}} ```
    If files were parsed correctly you should get a result with "numberOfTotalFiles" > 0.
   
2. Run the container via the ./run.sh script or manually. This should spawn a shell in the docker.
    WARNING: The way the FUSE is configured it runs in the foreground and blocks the current shell so that we can see debug output. 
    This obviously means that you can't use this shell to navigate the FUSE. This is why the container runs [tmux](https://github.com/tmux/tmux/wiki) (Terminal Multiplexer) which allows you to have multiple terminals at the same time.
    To spawn a new terminal in tmux run "ctrl+b %". To navigate between the two terminals use "ctrl+b 'arrow_keys'".
    An other option would be setting the FUSE to run in the background in `src/main.py:215`
   
3. To mount the metadatahub as a FUSE run the mount script: `./mount.sh`
4. Navigate to the directory mounted diractory: `cd /fuse_mount`
5. Navigate the directory via `ls` and `cd`
   

<!--Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

<!--_For more examples, please refer to the [Documentation](https://example.com)_



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



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* []()
* []()
* []()





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

