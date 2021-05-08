import requests
import json

"""
This file is responsible for communicating with the metadata-hub.
All the classes in here are counterparts of elements in the Metadatahub database
Every variable in the classes has two types because they work in two ways. When serializing a request they signal
whether the variable is requests. When deserializing the retrieved value is put into the member.
An example for how to create a call would be:

res = MetadataResult()
f = File()
f.name = True
f.dir_path = True
res.files = f
res.number_of_total_files = True
e = Error()
e.message = True
e.stack_trace = True

m = MetadataQuery(res)
res = m.build_and_send_request()
"""


class Metadatum:
    name: str or bool = False
    value: str or bool = False


class Error:
    message: str or bool = False
    stack_trace: str or bool = False


class File:
    id: str or bool = False
    crawl_id: str or bool = False
    dir_path: str or bool = False
    name: str or bool = False
    type: str or bool = False
    size: str or bool = False
    metadata: [Metadatum] or Metadatum or bool = False
    creation_time: str or bool = False
    access_time: str or bool = False
    modification_time: str or bool = False
    file_hash: str or bool = False
    deleted: bool or bool = False


class MetadataResult:
    from_index: int or bool = False
    to_index: int or bool = False
    number_of_total_files: int or bool = False
    number_of_returned_files: int or bool = False
    files: [File] or File or bool = False
    error: Error or bool = False


