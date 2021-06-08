import anytree.resolver
from typing import Dict, List
from sfs.backend import Backend
from sfs.sfs_stat import SFSStat
from anytree import Node, Resolver, RenderTree
import logging
import os
import time
import stat
import mdh
from .query import MDHQueryRoot
import sfs.paths


class MDHBackend(Backend):
    """
    Implementation of the Backend interface for the MDH.
    For documentation of the functions see Backend.py
    """

    def __init__(self, instance_config: Dict):
        """
        Constructor
        :param root: the root node of the directory tree of the files that the backend is holding
        """
        self.instance_config = instance_config
        self.directory_tree = None
        self.metadata_files: List[Dict] = []
        self.file_paths = []
        self._update_state()

    def _update_state(self):
        self._update_metadata_files()
        self._extract_file_paths()

    def get_file_paths(self):
        return self.file_paths

    def _extract_file_paths(self):
        updated_file_paths = []
        for file in self.metadata_files:
            full_file_path = ""
            for metadata in file['metadata']:
                if metadata['name'] == "SourceFile":
                    full_file_path = metadata['value']
            updated_file_paths.append(full_file_path)

        self.file_paths = updated_file_paths

    def _extract_file_paths_parts(self) -> List[List[str]]:
        file_paths_parts = []
        for file_path in file_paths:
            file_paths_parts.append(file_path.split("/")[1:])
        return file_paths_parts

    def _update_metadata_files(self):
        core = self.instance_config['core']
        if self.instance_config['querySource'] == 'inline':
            raise NotImplementedError
        if self.instance_config['querySource'] == 'file':
            path = self.instance_config['query']['path']

        query_root = MDHQueryRoot(core, path)
        query_root.send_request_get_result()
        self.metadata_files = query_root.result['searchMetadata']['files']

    def contains_path(self, path: str) -> bool:
        return path in self.file_paths

    ######################
    # File System Calls #
    ######################
    def access(self, path, mode):
        logging.info("access called!")
        return 0

    def chmod(self, path, mode):
        logging.info("chmod called!")
        raise NotImplementedError()

    def chown(self, path, uid, gid):
        logging.info("chown called!")
        raise NotImplementedError()

    def getattr(self, path, fh=None):
        logging.info("getattr called!")
        path_stat = SFSStat()
        os_path = os.stat(path)

        path_stat.st_size = os_path.st_size

        now = time.time()
        path_stat.st_atime = now
        path_stat.st_mtime = now
        path_stat.st_ctime = now

        return path_stat.__dict__

    def readdir(self, path, fh):
        logging.info("readdir called!")

        print(f"readdir called with {path}")
        children = [".", ".."]

        file_finder = Resolver("name")
        path = path[1:]  # strip leading "/"
        path_node: Node = file_finder.get(self.directory_tree, path)
        child: Node
        for child in path_node.children:
            children.append(child.name)
            print(f"added {child.name}")
        return children

    def readlink(self, path):
        logging.info("readlink called!")
        raise NotImplementedError()

    def mknod(self, path, mode, dev):
        logging.info("mknod called!")
        raise NotImplementedError()

    def rmdir(self, path):
        logging.info("rmdir called!")
        raise NotImplementedError()

    def mkdir(self, path, mode):
        logging.info("mkdir called!")
        raise NotImplementedError()

    def statfs(self, path):
        logging.info("statfs called!")
        raise NotImplementedError()

    def unlink(self, path):
        logging.info("unlink called!")
        raise NotImplementedError()

    def symlink(self, name, target):
        logging.info("symlink called!")
        raise NotImplementedError()

    def rename(self, old, new):
        logging.info("rename called!")
        raise NotImplementedError()

    def link(self, target, name):
        logging.info("link called!")
        raise NotImplementedError()

    def utimens(self, path, times=None):
        logging.info("utimens called!")
        raise NotImplementedError()

    def open(self, path, flags):
        logging.info("open called!")
        return os.open(path, flags)

    def create(self, path, mode, fi=None):
        logging.info("create called!")
        ret = os.open(path, os.O_RDWR | os.O_CREAT, mode)
        data = b"test"
        os.write(ret, data)
        # TODO: trigger rescan in the MDH
        mdh.harvest.schedule_add("core-test", "rescan_mdh.graphql")
        time.sleep(10)
        # TODO remove content from file
        self.update_tree()
        return ret

    def read(self, path, length, offset, fh):
        logging.info("read called!")
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        logging.info("write called!")
        os.lseek(fh, offset, os.SEEK_SET)
        ret = os.write(fh, buf)
        # TODO trigger rescan
        return ret

    def truncate(self, path, length, fh=None):
        logging.info("truncate called!")
        raise NotImplementedError()

    def flush(self, path, fh):
        logging.info("flush called!")
        raise NotImplementedError()

    def release(self, path, fh):
        logging.info("release called!")
        raise NotImplementedError()

    def fsync(self, path, fdatasync, fh):
        logging.info("fsync called!")
        raise NotImplementedError()
