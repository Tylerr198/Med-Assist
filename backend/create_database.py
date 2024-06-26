from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

def load_documents():
    document_loader = PyPDFDirectoryLoader('backend/data')
    documents = document_loader.load()

    # add metadata to use for filtering
    for document in documents:
        document.metadata['filename'] = document.metadata['source'][13:-4]
    return documents

def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

documents = load_documents()
chunks = split_documents(documents)
embedding = HuggingFaceEmbeddings()

# create vectore store into chromadb
vectorstore = Chroma.from_documents(documents=chunks, embedding=embedding, persist_directory="backend/chroma_db")