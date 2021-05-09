# 3rd party imports
import json
import unittest

# Local imports
from src.mdh_bridge \
    import MDHQueryRoot, MDHQuery_searchMetadata, MDHQuery_systemInfo, MDHMetadatatagDataType, MDHFile, MDHMetadatum


class TestBridge(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        query_root = MDHQueryRoot()
        # search query
        search_query = MDHQuery_searchMetadata()

        # setup search options
        search_query.filterFunctions = True
        search_query.selectedTags = True

        # setup result
        search_query.result.totalFilesCount = True
        search_query.result.returnedFilesCount = True
        search_query.result.instanceName = True
        search_query.result.timeZone = True
        search_query.result.fixedReturnColumnSize = True
        search_query.result.dataTypes = MDHMetadatatagDataType()
        search_query.result.dataTypes.name = True
        search_query.result.dataTypes.type = True

        # setup files
        search_query.result.files = MDHFile()
        search_query.result.files.id = True
        search_query.result.files.metadata = MDHMetadatum()
        search_query.result.files.metadata.value = True
        search_query.result.files.metadata.name = True

        query_root.queries.append(search_query)

        # system query
        system_query = MDHQuery_systemInfo()

        system_query.result.instanceName = True
        system_query.result.currentUserRole = True
        system_query.result.hostSystem = True

        query_root.queries.append(system_query)

        cls.query_root = query_root

    def test_deserialize(self) -> None:

        query_root = self.query_root

        graphql = json.dumps(
            {"data": {
                "searchMetadata": {
                    "totalFilesCount": 1446,
                    "returnedFilesCount": 1446,
                    "instanceName": "core-1",
                    "timeZone": "UTC",
                    "fixedReturnColumnSize": True,
                    "dataTypes": [
                        {
                            "name": "MIMEType",
                            "type": "str"
                        },
                        {
                            "name": "FileName",
                            "type": "str"
                        },
                        {
                            "name": "FileInodeChangeDate",
                            "type": "ts"
                        },
                        {
                            "name": "SourceFile",
                            "type": "str"
                        },
                        {
                            "name": "FileSize",
                            "type": "dig"
                        }
                    ],
                    "files": [
                        {
                            "id": "666",
                            "metadata": [
                                {
                                    "name": "FileName",
                                    "value": "image-00194.dcm"
                                },
                                {
                                    "name": "FileSize",
                                    "value": "86000"
                                },
                                {
                                    "name": "MIMEType",
                                    "value": "application/dicom"
                                },
                                {
                                    "name": "FileInodeChangeDate",
                                    "value": "2021-05-08 11:54:00"
                                },
                                {
                                    "name": "SourceFile",
                                    "value": "/mdh/dicom/series-00000/image-00194.dcm"
                                }
                            ]
                        }
                    ]
                },
                "systemInfo": {
                    "hostSystem": "Linux",
                    "currentUserRole": "ADMIN",
                    "instanceName": "core-1"
                }
            }}
        )

        query_root.deserialize(graphql)
        mdh_search_query = query_root.queries[0]
        mdh_system_query = query_root.queries[1]

        # search query tests
        self.assertEqual("searchMetadata", mdh_search_query.query_name)
        self.assertEqual(1446, mdh_search_query.result.totalFilesCount)
        self.assertEqual(1446, mdh_search_query.result.returnedFilesCount)
        self.assertEqual("core-1", mdh_search_query.result.instanceName)
        self.assertEqual("UTC", mdh_search_query.result.timeZone)
        self.assertEqual(True, mdh_search_query.result.fixedReturnColumnSize)

        dataTypes = mdh_search_query.result.dataTypes
        self.assertEqual("MIMEType", dataTypes[0].name)
        self.assertEqual("str", dataTypes[0].type)

        files = mdh_search_query.result.files
        self.assertEqual("666", files[0].id)
        self.assertEqual("FileName", files[0].metadata[0].name)
        self.assertEqual("image-00194.dcm", files[0].metadata[0].value)

        # system query tests
        self.assertEqual("Linux", mdh_system_query.result.hostSystem)
        self.assertEqual("ADMIN", mdh_system_query.result.currentUserRole)
        self.assertEqual("core-1", mdh_system_query.result.instanceName)

    def test_serialize(self) -> None:
        query_root = self.query_root
        mdh_search_query = query_root.queries[0]
        mdh_system_query = query_root.queries[1]

        graphql = query_root.serialize()

        # search query tests
        self.assertIn(mdh_search_query.query_name, graphql)
        self.assertIn(str(mdh_search_query.selectedTags), graphql)
        # TODO: test filterFunctions and filterLogicOption (probably unnecessary)

        # system query tests
        self.assertIn(mdh_system_query.query_name, graphql)
