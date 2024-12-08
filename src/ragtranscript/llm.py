#!/usr/bin/env python
import logging
import json
import dotenv
import hashlib
import litellm

dotenv.load_dotenv()

llmmodel = "groq/Llama-3.3-70b-Versatile"
def call_lite_llm(input, responseFormat = None):    
    response = litellm.completion(
      model=llmmodel,
      temperature=0,
      max_tokens=8096,
      response_format=responseFormat,
      messages=[
        {"role": "system", "content": "You are a financial analyst."},
        {"role": "user", "content": input}
      ]
    )
    ideas = response['choices'][0]['message']['content']
    return ideas

def analyze_context(input, precontext, postcontext, responseFormat = None):
    logging.info("Analyzing context with:" + precontext + "\n" + postcontext)
    combinedmessage = precontext + input + postcontext
    hashed_message = hashlib.md5(combinedmessage.encode()).hexdigest()

    # Load answer from file 
    answer =""
    try:
        with open('../Data/LLMCache/cache.'+hashed_message+'.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            answer = data['answer']
            
    except FileNotFoundError:
        answer = call_lite_llm(combinedmessage, responseFormat)
        with open('../Data/LLMCache/cache.'+hashed_message+'.json', 'w', encoding='utf-8') as file:
            json.dump({'question': combinedmessage,'answer': answer}, file)
    return answer        

