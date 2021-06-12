# HOW TO EXECUTE?
# First install the package: pip install pytest-docker-compose
# Run with: pytest --docker-compose="path_to_docker_compose_yml" test_integ.py

import pytest
import os
import subprocess
import unittest


class TestIntegratedTool(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        print("/************************************* Entered setUp *************************************/")

        self.MDH_CORE = "core-sfs"
        self.MOUNT_POINT = "/home/sfsuser/Vaidehi"

        # Check if mdh core is running
        is_core_up = subprocess.Popen(["docker", "container", "inspect", "-f",
                                       "'{{.State.Running}}'", self.MDH_CORE], stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
        out, err = is_core_up.communicate()
        if "true" not in out.decode():
            print("MDH CORE NOT RUNNING!!!")
            exit(1)

        docker_compose_up = subprocess.Popen(["docker-compose", "up", "-d", "--build"], stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)
        docker_up_out, docker_up_err = docker_compose_up.communicate()
        if docker_up_err.decode().__contains__("error") == True:
            print("ERROR RUNNING DOCKER-COMPOSE UP!")
            exit(1)

        # Check if subprocess is running
        is_up = docker_compose_up.poll()

        # Returns 0 if subprocess is alive, otherwise 1
        if is_up is not None:
            docker_start = subprocess.Popen(
                ["docker", "container", "start", "synthetic-file-system"], stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            is_up = docker_start.poll()
            if is_up is not None:
                print("Container synthetic-file-system cannot be started!!")
                exit(1)

    @pytest.mark.dependency()
    def test_mount(self):
        print("/************************************* Entered test_mount *************************************/")

        # Run mount.sh
        docker_mount = subprocess.Popen(["docker", "container", "exec", "-d", "synthetic-file-system",
                                         "./mount.sh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        docker_mount_out, docker_mount_err = docker_mount.communicate()
        docker_mount_err = docker_mount_err.decode()
        if "failed" in docker_mount_err:
            print("ERROR RUNNING MOUNT.SH!!!")
            exit(1)


    @pytest.mark.dependency(depends=['test_mount'])
    def test_open_file(self):
        print("/************************************* Entered test_open_file *************************************/")

        counter = 0
        for root, dirs, files in os.walk("/home/sfsuser/Vaidehi"):
            for f in files:
                file_path = os.path.join(root, f)
                if counter == 0:
                    if file_path.endswith(('.pdf', '.txt', '.docx', '.xlsx', '.html', '.csv')):
                        try:
                            check_read = open(file_path, 'r')
                            counter += 1
                        except IOError as x:
                            print(
                                "************* UNABLE TO OPEN MOUNTED FILES!!! ***************")
                            exit(1)
                else:
                    break


    # Turn off docker services
    def tearDownClass(self):
        print("/************************************* Entered tearDown *************************************/")

        docker_compose_down = subprocess.Popen(["docker-compose", "down"])

        # Check if subprocess is running
        is_down = docker_compose_down.poll()

        # Could do with an assertion error, I don't know which one.
        if is_down is None:
            print("************** COULD NOT SHUT DOWN DOCKER **************")
