from openai import OpenAI
import tiktoken

import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

from pypdf import PdfReader, PageRange
import os


api_key = os.environ.get('OPENAI_API_KEY')

## Function to read the uploaded PDF
def read_data_from_PDF(input_path):
  input_text = ''
  print ('Reading PDF from path', input_path)
  reader = PdfReader(input_path)
  number_of_pages = len(reader.pages)
  print ('PDF has been read with ', number_of_pages, ' pages')
  for page in reader.pages:
    input_text += page.extract_text() + "\n"
  return input_text


## Function to split the text into sentences
def split_text (input_text):
  split_texts = sent_tokenize(input_text)
  return split_texts


## Function to create chunks while considering sentences
def create_chunks(split_sents, max_token_len=50):
  enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
  current_token_len = 0
  input_chunks = []
  current_chunk = ""
  for sents in split_sents:
    sent_token_len = len(enc.encode(sents))
    if (current_token_len + sent_token_len) > max_token_len:
      input_chunks.append(current_chunk)
      current_chunk = ""
      current_token_len = 0
    current_chunk = current_chunk + sents
    current_token_len = current_token_len + sent_token_len
  if current_chunk != "":
    input_chunks.append(current_chunk)
  return input_chunks


## Function to create chunks
def create_input_chunks(input_text):
  split_sents = split_text(input_text)
  input_chunks = create_chunks(split_sents, max_token_len=3000)
  return input_chunks


## Function to create summary of the given input text
def create_summary_points(input_chunks):
  client = OpenAI(api_key=api_key)
  instructPrompt = """
                  Summarize the key points of the Women’s Movement and Feminism in Central Asia, highlighting historical challenges, current issues, and potential strategies for progress. Structure the summary to engage a podcast audience with progressive and anti colonial values and also make it sound casual.

                  - Highlight historical events
                  - Highlight uniqness of the culture and problems
                  - Make it less generalized
                  """
  podcastFacts = []
  for text in input_chunks:
    request = instructPrompt + '\n' + text
    chatOutput = client.chat.completions.create(model="gpt-3.5-turbo",
                                            messages=[{"role": "system", "content": "You are a helpful assistant."},
                                                      {"role": "user", "content": request}
                                                      ]
                                            )
    podcastFacts.append(chatOutput.choices[0].message.content)
  return "\n".join(podcastFacts)


## Two different prompt styles for the podcast conversation
debate_podcast_prompt = """
Could you simulate a podcast conversation in a debate-style between two women, \"Aisulu\" and \"AI\", discussing the following key points extracted from a research paper?
Some things that you need to keep in mind while creating the conversation:
- In the debate, Aisulu takes a stance that has a positive view of the findings and supports the implications and findings represented by these key points. They provide their reasoning and analogical examples to back up their interpretations.
- Conversely, AI adopts a more critical or alternative viewpoint. They question some of the findings by discussing potential drawbacks, limitations, or different outcomes.
- The conversation should see both experts engaging with each key point, presenting their views, challenging each other's interpretations, and discussing the broader implications of their arguments.
- The debate should be balanced, allowing each expert to articulate their perspective comprehensively.
- Conclude the conversation with each expert summarizing their overall position on the topic.
Here's some of the facts from the topic.
Kazakhstan are by no means passive subjects of the regime and the patriarchy.
Women become victims of gender-based violence and the government is not in a hurry to protect them and challenge its patriarchal structure.
Kazakhstani women marching against VAW and sexism on 8 March 2020 in Almaty Kazakhstan.
"""

casual_podcast_prompt = """
Could you simulate a podcast conversation between two friends \"Aisulu\" and \"AI\" having a conversation about the following facts?
Some things I'd like to ask:
  - Use \"Aisulu:\" and \"AI:\" to indicate who is speaking. Start the dialog with a casual discussion on where each person is from
  - Start the dialog with a casual discussion on what each person's hobby is right now.
  - Make the dialog about this as long as possible and make it sound funny
  - Sid is the one presenting the information, AI is asking intelligent questions that help Aisulu elaborate the facts.
Here's some of the facts from the topic.
"""

styles = {'casual':casual_podcast_prompt,
          'debate': debate_podcast_prompt}


## Function to create the podcast script
def create_podcast_script(podcast_points, output_style):
  client = OpenAI(api_key=api_key)
  instructPrompt = styles[output_style]
  request = instructPrompt + '\n' + podcast_points
  chatOutput = client.chat.completions.create(model="gpt-3.5-turbo-16k",
                                            messages=[{"role": "system", "content": "You are a helpful assistant."},
                                                      {"role": "user", "content": request}
                                                      ]
                                            )
  return chatOutput.choices[0].message.content


## Function to call all the podcast script generation steps
def create_podcast(input_path, output_style):
  input_text = read_data_from_PDF(input_path)
  input_chunks = create_input_chunks(input_text)
  podcastHighlights = create_summary_points(input_chunks)
  podcastScript = create_podcast_script(podcastHighlights, output_style)
  return podcastScript


## Function to generate speech from input text
def openai_generation(input_text, speaker_voice, model_choice="tts-1"):
  client = OpenAI(api_key=api_key)
  response = client.audio.speech.create(
      model=model_choice,
      voice=speaker_voice,
      input=input_text
  )
  return response.read()


## Function to generate complete audio podcast from script
## NOTE: this function assumes that there are only two speakers; please modify if you have multiple speakers in the script
def create_podcast_audio(podcastScript, speakerName1="Aisulu", speakerChoice1='shimmer', speakerName2="AI", speakerChoice2='alloy'):
  genPodcast = []
  podcastLines = podcastScript.split('\n\n')
  podcastLineNumber = 0
  for line in podcastLines:
    if podcastLineNumber % 2 == 0:
      speakerChoice = speakerChoice1
      line = line.replace(speakerName1+":", '')
    else:
      speakerChoice = speakerChoice2
      line = line.replace(speakerName2+":", '')
    genVoice = openai_generation(input_text=line, speaker_voice=speakerChoice, model_choice="tts-1")
    genPodcast.append(genVoice)
    podcastLineNumber += 1
  with open("genPodcast.mp3", "wb") as f:
    for pod in genPodcast:
      f.write(pod)
  return "genPodcast.mp3"

import gradio as gr

def upload_file(file):
    return file.name

with gr.Blocks() as demo:
    file_output = gr.File()
    upload_button = gr.UploadButton("Click to Upload a PDF", file_types=[".pdf"], file_count="single")
    upload_button.upload(upload_file, upload_button, file_output)
    podcast_style = gr.Dropdown(styles.keys(), label="podcast_style")
    generate_podcast_button = gr.Button("Generate Podcast Script")
    podcast_script = gr.Textbox(interactive=True, label="podcast_script")

    generate_podcast_button.click(fn=create_podcast, inputs=[file_output, podcast_style], outputs=podcast_script, api_name="generate_podcast_script")

    generate_audio_button = gr.Button("Generate Audio Version")
    podcast_audio = gr.Audio(label="podcast_audio", interactive=False, type="filepath")
    generate_audio_button.click(fn=create_podcast_audio, inputs=podcast_script, outputs=podcast_audio, api_name="generate_podcast_audio")

demo.launch(debug=True, share=True)