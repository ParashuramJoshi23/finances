import os
from nltk.tokenize import sent_tokenize
import nltk
from langchain import LLMChain
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, validator
from .models import FinancialData
from django.conf import settings
from dotenv import load_dotenv
load_dotenv()


# Ensure NLTK data is downloaded
nltk.download('punkt')

# Define the structured output model
class CategorizedSentence(BaseModel):
    category: str = Field(description="One of Assets, Expenditures, Income, or Unclassified")
    fact_text: str = Field(description="The original sentence")

    @validator('category', allow_reuse=True)
    def validate_category(cls, v):
        valid_categories = ['Assets', 'Expenditures', 'Income', 'Unclassified']
        if v not in valid_categories:
            raise ValueError(f"Invalid category: {v}")
        return v

# Initialize the parser
parser = PydanticOutputParser(pydantic_object=CategorizedSentence)

# Define the prompt template
prompt_template = PromptTemplate(
    template="""
You are analyzing a conversation between a wealth manager and a client.
wealth manager is denoted by IFA and client is denoted by Mr. Thompson.
Classify the following sentence into one of the categories: "Assets", "Expenditures", "Income", or "Unclassified".

Sentence: "{sentence}"
Return the result in JSON format:
{format_instructions}
""",
    input_variables=["sentence"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)


def process_transcript(transcript_instance):
    # Read the transcript file
    
    transcript_path = transcript_instance.file.path
    with open(transcript_path, 'r', encoding='utf-8') as file:
        transcript_text = file.read()
    
    # Split transcript into sentences
    sentences = sent_tokenize(transcript_text)
    wealth_manager = "IFA"
    client = "Mr. Thompson"
    # Process each sentence
    for sentence in sentences:
        # Clean and skip empty sentences
        if wealth_manager in sentence:
            sentence.split(wealth_manager)[1]
        if client in sentence:
            sentence.split(client)[1]

        sentence = sentence.strip()
        if not sentence:
            continue
        
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

        # Create the chain
        chain = LLMChain(llm=llm, prompt=prompt_template)
        import openai
        # Run the chain
        try:
            output = chain.run(sentence=sentence)
            # Parse the output
            result = parser.parse(output)
            # Save to database
            FinancialData.objects.create(
                transcript=transcript_instance,
                category=result.category,
                fact_text=result.fact_text,
            )
            print(f"Processed sentence: {sentence}")
        except Exception as e:
            print(f"Error processing sentence: {sentence}")
            print(e)
        except openai.error.OpenAIError as e:
            print("Successfully accessed openai.error:", e)