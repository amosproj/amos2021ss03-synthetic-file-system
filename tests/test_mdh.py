# 3rd party imports
import json
import unittest

# Local import
from src.mdh_bridge import MDHQueryRoot, MDHQuery_searchMetadata, MDHMetadatatagDataType, MDHFile, MDHMetadatum


class TestBridge(unittest.TestCase):

    def setUp(self):
        query_root = MDHQueryRoot()
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

        self.query_root = query_root

    def test_deserialize(self):

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
                }
            }}
        )

        query_root.deserialize(graphql)
        mdh_query = query_root.queries[0]

        self.assertEqual("searchMetadata", mdh_query.query_name)
        self.assertEqual(1446, mdh_query.result.totalFilesCount)
        self.assertEqual(1446, mdh_query.result.returnedFilesCount)
        self.assertEqual("core-1", mdh_query.result.instanceName)
        self.assertEqual("UTC", mdh_query.result.timeZone)
        self.assertEqual(True, mdh_query.result.fixedReturnColumnSize)

        dataTypes = mdh_query.result.dataTypes
        self.assertEqual("MIMEType", dataTypes[0].name)
        self.assertEqual("str", dataTypes[0].type)

        files = mdh_query.result.files
        self.assertEqual("666", files[0].id)
        self.assertEqual("FileName", files[0].metadata[0].name)
        self.assertEqual("image-00194.dcm", files[0].metadata[0].value)

    def test_serialize(self):
        query_root = self.query_root

        print(json.loads(query_root.serialize()))

        self.assertTrue(False)
