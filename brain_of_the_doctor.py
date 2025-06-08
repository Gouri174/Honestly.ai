# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

# #Step1: Setup GROQ API key
# import os

# GROQ_API_KEY=os.environ.get("GROQ_API_KEY")

# #Step2: Convert image to required format
# import base64


# #image_path="acne.jpg"

# def encode_image(image_path):   
#     image_file=open(image_path, "rb")
#     return base64.b64encode(image_file.read()).decode('utf-8')

# #Step3: Setup Multimodal LLM 
# from groq import Groq

# query="Is there something wrong with my face?"
# model = "meta-llama/llama-4-scout-17b-16e-instruct"
# #model="llama-3.2-90b-vision-preview" #Deprecated

# def analyze_image_with_query(query, model, encoded_image):
#     client=Groq()  
#     messages=[
#         {
#             "role": "user",
#             "content": [
#                 {
#                     "type": "text", 
#                     "text": query
#                 },
#                 {
#                     "type": "image_url",
#                     "image_url": {
#                         "url": f"data:image/jpeg;base64,{encoded_image}",
#                     },
#                 },
#             ],
#         }]
#     chat_completion=client.chat.completions.create(
#         messages=messages,
#         model=model
#     )

#     return chat_completion.choices[0].message.content

import os
import base64
from groq import Groq

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Language-specific prompts
LANGUAGE_PROMPTS = {
    "en": "You are a compassionate, empathetic therapist speaking to a friend. Respond in warm, caring language.",
    "hi": "आप एक दयालु, संवेदनशील मनोचिकित्सक हैं जो मित्र की तरह बात करते हैं। उत्तर गर्मजोशी और देखभाल से दें।",
    "ta": "நீங்கள் ஒரு நண்பரிடம் பேசும் ஒரு இரக்கமுள்ள, பரிவுணர்வு மிக்க சிகிச்சையாளர். அன்பான, அக்கறையுள்ள மொழியில் பதிலளிக்கவும்.",
    "te": "మీరు ఒక స్నేహితుడితో మాట్లాడుతున్న కరుణామయ, సానుభూతిగల చికిత్సకుడు. వెచ్చని, శ్రద్ధగల భాషలో స్పందించండి.",
    "ml": "നിങ്ങൾ ഒരു സുഹൃത്തിനോട് സംസാരിക്കുന്ന അനുകമ്പയുള്ള, സഹാനുഭൂതിയുള്ള ഒരു തെറാപ്പിസ്റ്റാണ്. ഊഷ്മളവും കരുതലുള്ളതുമായ ഭാഷയിൽ പ്രതികരിക്കുക.",
    "bn": "তুমি একজন সহানুভূতিশীল, সহানুভূতিশীল থেরাপিস্ট, বন্ধুর সাথে কথা বলো। উষ্ণ, যত্নশীল ভাষায় উত্তর দাও।"
}

def encode_image(image_path):
    """Encode image to base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image_with_query(query, encoded_image, language="en", model="meta-llama/llama-4-scout-17b-16e-instruct"):
    """
    Analyze image with multilingual support
    
    Args:
        query: Patient's query
        encoded_image: Base64 encoded image
        language: Language code (en, hi, ta, te, ml, bn)
        model: Groq model to use
    """
    client = Groq(api_key=GROQ_API_KEY)
    
    # Get language-specific prompt
    system_prompt = LANGUAGE_PROMPTS.get(language, LANGUAGE_PROMPTS["en"])
    
    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": query},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}",
                    },
                },
            ],
        }
    ]
    
    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model,
            temperature=0.7,
            max_tokens=300
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error in analysis: {str(e)}"