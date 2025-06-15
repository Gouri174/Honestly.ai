import os
import gradio as gr
from voice_of_the_patient import transcribe_audio
from voice_of_the_doctor import text_to_speech_with_elevenlabs
from brain_of_the_doctor import analyze_with_empathy, encode_image
from login import log_activity

LANGUAGES = [
    ("English", "en"),
    ("Hindi", "hi"),
    ("Tamil", "ta"),
    ("Telugu", "te"),
    ("Malayalam", "ml"),
    ("Bengali", "bn")
]

def process_inputs(audio_filepath, image_filepath, text_input, language, username, email):
    try:
        log_activity(username, email, "Started therapy session")
        
        if audio_filepath:
            query = transcribe_audio(audio_filepath, language=language) or ""
            log_activity(username, email, f"Audio input transcribed: {query[:50]}...")
        else:
            query = text_input or ""
            log_activity(username, email, f"Text input provided: {query[:50]}...")
        
        encoded_image = None
        if image_filepath:
            encoded_image = encode_image(image_filepath)
            log_activity(username, email, "Image uploaded and processed")
        
        therapist_response = analyze_with_empathy(
            query=query,
            encoded_image=encoded_image,
            language=language
        )
        log_activity(username, email, f"Therapist response generated: {therapist_response[:50]}...")
        
        tts_output = f"response_{username}.mp3"
        if text_to_speech_with_elevenlabs(therapist_response, tts_output, language):
            log_activity(username, email, "Voice response generated successfully")
            return query, therapist_response, tts_output
        return query, therapist_response, None
        
    except Exception as e:
        error_msg = {
            "en": "I'm having trouble responding. Could you try again?",
            "hi": "मुझे जवाब देने में कठिनाई हो रही है। कृपया पुनः प्रयास करें",
            "ta": "இப்போது பதிலளிக்க எனக்கு சிக்கல் உள்ளது. மீண்டும் முயற்சிக்கலாமா?",
            "te": "ప్రస్తుతం స్పందించడంలో ఇబ్బంది ఉంది. మళ్లీ ప్రయత్నించగలరా?",
            "ml": "ഇപ്പോൾ പ്രതികരിക്കാൻ ഞാൻ ബുദ്ധിമുട്ട് അനുഭവിക്കുന്നു. വീണ്ടും ശ്രമിക്കാമോ?",
            "bn": "এখনই উত্তর দিতে আমার সমস্যা হচ্ছে। আপনি কি আবার চেষ্টা করতে পারেন?"
        }
        log_activity(username, email, f"Error occurred: {str(e)}")
        return query, error_msg.get(language, error_msg["en"]), None

def launch_app():
    """Launch the full application with login and main interface"""
    with gr.Blocks() as app:
        # Create state to track authentication
        auth_state = gr.State({"authenticated": False, "username": "", "email": ""})
        
        # Login interface
        with gr.Column(visible=True) as login_col:
            gr.Markdown("## Welcome to Honestly.ai - Please Login")
            username = gr.Textbox(label="Username")
            email = gr.Textbox(label="Email")
            login_btn = gr.Button("Login")
            status = gr.Textbox(label="Status", interactive=False)
        
        # Main interface (initially hidden)
        with gr.Column(visible=False) as main_col:
            with gr.Row():
                audio_input = gr.Audio(sources=["microphone"], type="filepath", label="Record your feelings")
                image_input = gr.Image(type="filepath", label="Optional: Share a relevant image")
            
            text_input = gr.Textbox(label="Or type how you're feeling", placeholder="I've been feeling...")
            language = gr.Dropdown(choices=LANGUAGES, label="Language", value="en")
            
            # Hidden inputs for user data
            username_state = gr.Textbox(visible=False)
            email_state = gr.Textbox(visible=False)
            
            submit_btn = gr.Button("Get Response")
            
            with gr.Row():
                user_query = gr.Textbox(label="Your Thoughts", interactive=False)
                therapist_response = gr.Textbox(label="Therapist's Response", interactive=False)
                voice_output = gr.Audio(label="Voice Response", autoplay=True)
        
        def handle_login(username, email):
            if not username or not email:
                return {status: "Username and email are required", auth_state: auth_state.value}
            
            new_state = {
                "authenticated": True,
                "username": username,
                "email": email
            }
            
            log_activity(username, email, "User logged in")
            
            return {
                status: "Login successful!",
                login_col: gr.Column(visible=False),
                main_col: gr.Column(visible=True),
                username_state: username,
                email_state: email,
                auth_state: new_state
            }
        
        login_btn.click(
            handle_login,
            inputs=[username, email],
            outputs=[status, login_col, main_col, username_state, email_state, auth_state]
        )
        
        submit_btn.click(
            process_inputs,
            inputs=[audio_input, image_input, text_input, language, username_state, email_state],
            outputs=[user_query, therapist_response, voice_output]
        )
    
    app.launch(share=True)

if __name__ == "__main__":
    launch_app()