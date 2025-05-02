from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
import json
import markdown
from .utils.gemini_api import get_content_suggestions, get_title_suggestions
from django.contrib.auth.decorators import login_required

@login_required
@csrf_protect
@require_POST
def api_title_suggestions(request):
    print(1)
    try:
        data = json.loads(request.body)
        content = data.get('content', '')
        
        if not content:
            return JsonResponse({'error': 'Content is required'}, status=400)
        
        suggestions_md = get_title_suggestions(content)
        # Convert markdown to HTML
        suggestions_html = markdown.markdown(suggestions_md)
        return JsonResponse({'suggestions': suggestions_html})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@csrf_protect
@require_POST
def api_content_suggestions(request):
    print(2)
    try:
        data = json.loads(request.body)
        content = data.get('content', '')
        print(content)
        
        if not content:
            return JsonResponse({'error': 'Content is required'}, status=400)
        
        suggestions_md = get_content_suggestions(content)
        # Convert markdown to HTML
        suggestions_html = markdown.markdown(suggestions_md)
        return JsonResponse({'suggestions': suggestions_html})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)