class MetadataQuery:
    file_ids: bool or [int] = False
    crawl_ids: bool or [int] = False
    dir_path: bool or str = False
    dir_path_option: bool or [str] = False
    file_name: bool or str = False
    file_name_option: bool or [str] = False
    file_type: bool or [str] = False
    size: bool or int = False
    size_option: bool or str = False
    start_creation_time: bool or str = False
    end_creation_time: bool or str = False
    start_access_time: bool or str = False
    end_access_time: bool or str = False
    start_modification_time: bool or str = False
    end_modification_time: bool or str = False
    file_hashes: bool or [str] = False
    metadata_attributes: bool or [str] = False
    metadata_values: bool or [str] = False
    metadata_filter_logic_options: bool or str = False
    metadata_filter_logic: bool or str = False
    selected_attributes: bool or [str] = False
    sortBy: bool or [str] = False
    sortBy_options: bool or [str] = False
    limitFetchingSize: bool or int = False
    offset: bool or int = False
    showDeleted: bool = False

    meta_data_result: MetadataResult

    def __init__(self, meta_data_result):
        self.meta_data_result = meta_data_result

    @staticmethod
    def deserialize(query_result: str) -> MetadataResult:
        """
        Deserializes a webql answer
        :param query_result: The result recieved from the metadatahub
        :return: The deserialized result
        """

        query_md_result = MetadataResult()
        json_result = json.loads(query_result)
        json_content_data: dict = json_result["data"]["searchForFileMetadata"]
        query_md_result.number_of_total_files = \
            int(json_content_data["numberOfTotalFiles"]) if "numberOfTotalFiles" in json_content_data else -1

        query_md_result.numberOfReturnedFiles = \
            int(json_content_data["numberOfReturnedFiles"]) if "numberOfReturnedFiles" in json_content_data else -1

        query_md_result.from_index = int(json_content_data["from_index"]) if "from_index" in json_content_data else -1
        query_md_result.to_index = int(json_content_data["to_index"]) if "to_index" in json_content_data else -1
        query_md_result.error = Error()
        if "error" in json_content_data:
            error_data: dict = json_content_data["error"]
            query_md_result.error.message = error_data["message"] if "message" in error_data else ""
            query_md_result.error.stack_trace = error_data["stack_trace"] if "stack_trace" in error_data else ""

        query_md_result.files = []
        for json_file_data in json_content_data["files"]:
            file = File()
            file.id = json_file_data["id"] if "id" in json_file_data else ""
            file.crawl_id = json_file_data["crawl_id"] if "crawl_id" in json_file_data else ""
            file.name = json_file_data["name"] if "name" in json_file_data else ""
            file.type = json_file_data["type"] if "type" in json_file_data else ""
            file.dir_path = json_file_data["dir_path"] if "dir_path" in json_file_data else ""
            file.deleted = json_file_data["deleted"] if "deleted" in json_file_data else ""
            file.access_time = json_file_data["access_time"] if "access_time" in json_file_data else ""
            file.creation_time = json_file_data["creation_time"] if "creation_time" in json_file_data else ""
            file.modification_time = \
                json_file_data["modification_time"] if "modification_time" in json_file_data else ""
            file.dir_path = json_file_data["dir_path"] if "dir_path" in json_file_data else ""
            file.size = json_file_data["size"] if "size" in json_file_data else ""
            if "metadata" in json_file_data:
                json_metadata_data: dict = json_file_data["metadata"]
                file.metadata = Metadatum()
                file.metadata.name = json_metadata_data["name"]
                file.metadata.value = json_metadata_data["value"]

            query_md_result.files.append(file)

        return query_md_result

    def serialize(self) -> str:
        """
        Serializes the contents of this class into a webql query
        :return: The query as a simple string
        """

        # Build the query header
        query = "query { searchForFileMetadata"
        search_for_file_metadata_query = "("
        metadata_query_exists = False
        # Build the searchForFileMetadata filter function
        attributes = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith(
            "__") and not attr == "meta_data_result"]
        for i, attribute in enumerate(attributes):
            value = getattr(self, attribute)
            if value:
                search_for_file_metadata_query += f"{attribute}: {value}"
                metadata_query_exists = True
                if not i == len(attributes) - 1:
                    search_for_file_metadata_query += ", "
        # end the function and start the results block

        # empty function call is not allowed for some reason ¯\_(ツ)_/¯
        if metadata_query_exists:
            query += search_for_file_metadata_query
            query += ")"
        query += "{"

        # TODO optimize this, this is plain retarded, but I'm too lazy right now
        if self.meta_data_result.number_of_total_files:
            query += "\n numberOfTotalFiles \n"
        if self.meta_data_result.number_of_total_files:
            query += "\n numberOfReturnedFiles \n"
        if self.meta_data_result.number_of_total_files:
            query += "\n fromIndex \n"
        if self.meta_data_result.number_of_total_files:
            query += "\n toIndex \n"
        if type(self.meta_data_result.files) is File:
            query += "files {"

            # noinspection PyTypeChecker
            meta_data_result_file = self.meta_data_result.files  # type: File
            if meta_data_result_file.id:
                query += " \n id \n"
            if meta_data_result_file.crawl_id:
                query += " \n crawl_id \n"
            if meta_data_result_file.dir_path:
                query += " \n dir_path \n"
            if meta_data_result_file.name:
                query += " \n name \n"
            if meta_data_result_file.type:
                query += " \n name \n"
            if meta_data_result_file.size:
                query += " \n size \n"
            if meta_data_result_file.creation_time:
                query += " \n creation_time \n"
            if meta_data_result_file.modification_time:
                query += " \n modification_time \n"
            if meta_data_result_file.access_time:
                query += " \n access_time \n"
            if meta_data_result_file.file_hash:
                query += " \n file_hash \n"
            if meta_data_result_file.deleted:
                query += " \n deleted \n"
            if type(meta_data_result_file.metadata) is Metadatum:

                # noinspection PyTypeChecker
                meta_data_result_file_metadata = meta_data_result_file.metadata  # type: Metadatum
                query += " metadata {"
                if meta_data_result_file_metadata.name:
                    query += " \n name \n"
                if meta_data_result_file_metadata.value:
                    query += " \n value \n"
                query += "}"
            query += "}"

        if type(self.meta_data_result.error) is Error:

            # noinspection PyTypeChecker
            meta_data_result_error = self.meta_data_result.error  # type: Error
            query += "error {"
            if meta_data_result_error.message:
                query += " \n message \n"
            if meta_data_result_error.stack_trace:
                query += " \n stack_trace \n"
            query += "}"

        query += "}}"
        return query

    def build_and_send_request(self, url="http://localhost:8080/graphql") -> MetadataResult:
        """
        Serializes this classes content into a webql request and sends it to the metadatahub web service
        :param url: The url the metadatahub is running
        :return: The deserialized json result of the query
        """
        query = self.serialize()
        result = requests.post(url, json={"query": query})
        return self.deserialize(result.text)


# for testing purposes
if __name__ == '__main__':
    res = MetadataResult()
    f = File()
    f.name = True
    f.dir_path = True
    res.files = f
    res.number_of_total_files = True
    e = Error()
    e.message = True
    e.stack_trace = True

    m = MetadataQuery(res)
    res = m.build_and_send_request()
    print(res)
