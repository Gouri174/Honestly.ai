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

def analyze_with_empathy(query, encoded_image, language="en", model="meta-llama/llama-4-scout-17b-16e-instruct"):
    """
    Analyze input with DASS sentiment awareness and empathy
    
    Args:
        query: Patient's query
        encoded_image: Base64 encoded image (optional)
        language: Language code
        model: Groq model
    """
    client = Groq(api_key=GROQ_API_KEY)
    
    # Updated prompt with DASS instructions
    SYSTEM_PROMPTS = {
        "en": "You are a compassionate therapist. Analyze the patient's emotional state using DASS (Depression, Anxiety, Stress Scales) principles. Look for signs of: "
               "1. Depression (hopelessness, low energy, self-criticism)\n"
               "2. Anxiety (excessive worry, restlessness, tension)\n"
               "3. Stress (overwhelm, irritability, difficulty relaxing)\n"
               "Respond with warm, caring language tailored to their emotional needs.",
        "hi": "आप एक दयालु चिकित्सक हैं। डीएएसएस (डिप्रेशन, एंग्जाइटी, स्ट्रेस स्केल) सिद्धांतों का उपयोग करके रोगी की भावनात्मक स्थिति का विश्लेषण करें। "
               "इन संकेतों की तलाश करें:\n"
               "1. अवसाद (निराशा, कम ऊर्जा, आत्म-आलोचना)\n"
               "2. चिंता (अत्यधिक चिंता, बेचैनी, तनाव)\n"
               "3. तनाव (अभिभूत होना, चिड़चिड़ापन, आराम करने में कठिनाई)\n"
               "उनकी भावनात्मक जरूरतों के अनुरूप गर्मजोशी और देखभाल के साथ उत्तर दें।",
        "ta": "நீங்கள் ஒரு இரக்கமுள்ள சிகிச்சையாளர். DASS (மனச்சோர்வு, கவலை, அழுத்த அளவுகோல்கள்) கொள்கைகளைப் பயன்படுத்தி நோயாளியின் உணர்ச்சி நிலையை பகுப்பாய்வு செய்யவும். "
               "இந்த அறிகுறிகளைத் தேடவும்:\n"
               "1. மனச்சோர்வு (நிராசை, குறைந்த சக்தி, சுய விமர்சனம்)\n"
               "2. கவலை (அதிக கவலை, அமைதியின்மை, அழுத்தம்)\n"
               "3. அழுத்தம் (மிகவும் சோர்வு, கோபம், ஓய்வெடுக்க முடியாமை)\n"
               "அவர்களின் உணர்ச்சி தேவைகளுக்கு ஏற்ப அன்பான, பரிவுள்ள மொழியில் பதிலளிக்கவும்.",
        "te": "మీరు ఒక కరుణామయ చికిత్సకుడు. DASS (డిప్రెషన్, ఆందోళన, ఒత్తిడి స్కేల్స్) సూత్రాలను ఉపయోగించి రోగి యొక్క భావోద్వేగ స్థితిని విశ్లేషించండి. "
               "ఈ సంకేతాలను చూడండి:\n"
               "1. డిప్రెషన్ (నిరాశ, తక్కువ శక్తి, ఆత్మ విమర్శ)\n"
               "2. ఆందోళన (అత్యధిక ఆందోళన, అస్థిరత, ఒత్తిడి)\n"
               "3. ఒత్తిడి (అతిగా ఒత్తిడి, కోపం, విశ్రాంతి తీసుకోవడంలో కష్టాలు)\n"
               "వారి భావోద్వేగ అవసరాలకు అనుగుణంగా వెచ్చని, శ్రద్ధగల భాషలో స్పందించండి.",
        "ml": "നിങ്ങൾ ഒരു കരുണയുള്ള ചികിത്സകനാണ്. DASS (ഡിപ്രെഷൻ, ആൻസൈറ്റി, സ്ട്രെസ് സ്കെയിലുകൾ) സിദ്ധാന്തങ്ങൾ ഉപയോഗിച്ച് രോഗിയുടെ വികാരാവസ്ഥ വിശകലനം ചെയ്യുക. "
               "ഈ ലക്ഷണങ്ങൾക്കായി നോക്കുക:\n"
               "1. ഡിപ്രെഷൻ (നിരാശ, കുറഞ്ഞ ഊർജം, സ്വയം വിമർശനം)\n"
               "2. ആൻസൈറ്റി (അത്യധികം ആശങ്ക, അസ്ഥിരത, സമ്മർദ്ദം)\n"
               "3. സ്ട്രെസ് (അധിക സമ്മർദ്ദം, കോപം, വിശ്രമിക്കാൻ ബുദ്ധിമുട്ട്)\n"
               "അവരുടെ വികാര ആവശ്യങ്ങൾക്ക് അനുയോജ്യമായ സ്നേഹപൂർവ്വവും കരുതലുമായ ഭാഷയിൽ പ്രതികരിക്കുക.",
        "bn": "আপনি একজন সহানুভূতিশীল চিকিৎসক। DASS (ডিপ্রেশন, উদ্বেগ, চাপ স্কেল) নীতিগুলি ব্যবহার করে রোগীর আবেগগত অবস্থার বিশ্লেষণ করুন। "
               "এই লক্ষণগুলির জন্য দেখুন:\n"
               "1. ডিপ্রেশন (নিরাশা, কম শক্তি, আত্ম-সমালোচনা)\n"
               "2. উদ্বেগ (অতিরিক্ত উদ্বেগ, অস্থিরতা, চাপ)\n"
               "3. চাপ (অতিরিক্ত চাপ, বিরক্তি, বিশ্রাম নিতে অসুবিধা)\n"
               "তাদের আবেগগত প্রয়োজনের জন্য উপযুক্ত উষ্ণ, যত্নশীল ভাষায় প্রতিক্রিয়া জানান।"
        
    }
    
    system_prompt = SYSTEM_PROMPTS.get(language, SYSTEM_PROMPTS["en"])
    
    # Build message content
    user_content = [{"type": "text", "text": query}]
    if encoded_image:
        user_content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}
        })

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content}
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
        return f"Error: {str(e)}"