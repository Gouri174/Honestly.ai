

#VoiceBot UI with Gradio
# import os
# import gradio as gr

# from brain_of_the_doctor import encode_image, analyze_image_with_query
# from voice_of_the_patient import record_audio, transcribe_with_groq
# from voice_of_the_doctor import text_to_speech_with_gtts, text_to_speech_with_elevenlabs

# #load_dotenv()

# system_prompt="""You have to act as a professional doctor, i know you are not but this is for learning purpose. 
#             What's in this image?. Do you find anything wrong with it medically? 
#             If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
#             your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
#             Donot say 'In the image I see' but say 'With what I see, I think you have ....'
#             Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
#             Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""


# def process_inputs(audio_filepath, image_filepath):
#     speech_to_text_output = transcribe_with_groq(GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
#                                                  audio_filepath=audio_filepath,
#                                                  stt_model="whisper-large-v3")

#     # Handle the image input
#     if image_filepath:
#         doctor_response = analyze_image_with_query(query=system_prompt+speech_to_text_output, encoded_image=encode_image(image_filepath), model="llama-3.2-11b-vision-preview")
#     else:
#         doctor_response = "No image provided for me to analyze"

#     voice_of_doctor = text_to_speech_with_elevenlabs(input_text=doctor_response, output_filepath="final.mp3") 

#     return speech_to_text_output, doctor_response, voice_of_doctor


# # Create the interface
# iface = gr.Interface(
#     fn=process_inputs,
#     inputs=[
#         gr.Audio(sources=["microphone"], type="filepath"),
#         gr.Image(type="filepath")
#     ],
#     outputs=[
#         gr.Textbox(label="Speech to Text"),
#         gr.Textbox(label="Doctor's Response"),
#         gr.Audio("Temp.mp3")
#     ],
#     title="AI Doctor with Vision and Voice"
# )

# iface.launch(debug=True)

# #http://127.0.0.1:7860

import os
import gradio as gr
from voice_of_the_patient import transcribe_audio
from voice_of_the_doctor import text_to_speech_with_elevenlabs
from brain_of_the_doctor import encode_image, analyze_image_with_query

# Language options (limited to what works with free plan)
LANGUAGES = [
    ("English", "en"),
    ("Hindi", "hi"),
    ("Tamil", "ta"),
    ("Telugu", "te"),
    ("Malayalam", "ml"),
    ("Bengali", "bn")
]

system_prompt = """You are a professional therapist. Analyze the image and provide medical advice.
Respond in the same language as the patient's query. If the query is in an Indian language, respond in that language.
Respond in a warm, caring manner as if you are speaking to a friend."""

def process_inputs(audio_filepath, image_filepath, text_input, language):
    # Process audio input
    if audio_filepath:
        query = transcribe_audio(audio_filepath, language=language)
    else:
        query = text_input

    # Process image if provided
    if image_filepath:
        encoded_image = encode_image(image_filepath)
        doctor_response = analyze_image_with_query(
            query=system_prompt + "\nPatient says: " + (query if query else "No query provided"),
            encoded_image=encoded_image,
            model="meta-llama/llama-4-scout-17b-16e-instruct"
        )
    else:
        doctor_response = "Please provide an image for analysis"

    # Generate speech (will use closest available voice for the language)
    tts_output = "doctor_response.mp3"
    text_to_speech_with_elevenlabs(
        input_text=doctor_response,
        output_filepath=tts_output,
        language=language
    )

    return query, doctor_response, tts_output

iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath"),
        gr.Textbox(label="Or type your query here"),
        gr.Dropdown(choices=LANGUAGES, label="Select Language", value="en")
    ],
    outputs=[
        gr.Textbox(label="Your Query"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio(label="Voice Response")
    ],
    title="Honestly.ai",
    description="Your AI Therapist (text, speak or image in your preferred language)"
)

iface.launch(debug=True)