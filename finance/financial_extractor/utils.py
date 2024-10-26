import os
from nltk.tokenize import sent_tokenize
import nltk
from langchain import OpenAI, LLMChain
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, validator
from .models import FinancialData
from django.conf import settings

# Ensure NLTK data is downloaded
nltk.download('punkt')

# Define the structured output model
class CategorizedSentence(BaseModel):
    category: str = Field(description="One of Assets, Expenditures, Income, or Unclassified")
    fact_text: str = Field(description="The original sentence")

    @validator('category')
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
You are an expert financial analyst.

Classify the following sentence into one of the categories: "Assets", "Expenditures", "Income", or "Unclassified".

Sentence: "{sentence}"

Return the result in JSON format:

{format_instructions}
""",
    input_variables=["sentence"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

# Initialize the LLM with your OpenAI API key
llm = OpenAI(temperature=0)

# Create the chain
chain = LLMChain(llm=llm, prompt=prompt_template)

def process_transcript(transcript_instance):
    # Read the transcript file
    transcript_path = transcript_instance.file.path
    with open(transcript_path, 'r', encoding='utf-8') as file:
        transcript_text = file.read()

    # Split transcript into sentences
    sentences = sent_tokenize(transcript_text)

    # Process each sentence
    for sentence in sentences:
        # Clean and skip empty sentences
        sentence = sentence.strip()
        if not sentence:
            continue

        # Run the chain
        try:
            output = chain.run(sentence=sentence)
            # Parse the output
            result = parser.parse(output)
            if result.category != "Unclassified":
                # Save to database
                FinancialData.objects.create(
                    transcript=transcript_instance,
                    category=result.category,
                    fact_text=result.fact_text,
                )
        except Exception as e:
            print(f"Error processing sentence: {sentence}")
            print(e)
