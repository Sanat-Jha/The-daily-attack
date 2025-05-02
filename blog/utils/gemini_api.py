import google.generativeai as genai
import os

# Configure the Gemini API with your API key
genai.configure(api_key="AIzaSyDLG7ztyXuVWaH-mcm2HrSLHCgJU8arjvg")

def get_content_suggestions(content):
    """
    Get content improvement suggestions from Gemini API
    """
    try:
        # Use the correct model name
        model = genai.GenerativeModel('gemini-2.0-flash-lite-preview')
        prompt = f"""
        Please analyze the following blog post content and provide 3-5 specific suggestions 
        to improve it. Focus on clarity, engagement, and readability:
        
        {content}
        
        Format your response as a bulleted list of actionable suggestions.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error getting content suggestions: {str(e)}"

def get_title_suggestions(content):
    print(list_available_models())
    """
    Generate title suggestions based on the content
    """
    try:
        # Use the correct model name
        model = genai.GenerativeModel('gemini-2.0-flash-lite-preview')
        prompt = f"""
        Based on the following blog post content, suggest 5 engaging and SEO-friendly title options:
        
        {content}
        
        Format your response as a numbered list of title suggestions.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error getting title suggestions: {str(e)}"

def list_available_models():
    """
    List all available models from the Gemini API
    """
    try:
        models = genai.list_models()
        return [model.name for model in models]
    except Exception as e:
        return f"Error listing models: {str(e)}"