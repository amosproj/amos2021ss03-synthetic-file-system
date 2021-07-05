# Python imports
import os
import stat
import time
from typing import Dict, List

# 3rd party imports
import anytree
import logging
import mdh

# Local imports
import sfs.backend
from sfs.backend import Backend
from sfs.paths import ROOT_PATH
from sfs.sfs_stat import SFSStat
from .mdh_util import QueryTemplates, MDHQuery
from ...dir_tree import DirectoryTree
import sfs.backend.mdh.backend_updater as backend_updater


class MDHBackend(Backend):
    """
    Implementation of the Backend interface for the MDH.
    For documentation of the functions see Backend.py
    """

    def __init__(self, mdh_id: int, instance_config: Dict):
        """
        Constructor for the Backend. Initializes the MDHBackendUpdater
        :param backend_id: id of the mdh backend (1,2,3,...)
        :param instance_config: configuration of this instance, retrieved by the config parser
        """
        self.mdh_id = mdh_id
        self.name = f'mdh{mdh_id}'
        self.instance_config = instance_config
        self.core = instance_config['core']
        self.result_structure = instance_config["resultStructure"]
        self.mdh_query = MDHQuery(self.core)
        self.directory_tree = None
        self.metadata_files: List[Dict] = []
        self._mdh_xattr = {}
        self.file_paths = []
        self.file_path_cache: set[str] = set()
        self.file_path_cache_copy: set[str] = set()
        self.backend_updater = backend_updater.MDHBackendUpdater(self)
        self._update_state()

    def rescan(self):
        """
        dirty hack to rescan the MDH and wait until the scan is done.
        This has to be done differently in the future!!!!!!!!
        :return: None
        """
        # noinspection PyBroadException
        try:
            self.file_path_cache_copy = self.file_path_cache.copy()
            core = self.instance_config['core']
            dir_path = os.path.dirname(os.path.abspath(__file__))
            mdh.harvest.schedule_add(core, dir_path + "/internals/rescan_mdh.graphql")
            mdh.harvest.schedule_add(core, dir_path + "/internals/rescan_mdh_dummy.graphql")
            while len(mdh.harvest.schedule_list(core)) != 0:
                pass
            mdh.harvest.active_stop(core, "Dummy")
        except Exception:
            pass
        self._update_state()

    def _update_state(self) -> None:
        """
        Updates the internal states of the backend
        :return: None
        """
        self._update_metadata_files()
        self._extract_file_paths()
        self.file_path_cache.difference_update(self.file_path_cache_copy)
        self.backend_updater.update_cache(self.file_path_cache)
        self._build_xattr_store()

    def get_file_paths(self):
        """
        Retrieves the file paths handled by this backend
        :return: list of the file paths handles by this backend
        """
        return self.file_paths

    def _build_xattr_store(self):
        for file in self.metadata_files:
            xattr = {}
            metadata = file.get('metadata', {})
            src = None
            for entry in metadata:
                if entry['name'] == 'SourceFile':
                    src = entry['value']
                else:
                    xattr.update({f'sfs.{entry["name"]}' : entry['value']})

            if src is not None:
                self._mdh_xattr.update({src: xattr})

    def _extract_file_paths(self):
        """
        Extracts all the file paths from the result of the query to the MDH and then builds
        the directory tree using these files
        :return: None
        """
        updated_file_paths = []
        for file in self.metadata_files:
            full_file_path = ""
            for metadata in file['metadata']:
                # TODO: should go in a separate function
                if metadata['name'] == "SourceFile":
                    full_file_path = metadata['value']
            updated_file_paths.append(full_file_path)

        self.file_paths = updated_file_paths
        self.directory_tree = DirectoryTree()
        self.directory_tree.build(sfs.backend.BackendManager().get_file_paths([self]), self.result_structure)

    def _extract_file_paths_parts(self) -> List[List[str]]:
        """
        Splits all the file paths handles by the MDH into all their single parts
        :return: 2D list of all the single parts
        """
        file_paths_parts = []
        for file_path in self.file_paths:
            file_paths_parts.append(file_path.split("/")[1:])
        return file_paths_parts

    def _update_metadata_files(self):
        """
        Updates the internal Metadata for every file using the result of the MDH query
        :return:
        """
        path = ""
        if self.instance_config['querySource'] == 'inline':
            query_options = self.instance_config['query']
            query = QueryTemplates.create_query(query_options)
            p = ROOT_PATH / 'sfs/backend/mdh/internals/inline_query.graphql'
            with open(p, 'w') as fpointer:
                fpointer.write(query)
            path = str(p)
        if self.instance_config['querySource'] == 'file':
            path = self.instance_config['query']['path']

        result = self.mdh_query.send_request_and_get_result(path)

        self.metadata_files = result['searchMetadata']['files']

    def contains_path(self, path: str) -> bool:
        """
        checks whether or not this backend handles a certain file/element
        :param path: path to this element
        :return: True if this backend contains this file, false otherwise
        """
        if path in [".", "..", f"/{self.name}"]:
            return True
        tree_path = "/Root" + path
        logging.info(f"contains path with: {path}")
        return self.directory_tree.contains(tree_path) or path in self.file_path_cache

    def _get_mdh_xattr(self, path):
        p = self._get_os_path(path)
        return self._mdh_xattr[p]

    def _get_os_path(self, path: str) -> str:
        """
        Retrieves the actual path of a file on the OS
        :param path: internal path to the file
        :return: os path of the file
        """
        p = "/" + "/".join(path.split("/")[2:])
        if self.result_structure == 'flat':
            p = f'{self.directory_tree.get_original_path(p[1:])}'
        return p

    def _add_to_cache(self, file_path: str) -> None:
        """
        Adds a file to the internal cache, and updates the cache file
        :param file_path: path to the file that will be added to the cache
        :return: None
        """
        self.file_path_cache.add(file_path)
        self.backend_updater.update_cache(self.file_path_cache)

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
        logging.info("getattr in mdh backend called!")

        path_stat = SFSStat()
        now = time.time()
        path_stat.st_atime = now
        path_stat.st_mtime = now
        path_stat.st_ctime = now

        if path in [".", "..", f"/{self.name}"]:
            path_stat.st_mode = stat.S_IFDIR | 0o755
            return path_stat.__dict__
        try:
            os_path = self._get_os_path(path)

            # /mdh/home/
            if os.path.isfile(os_path):
                print("got regular file")
                path_stat.st_mode = stat.S_IFREG | 0o755
            else:
                path_stat.st_mode = stat.S_IFDIR | 0o755

            print(os_path)
            os_stats = os.stat(os_path)
            path_stat.st_size = os_stats.st_size

        except anytree.resolver.ChildResolverError:
            # file does not exist yet
            logging.info("could not find file!")
            path_stat.st_size = os.stat(self._get_os_path(path)).st_size
        return path_stat.__dict__

    def readdir(self, path, fh):
        logging.info("readdir called!")

        print(f"readdir called with {path}")
        children = [".", ".."]

        for file in self.file_path_cache:
            if file.startswith(path):
                file_name = file.removeprefix(path).split("/")[1]
                children.append(file_name)

        children_node = self.directory_tree.get_children(path)
        for child in children_node:
            children.append(child)
            print(f"added {child}")
        return list(set(children))  # remove duplicates

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
        os.utime(self._get_os_path(path), times)

    def open(self, path, flags):
        logging.info(f"open called with {path}!")
        return os.open(self._get_os_path(path), flags)

    def create(self, path, mode, fi=None):
        logging.info(f"create mdh called with path {path}!")
        os_path = self._get_os_path(path)
        ret = os.open(os_path, os.O_RDWR | os.O_CREAT, mode)
        self._add_to_cache(path)
        return ret

    def read(self, path, length, offset, fh):
        logging.info("read called!")
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        logging.info("write called!")
        os.lseek(fh, offset, os.SEEK_SET)
        ret = os.write(fh, buf)
        self._add_to_cache(path)
        return ret

    def truncate(self, path, length, fh=None):
        logging.info("truncate called!")
        os.truncate(self._get_os_path(path), length)
        self._add_to_cache(path)

    def flush(self, path, fh):
        logging.info("flush called!")
        os.fsync(fh)

    def release(self, path, fh):
        logging.info("release called!")

    def fsync(self, path, fdatasync, fh):
        logging.info("fsync called!")
        os.fsync(fh)

    def getxattr(self, path, name, position=0):
        print("getxattr called")
        os_path = self._get_os_path(path)
        ret = None
        try:
            _xattr = self._get_mdh_xattr(path)
            return _xattr[name].encode('utf-8')
        except KeyError:
            # Not a mdh meta attribute
            pass
        ret = os.getxattr(os_path, name)
        return ret

    def listxattr(self, path):
        logging.info("listxattr called")
        os_path = self._get_os_path(path)
        ret = []
        try:
            ret += os.listxattr(os_path)
            print(ret)
        except OSError:
            # TODO: check for different errnos
            pass
        _xattr = self._get_mdh_xattr(path)
        _ret = [xattr for xattr in _xattr.keys()]
        ret += _ret
        return ret

    def setxattr(self, path, name, value, options, position=0):
        logging.info("setxattr called")
        os_path = self._get_os_path(path)
        ret = None
        try:
            ret = os.setxattr(os_path, name, value, options)
        except OSError:
            pass

        return ret

    def removexattr(self, path, name):
        logging.info("removexattr called")
        os_path = self._get_os_path(path)
        try:
            os.removexattr(os_path, name)
        except OSError:
            pass
        _xattr = self._get_mdh_xattr(path)
        del _xattr[name]
