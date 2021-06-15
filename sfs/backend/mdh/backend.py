# Python imports
import os
import time
import stat

# 3rd party imports
import anytree
from anytree import Node, Resolver
from typing import Dict, List
import logging
import mdh

# Local imports
import sfs.paths
from sfs.backend import Backend
import sfs.backend
from sfs.sfs_stat import SFSStat
from .query import MDHQueryRoot
from ...dir_tree import DirectoryTree


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

    def _rescan(self):
        """
        dirty hack to rescan the MDH and wait until the scan is done.
        This has to be done differently in the future!!!!!!!!
        :return: None
        """
        try:
            logging.error("1")
            core = self.instance_config['core']
            logging.error("6")
            dir_path = os.path.dirname(os.path.abspath(__file__))
            mdh.harvest.schedule_add(core, dir_path + "/internals/rescan_mdh.graphql")
            mdh.harvest.schedule_add(core, dir_path + "/internals/rescan_mdh_dummy.graphql")
            logging.error("5")
            while len(mdh.harvest.schedule_list(core)) != 0:
                pass
            mdh.harvest.active_stop(core, "Dummy")
            logging.error("4")
        except Exception:
            logging.error("2")
            pass
        logging.error("3")
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
        self.directory_tree = DirectoryTree()
        self.directory_tree.build(sfs.backend.BackendManager().get_file_paths([self]))

    def _extract_file_paths_parts(self) -> List[List[str]]:
        file_paths_parts = []
        for file_path in self.file_paths:
            file_paths_parts.append(file_path.split("/")[1:])
        return file_paths_parts

    def _update_metadata_files(self):
        core = self.instance_config['core']
        if self.instance_config['querySource'] == 'inline':
            raise NotImplementedError
        if self.instance_config['querySource'] == 'file':
            path = self.instance_config['query']['path']

        query_root = MDHQueryRoot(core, path)

        result = query_root.send_request_get_result()

        self.metadata_files = result['searchMetadata']['files']

    def contains_path(self, path: str) -> bool:
        if path in [".", "..", "/", "/mdh"]:
            return True
        path = "/Root" + path
        logging.error(f"contains path with: {path}")
        return self.directory_tree.contains(path)

    def _get_os_path(self, path):
        return "/" + "/".join(path.split("/")[2:])

    ######################
    # File System Calls #
    ######################

    def access(self, path, mode):
        logging.error("access called!")
        return 0

    def chmod(self, path, mode):
        logging.error("chmod called!")
        raise NotImplementedError()

    def chown(self, path, uid, gid):
        logging.error("chown called!")
        raise NotImplementedError()

    def getattr(self, path, fh=None):
        logging.error("getattr in mdh backend called!")

        path_stat = SFSStat()
        now = time.time()
        path_stat.st_atime = now
        path_stat.st_mtime = now
        path_stat.st_ctime = now

        if path in [".", "..", "/", "/mdh"]:
            path_stat.st_mode = stat.S_IFDIR | 0o755
            return path_stat.__dict__
        try:
            # /mdh/home/
            mdh_path = "/Root" + path
            os_path = "/" + "/".join(path.split("/")[2:])

            if self.directory_tree.is_file(mdh_path):
                print("got regular file")
                path_stat.st_mode = stat.S_IFREG | 0o755
            else:
                path_stat.st_mode = stat.S_IFDIR | 0o755

            os_stats = os.stat(os_path)
            path_stat.st_size = os_stats.st_size

        except anytree.resolver.ChildResolverError:
            # file does not exist yet
            logging.error("could not find file!")
            path_stat.st_size = os.stat(self._get_os_path(path)).st_size
        return path_stat.__dict__

    def readdir(self, path, fh):
        logging.error("readdir called!")

        print(f"readdir called with {path}")
        children = [".", ".."]

        children_node = self.directory_tree.get_children(path)
        for child in children_node:
            children.append(child)
            print(f"added {child}")
        return children

    def readlink(self, path):
        logging.error("readlink called!")
        raise NotImplementedError()

    def mknod(self, path, mode, dev):
        logging.error("mknod called!")
        raise NotImplementedError()

    def rmdir(self, path):
        logging.error("rmdir called!")
        raise NotImplementedError()

    def mkdir(self, path, mode):
        logging.error("mkdir called!")
        raise NotImplementedError()

    def statfs(self, path):
        logging.error("statfs called!")
        raise NotImplementedError()

    def unlink(self, path):
        logging.error("unlink called!")
        raise NotImplementedError()

    def symlink(self, name, target):
        logging.error("symlink called!")
        raise NotImplementedError()

    def rename(self, old, new):
        logging.error("rename called!")
        raise NotImplementedError()

    def link(self, target, name):
        logging.error("link called!")
        raise NotImplementedError()

    def utimens(self, path, times=None):
        logging.error("utimens called!")
        os.utime(self._get_os_path(path), times)

    def open(self, path, flags):
        logging.error(f"open called with {path}!")
        return os.open(self._get_os_path(path), flags)

    def create(self, path, mode, fi=None):
        # TODO: The mdh does not harvest empty files, so some random info is written to the file before the harvest
        # TODO: and then deleted. While this works, it leads to the metadata potentially being wrong :(
        logging.error(f"create mdh called with path {path}!")
        os_path = self._get_os_path(path)
        logging.error(f"creating with os path! {os_path}!")
        ret = os.open(os_path, os.O_RDWR | os.O_CREAT, mode)
        data = b"test"
        os.write(ret, data)
        logging.error(f"rescanning! {os_path}!")
        self._rescan()
        # remove content from file
        os.truncate(os_path, 0)
        logging.error(f"created file! {os_path}!")
        return ret

    def read(self, path, length, offset, fh):
        logging.error("read called!")
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        logging.error("write called!")
        os.lseek(fh, offset, os.SEEK_SET)
        ret = os.write(fh, buf)
        self._rescan()
        return ret

    def truncate(self, path, length, fh=None):
        logging.error("truncate called!")
        os.truncate(self._get_os_path(path), length)

    def flush(self, path, fh):
        logging.error("flush called!")
        os.fsync(fh)

    def release(self, path, fh):
        logging.error("release called!")

    def fsync(self, path, fdatasync, fh):
        logging.error("fsync called!")
        os.fsync(fh)
