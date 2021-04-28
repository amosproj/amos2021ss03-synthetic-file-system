import requests


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
    dir_path_option = False  # TODO
    file_name: bool or str = False
    file_name_option = False  # TODO
    file_type: bool or [str] = False
    size: bool or int = False
    start_creation_time: bool or str = False
    end_creation_time: bool or str = False
    start_access_time: bool or str = False
    end_access_time: bool or str = False
    start_modification_time: bool or str = False
    end_modification_time: bool or str = False
    file_hashes: bool or [str] = False
    metadata_attributes: bool or [str] = False
    metadata_values: bool or [str] = False
    metadata_filter_logic_options: bool = False  # TODO
    metadata_filter_logic: bool or str = False
    selected_attributes: bool or [str] = False
    sortBy: bool or [str] = False
    sortBy_options: bool = False  # TODO
    limitFetchingSize: bool or int = False
    offset: bool or int = False
    showDeleted: bool = False

    meta_data_result: MetadataResult

    def __init__(self, meta_data_result):
        self.meta_data_result = meta_data_result

    def build_query(self) -> str:

        # Build the query header
        query = "query { searchForFileMetadata"
        search_for_file_metadata_query = "("
        metadata_query_exists = False
        # Build the searchForFileMetadata filter function
        attributes = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__") and not attr == "meta_data_result"]
        for i, attribute in enumerate(attributes):
            value = getattr(self, attribute)
            print(f"{attribute}:{value}")
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
            print("adding file entry!")
            query += "files {"
            if self.meta_data_result.files.id:
                query += " \n id \n"
            if self.meta_data_result.files.crawl_id:
                query += " \n crawl_id \n"
            if self.meta_data_result.files.dir_path:
                query += " \n dir_path \n"
            if self.meta_data_result.files.name:
                query += " \n name \n"
            if self.meta_data_result.files.type:
                query += " \n name \n"
            if self.meta_data_result.files.size:
                query += " \n size \n"
            if self.meta_data_result.files.creation_time:
                query += " \n creation_time \n"
            if self.meta_data_result.files.modification_time:
                query += " \n modification_time \n"
            if self.meta_data_result.files.access_time:
                query += " \n access_time \n"
            if self.meta_data_result.files.file_hash:
                query += " \n file_hash \n"
            if self.meta_data_result.files.deleted:
                query += " \n deleted \n"
            if type(self.meta_data_result.files.metadata) is Metadatum:
                query += " metadata {"
                if self.meta_data_result.files.name:
                    query += " \n name \n"
                if self.meta_data_result.files.value:
                    query += " \n value \n"
                query += "}"
            query += "}"

        if type(self.meta_data_result.error) is Error:
            query += "error {"
            if self.meta_data_result.error.message:
                query += " \n message \n"
            if self.meta_data_result.error.stack_trace:
                query += " \n stack_trace \n"
            query += "}"

        query += "}}"
        return query


def send_request(query: str, url="http://localhost:8080/graphql") -> str:
    result = requests.post(url, json={"query": query})
    return result.text


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
    q = m.build_query()
    print(q)
    print(send_request(q))


