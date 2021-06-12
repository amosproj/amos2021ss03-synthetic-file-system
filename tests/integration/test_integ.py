# Python imports
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
        self.DOCKER_YML = "/home/sfsuser/Vaidehi/docker-compose.yml"

        # Check if mdh core is running
        is_core_up = subprocess.Popen(["docker", "container", "inspect", "-f",
                                       "'{{.State.Running}}'", self.MDH_CORE], stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
        out, err = is_core_up.communicate()
        if "true" not in out.decode():
            raise Exception("MDH CORE NOT RUNNING!!!")

        docker_compose_up = subprocess.Popen(["docker-compose", "up", "-f", self.DOCKER_YML, "-d", "--build"], stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)
        docker_up_out, docker_up_err = docker_compose_up.communicate()
        if docker_up_err.decode().__contains__("error") == True:
            raise Exception("ERROR RUNNING DOCKER-COMPOSE UP!")

        # Check if subprocess is running
        is_up = docker_compose_up.poll()

        # Returns 0 if subprocess is alive, otherwise 1
        if is_up is not None:
            docker_start = subprocess.Popen(
                ["docker", "container", "start", "synthetic-file-system"], stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            is_up = docker_start.poll()
            if is_up is not None:
                raise Exception("Container synthetic-file-system cannot be started!!")

   
    def test_mount(self):
        print("/************************************* Entered test_mount *************************************/")

        # Run mount.sh
        docker_mount = subprocess.Popen(["docker", "container", "exec", "-d", "synthetic-file-system",
                                         "./mount.sh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        docker_mount_out, docker_mount_err = docker_mount.communicate()
        docker_mount_err = docker_mount_err.decode()
        if "failed" in docker_mount_err:
            raise Exception("ERROR RUNNING MOUNT.SH!!!")


    
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
    @classmethod
    def tearDownClass(self):
        print("/************************************* Entered tearDown *************************************/")

        docker_compose_down = subprocess.Popen(["docker-compose", "down"])

        # Check if subprocess is running
        is_down = docker_compose_down.poll()

        # Could do with an assertion error, I don't know which one.
        if is_down is None:
            raise Exception("************** COULD NOT SHUT DOWN DOCKER **************")
        else:
            docker_image_rm = subprocess.Popen(["docker", "image", "rm", "fuse_skeleton"])
            print("REMOVED DOCKER IMAGE")
