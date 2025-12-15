import json
import os

import requests
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)


def _openai_headers():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


@csrf_exempt
def ai_enrich(request):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")

    try:
        payload = json.loads(request.body.decode() or "{}")
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    text = (payload.get("text") or "").strip()
    instruction = (payload.get("instruction") or "Improve clarity and tone without changing meaning.").strip()
    if not text:
        return HttpResponseBadRequest("text is required")

    logger.debug(
        "ai_enrich received request: instruction=%s text_len=%d preview=%r",
        instruction,
        len(text),
        text[:120],
    )

    headers = _openai_headers()
    if not headers:
        return JsonResponse({"error": "OPENAI_API_KEY missing"}, status=500)

    body = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a concise copy editor. Return only the improved text."},
            {"role": "user", "content": f"Instruction: {instruction}\n\nText:\n{text}"},
        ],
        "temperature": 0.3,
        "max_tokens": 600,
    }

    try:
        resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=body, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        improved = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        logger.debug(
            "ai_enrich response: improved_len=%d preview=%r",
            len(improved or text),
            (improved or text)[:120],
        )
    except Exception as exc:
        logging.exception("AI enrich failed")
        return JsonResponse({"error": str(exc)}, status=502)

    return JsonResponse({"enhanced_text": improved or text})
