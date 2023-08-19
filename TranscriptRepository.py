from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
import webvtt

directory = './transcripts'

# Modified function to handle unexpected line structures in the VTT file
def convert_vtt_to_txt_safe_corrected(infile, outfile):
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


def convert_vtt_to_txt(infile, outfile):
    """Convert VTT subtitle file to a plain text file."""
    vtt = webvtt.read(infile)
    transcript = ""
    lines = []
    last_speaker = None
    for line in vtt:
        speaker = line.lines[0].split('>')[0].split('v ')[1]
        if last_speaker != speaker:
            lines.append('\n'+speaker + ': ')
        lines.extend(line.text.strip().splitlines())
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

def load_docs(directory):
  loader = DirectoryLoader(directory)
  documents = loader.load()
  return documents

def split_docs(documents,chunk_size=1000,chunk_overlap=20):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  docs = text_splitter.split_documents(documents)
  return docs

transcript = "Tim Ferriss - How to Learn Better & Create Your Best Future _ Huberman Lab Podcast-doupx8SAs5Y.en.vtt"
#convert_vtt_to_txt_safe_corrected(transcript,"out.txt")


documents = load_docs(directory)
docs = split_docs(documents)
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma.from_documents(docs, embeddings)
query = "What type of intermittent fasting are named?"
matching_docs = db.similarity_search(query)
matching_docs[0]
print(matching_docs[0])

