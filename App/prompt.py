openai_api_key = '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'

from langchain.llms import OpenAI

llm = OpenAI(model_name="text-ada-001", openai_api_key=openai_api_key)
response = llm("What day comes after Friday?")
print(response)