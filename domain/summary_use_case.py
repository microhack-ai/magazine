import os
import sys
sys.path.append('..')

from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from data.llm_repository import LlmRepository
from data.transcript_repository import TranscriptRepository
from data.transcript.local.database.vector.database_cliente import DatabaseClient
from data.transcript.local.mappers.transcript_local_mapper import TranscriptLocalMapper

class SummaryUseCase:
    def __init__(self, transcriptRepository, llmRepository):
        self.transcriptRepository = transcriptRepository
        self.llmRepository = llmRepository

    def getAnswer(self, query):
        similarityDocs = self.transcriptRepository.searchSimilarityDocs(query)
        answer = self.llmRepository.askAQuestion(input_documents = similarityDocs, question = query)
        return answer


'''
path_transcript = "/Users/dev/Documents/microhack.ai/summary/data/transcript/local/database/files/converted_to_plain_text"
mapper = TranscriptLocalMapper(path_transcript)
embeddings = mapper.get_embeddings()
docs = mapper.get_docs()
db = DatabaseClient(embeddings, docs)
'''
embedding_function= SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2") 
db3 = Chroma(persist_directory="chroma_db", embedding_function=embedding_function)

transcriptRepository = TranscriptRepository(db3)

apiKey = os.environ.get("OPENAI_API_KEY")
modelName = "gpt-3.5-turbo"
llm = ChatOpenAI(model_name=modelName)
llmRespository = LlmRepository(apiKey, modelName, llm)

useCase = SummaryUseCase(transcriptRepository, llmRespository)
print(useCase.getAnswer("time"))
