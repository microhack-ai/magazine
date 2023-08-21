from langchain.chains.question_answering import load_qa_chain

class LlmRepository:
    def __init__(self, apiKey, modelName, llm):
        self.apiKey = apiKey
        self.modelName = modelName
        self.llm = llm

    def askAQuestion(self, input_documents, question):
        chain = load_qa_chain(self.llm, chain_type="stuff", verbose=True)
        return chain.run(input_documents=input_documents, question=question)
