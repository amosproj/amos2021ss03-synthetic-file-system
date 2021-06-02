# HOW TO EXECUTE?
# First install the package: pip install pytest-docker-compose
# Run with: pytest --docker-compose="path_to_docker_compose_yml" test_integ.py

import pytest
import os
import subprocess
import unittest
import time
import sys
import logging


class TestIntegratedTool(unittest.TestCase):


    def setUp(self):
        print("/************************************* Entered setUp *************************************/")

        self.mounted_files = []
        self.FUSE_MOUNTED_FILES_LIST = "/tmp/Mounted_files.lst"
        self.MDH_CORE = "core-sfs"
        self.MOUNTED_FROM = "/home/sfsuser/Vaidehi/amos-rep/test_tree"


        # Check if mdh core is running
        is_core_up = subprocess.Popen(["docker", "container", "inspect", "-f",
	                              "'{{.State.Running}}'", self.MDH_CORE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = is_core_up.communicate()
        if "true" not in out.decode():
            print("MDH CORE NOT RUNNING!!!")
            exit()

        docker_compose_up=subprocess.Popen(["docker-compose", "up"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        docker_up_out, docker_up_err = docker_compose_up.communicate()
        if docker_up_err.decode().__contains__("error") == True:
            print("ERROR RUNNING DOCKER-COMPOSE UP!")
            exit()

        # Check if subprocess is running
        is_up=docker_compose_up.poll()

        # Returns 0 if subprocess is alive, otherwise 1
        if is_up is not None:
            docker_start = subprocess.Popen(
                ["docker", "container", "start", "synthetic-file-system"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            is_up = docker_start.poll()
            if is_up is not None:
                print("Container synthetic-file-system cannot be started!!")
                exit()
        else:
            # Added sleep because docker takes time to be set up
            time.sleep(30)

    
    @pytest.mark.dependency()
    def test_mount(self):
        print("/************************************* Entered test_mount *************************************/")

        # Start docker just in case it is down
        docker_start=subprocess.Popen(
            ["docker", "container", "start", "synthetic-file-system"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


        # Run mount.sh
        docker_mount=subprocess.Popen(["docker", "container", "exec", "-d", "synthetic-file-system",
                                         "./mount.sh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        docker_mount_out, docker_mount_err=docker_mount.communicate()
        docker_mount_err = docker_mount_err.decode()
        if "failed" in docker_mount_err:
             print("ERROR RUNNING MOUNT.SH!!!")
             exit()

        time.sleep(5)

        # goes into the container and gets a list of all files under fuse_mount and writes it to a file
        self.mounted_files=os.popen(
            'docker container exec synthetic-file-system /bin/sh -c "cd ..; cd /fuse_mount; find . -type f" ').read()
        f=open(self.FUSE_MOUNTED_FILES_LIST, 'w')
        print(self.mounted_files, file=f)
        f.close()

        # Throws error if file containing mounted data is empty
        if os.stat(self.FUSE_MOUNTED_FILES_LIST).st_size == 0:
            print("Mounted files list at " + self.FUSE_MOUNTED_FILES_LIST, " empty!!!")
            exit()



    @pytest.mark.dependency(depends=['test_mount'])
    def test_dir_structure(self):
        print("/************************************* Entered test_dir_structure *************************************/")

        common_dir = self.MOUNTED_FROM.split("/")

        # Read all fuse files into an array
        fuse_mounted_files=open(self.FUSE_MOUNTED_FILES_LIST, "r")
        fuse_abs_mount_lines=fuse_mounted_files.readlines()
        fuse_mounted_files.close()

        # transforms '/home/sfsuser/Vaidehi/amos-rep/test_tree/dir0/dir144/dir158/dir160/dir164/dir165/CNV-1699976-2.jpeg' into '/dir0/dir144/dir158/dir160/dir164/dir165/CNV-1699976-2.jpeg'
        fuse_mount_lines=[i.split(common_dir[-1], 1)[1]
                            for i in fuse_abs_mount_lines]

        # Checks if files found at mounted_from were actually mounted on the vfs
        for root, dirs, files in os.walk(self.MOUNTED_FROM):
            for f in files:
                # /home/sfsuser/Vaidehi/amos-rep/test_tree/dir0/dir144/dir158/dir160/dir164/dir165/CNV-1699976-2.jpeg
                file_path=os.path.join(root, f)
                req_path=file_path.split(common_dir[-1])

                if (req_path[1] in fuse_mount_lines) == False:
                    self.assertRaises(FileNotFoundError)


    # Turn off docker services
    def tearDown(self):
        print("/************************************* Entered tearDown *************************************/")

        docker_compose_down=subprocess.Popen(["docker-compose", "down"])
        time.sleep(5)

        # Check if subprocess is running
        is_down=docker_compose_down.poll()

        # COuld do with an assertion error, I don't know which one.
        if is_down is None:
            print("************** COULD NOT SHUT DOWN DOCKER **************")
