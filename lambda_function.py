import json
import s3fs
from llama_index.core import StorageContext, load_index_from_storage
from langchain.schema import Document
from langchain_core.retrievers import BaseRetriever
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains import (
    create_history_aware_retriever,
    create_retrieval_chain,
)
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import PrivateAttr
from typing import List, Any

class LlamaIndexRetrieverWrapper(BaseRetriever):
    _llama_retriever: Any = PrivateAttr()

    def __init__(self, llama_retriever):
        """
        Initialize the wrapper with the LlamaIndex retriever.

        Args:
            llama_retriever: A LlamaIndex VectorIndexRetriever object.
        """
        super().__init__()
        self._llama_retriever = llama_retriever

    def get_relevant_documents(self, query: str) -> List[Document]:
        """
        Retrieve relevant documents for a given query.

        Args:
            query: The query string.

        Returns:
            A list of LangChain Document objects.
        """
        llama_docs = self._llama_retriever.retrieve(query)
        langchain_docs = []

        for node_with_score in llama_docs:
            # Extract the `Node` object
            node = node_with_score.node

            # Create a LangChain Document object
            langchain_doc = Document(
                page_content=node.text,
                metadata=node.metadata if hasattr(node, "metadata") else {}
            )
            langchain_docs.append(langchain_doc)

        return langchain_docs

    async def aget_relevant_documents(self, query: str) -> List[Document]:
        """
        Asynchronous version of `get_relevant_documents`.

        Args:
            query: The query string.

        Returns:
            A list of LangChain Document objects.
        """
        llama_docs = await self._llama_retriever.aretrieve(query)
        langchain_docs = []

        for node_with_score in llama_docs:
            # Extract the `Node` object
            node = node_with_score.node

            # Create a LangChain Document object
            langchain_doc = Document(
                page_content=node.text,
                metadata=node.metadata if hasattr(node, "metadata") else {}
            )
            langchain_docs.append(langchain_doc)

        return langchain_docs


s3 = s3fs.S3FileSystem(anon=False)

s3_bucket_name = 'my.bucket112123'
s3_prefix = 'storage/'

persist_dir = f'{s3_bucket_name}/{s3_prefix}'

#index
storage_context = StorageContext.from_defaults(persist_dir=persist_dir, fs=s3)
index = load_index_from_storage(storage_context)

#Retriever
llama_retriever = index.as_retriever(search_kwargs={"k": 5})
retriever = LlamaIndexRetrieverWrapper(llama_retriever)

#Memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

#LLM
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, just "
    "reformulate it if needed and otherwise return it as is."
)
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)

qa_system_prompt = (
    "You are an assistant for question-answering tasks. Use "
    "the following pieces of retrieved context to answer the "
    "question. If you don't know the answer, just say that you "
    "don't know. If the question is not somehow related to Data "
    "Mining, then say that and do not answer it.  Use three sentences maximum "
    "and keep the answer concise."
    ""
    "{context}"
)

qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt), 
        MessagesPlaceholder("chat_history"), 
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

rag_chain = create_retrieval_chain(
    history_aware_retriever, question_answer_chain
)

chat_history = []

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        print("parsed json")
        print(body)
    except:
        print("Error parsing JSON")

    try: 
        query = body.get('query')
        print("parsed query")
        print(query)
    except:
        print("Error parsing query")
    
    try:
        print(chat_history)
        response = rag_chain.invoke({"input": query, "chat_history": chat_history})
    except:
        print("Error invoking RAG chain")

    try:
        chat_history.append({"role": "user", "content": query})
        chat_history.append({"role": "assistant", "content": response["answer"]})
    except:
        print("Error updating chat history")

    try:
        dict = {"answer": response["answer"]}
    except:
        print("Error creating response dictionary")

    return {
        'statusCode': 200,
        'body': json.dumps(dict)
    }
