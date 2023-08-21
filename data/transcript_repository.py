class TranscriptRepository:
    def __init__(
            self,
            data_base_client
        ):
        self.data_base_client = data_base_client

    def searchSimilarityDocs(self, query):
        return self.data_base_client.similarity_search(query)