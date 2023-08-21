from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
import webvtt

class TranscriptLocalMapper:
    def __init__(
            self,
            transcript_directory
        ):
        self.transcript_directory = transcript_directory

    def convert_to_plain_text(self, infile, outfile):
        """Convert VTT subtitle file to a plain text file with error handling for Caption objects."""
        vtt = webvtt.read(infile)
        transcript = ""
        lines = []
        last_speaker = None
        for caption in vtt:
            try:
                # Attempt to split and extract speaker using the lines attribute of the Caption object
                speaker = caption.lines[0].split('>')[0].split('v ')[1]
            except IndexError:
                # If there's an error, set speaker to "Unknown"
                speaker = "Unknown"
            if last_speaker != speaker:
                lines.append('\n' + speaker + ': ')
            # Use caption.text to extract the text from the Caption object
            lines.extend(caption.text.strip().splitlines())
            last_speaker = speaker
        previous = None
        for line in lines:
            if line == previous:
                continue
            transcript += f" {line}"
            previous = line
        with open(outfile, 'w') as f:
            f.write(transcript)
        print(f'Length of original:\t{len(vtt.content)} characters\nLength of final:\t{len(transcript)} characters\nPercent Reduction:\t{100 - len(transcript)*100/len(vtt.content):.0f}%')

    def load_docs(self, directory):
        loader = DirectoryLoader(directory,show_progress=True)
        documents = loader.load()
        return documents

    def split_docs(self, documents):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
        docs = text_splitter.split_documents(documents)
        return docs
    
    def get_embeddings(self):
        return SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2") 
    
    def get_docs(self):
        documents = self.load_docs(self.transcript_directory)
        return self.split_docs(documents)