#this script is a getting started tutorial for how to use chromadb

# import the chromadb module
import chromadb
from .datafetch import get_transcript
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .llm import analyze_context

class RAG:
    _collection = None
    _client = None
    _idCounter = 0

    def __init__(self):
        self._client = chromadb.PersistentClient("./db")
        self._collection = self._client.get_or_create_collection("example_collection")
        self._idCounter = 0
        print("RAG initialized")

    def add_content(self, content, metadatadict):
        textsplitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100, length_function=len,
            is_separator_regex=False)
        chunks = textsplitter.create_documents([content])
        documents = []
        metadata = []
        ids = []

        for chunk in chunks:
            documents.append(chunk.page_content)
            metadata.append(metadatadict)
            ids.append(f"transcript_{self._idCounter}")
            self._idCounter += 1
        
        self._collection.upsert(
            documents=documents,
            metadatas=metadata,
            ids=ids
        )

    def add_transcript(self, ticker, year, quarter):
        t = get_transcript(ticker, year, quarter)
        self.add_content(t, {"document type": "Earning Call Transcript", "ticker": ticker, "year": year, "quarter": quarter})

    def query(self, query_texts, n_results):
        return self._collection.query(
            query_texts=query_texts,
            n_results=n_results
        )

def run():
    #Create a ChromaDB client
    rag = RAG()

    ticker = input("Please enter the ticker name: ")

    rag.add_transcript(ticker, 2024, 3)
    rag.add_transcript(ticker, 2024, 2)
    rag.add_transcript(ticker, 2024, 1)
    rag.add_transcript(ticker, 2023, 4)

    #Query the collection
    qry = input(f"What question do you want to ask about {ticker}: ")
    
    results = rag.query(
         query_texts=[qry], 
         n_results=20)

    print(analyze_context(str(results), 
        "Only use information that I provide and nothing from your internal knowledge. Summarize this text and answer "+qry,
          ""))

    return 0