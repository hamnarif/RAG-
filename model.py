from operator import itemgetter
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from supabase.client import Client, create_client
from langchain_core.runnables import RunnablePassthrough
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain.schema import format_document
from langchain_core.messages import get_buffer_string
from langchain_core.runnables import RunnableParallel
from langchain.prompts.prompt import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()


supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

embeddings = GPT4AllEmbeddings()
llm= ChatOllama(
    temperature=0,
    model="mistral",
    streaming=True,
    verbose=True
)
vectorstore = SupabaseVectorStore(
    embedding=embeddings,
    client=supabase,
    table_name="documents",
    query_name="match_documents",
)
retriever = vectorstore.as_retriever()

_template = """Given the following conversation and a follow up question, 
rephrase the follow up question to be a standalone question, in its original language, 
that can be used to query a FAISS index. This query will be used to retrieve documents with additional context.

Let me share a couple examples.

If you do not see any chat history, you MUST return the "Follow Up Input" as is:
```
Chat History:
Follow Up Input: How is Lawrence doing?
Standalone Question:
How is Lawrence doing?
```

If this is the second question onwards, you should properly rephrase the question like this:
```
Chat History:
Human: How is Lawrence doing?
AI: 
Lawrence is injured and out for the season.
Follow Up Input: What was his injury?
Standalone Question:
What was Lawrence's injury?
```

Now, with those examples, here is the actual chat history and input question.
Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:
[your response here]"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

template = """
You are an assistant for question-answering tasks. \
Use the following pieces of retrieved context to answer the question. \
Make sure not to make any changes to the context if possible when prepare answers so as to provide accurate responses.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Answer the question based only on the following context:
{context}
At the end of each answer you should contain metadata for relevant document in the form of (chapter name, section number).
For example, if context has `metadata`:(source:'docu_url', section_number:1.3, chapter_name: Chapter 1), you should display (Chapter 1, section 1.3).
Question: {question}
"""
ANSWER_PROMPT = ChatPromptTemplate.from_template(template)

DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(template="{page_content}")


def _combine_documents(
    docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"
):
    doc_strings = [format_document(doc, document_prompt) for doc in docs]
    return document_separator.join(doc_strings)

_inputs = RunnableParallel(
    standalone_question=RunnablePassthrough.assign(
        chat_history=lambda x: get_buffer_string(x["chat_history"])
    )
    | CONDENSE_QUESTION_PROMPT
    | llm
    | StrOutputParser(),
)
_context = {
    "context": itemgetter("standalone_question") | retriever | _combine_documents,
    "question": lambda x: x["standalone_question"],
}
conversational_qa_chain = _inputs | _context | ANSWER_PROMPT | llm

