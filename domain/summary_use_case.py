import os
import sys
sys.path.append('..')

from langchain.chat_models import ChatOpenAI
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



path_transcript = "/Users/dev/Documents/microhack.ai/summary/data/transcript/local/database/files/converted_to_plain_text"
mapper = TranscriptLocalMapper(path_transcript)
embeddings = mapper.get_embeddings()
docs = mapper.get_docs()
db = DatabaseClient(embeddings, docs)

transcriptRepository = TranscriptRepository(db)

apiKey = os.environ.get("OPENAI_API_KEY")
modelName = "gpt-3.5-turbo"
llm = ChatOpenAI(model_name=modelName)
llmRespository = LlmRepository(apiKey, modelName, llm)

useCase = SummaryUseCase(transcriptRepository, llmRespository)
print(useCase.getAnswer("What do you now about fasting?"))
