import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


class MusicLLM:
    def __init__(self, temperature=0.7):
       self.llm = ChatGroq(
           temperature=temperature,
           groq_api_key=os.getenv("GROQ_API_KEY"),
           model_name="llama-3.1-8b-instant"
       )
   
    def generate_melody(self,user_input):
        prompt = ChatPromptTemplate.from_template(
            "Generate a melody in the form of a list of musical notes based on the following input: {user_input}. "
            "Provide the output as a Python list of note strings (e.g., ['C4', 'E4', 'G4'])."
        )

        chain = prompt | self.llm
        return chain.invoke({"input" : user_input }).content.strip()
    
    def generate_harmony(self,melody):
        prompt = ChatPromptTemplate.from_template(
            "Create a harmony for the following melody: {melody}. Format: 1.0 0.5 0.5 2.0 ..."
        )

        chain = prompt | self.llm
        return chain.invoke({"melody" : melody }).content.strip()

    def adapt_style(self,style,melody,harmony,rythm):
        prompt = ChatPromptTemplate.from_template(
            "Adapt the following melody: {melody} and harmony: {harmony} with the rhythm pattern: {rythm} "
            "to match the style of {style}. Provide the output as a Python list of note strings."
        )

        chain = prompt | self.llm
        return chain.invoke({
            "style": style,
            "melody": melody,
            "harmony": harmony,
            "rhythm": rythm
        }).content.strip()