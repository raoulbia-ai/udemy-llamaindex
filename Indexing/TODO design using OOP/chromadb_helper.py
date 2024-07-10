import chromadb


class ChromaDBHelper:
    def __init__(self):
        # self.client = chromadb.HttpClient(host="localhost", port="8000")
        self.client = chromadb.EphemeralClient()
        print(f'existing collections: {self.client.list_collections()}')

    def delete_collection(self, collection_name):
        self.client.delete_collection(name=collection_name)

    def fetch_collection(self, collection_name):
        return self.client.get_collection(name=collection_name)

    def create_collection(self, collection_name):
        return self.client.create_collection(name=collection_name)


