import json
import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from groq import Groq

# Initialise Groq client once at import time
client = Groq(api_key=settings.GROQ_API_KEY)


def fetch_financial_news(query):
    """Fetch real-time financial news from NewsAPI based on the user's query."""
    api_key = getattr(settings, 'NEWS_API_KEY', None)
    if not api_key:
        return "No news API key configured."

    keywords   = " ".join([w for w in query.split() if len(w) > 3])
    search_term = keywords if keywords else "bitcoin price"

    url = (
        f"https://newsapi.org/v2/everything"
        f"?q={search_term}&language=en&pageSize=20&sortBy=publishedAt&apikey={api_key}"
    )

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        articles = resp.json().get('articles', [])

        if not articles:
            return f"No recent news found for '{search_term}'."

        news_context = "Recent News Highlights:\n"
        for i, article in enumerate(articles, 1):
            news_context += (
                f"ARTICLE {i}:\n"
                f"TITLE: {article.get('title')}\n"
                f"SUMMARY: {article.get('description')}\n"
                f"SOURCE: {article.get('source', {}).get('name')}\n"
                f"URL: {article.get('url')}\n\n"
            )
        return news_context

    except Exception as e:
        return f"Error fetching news: {str(e)}"


def fetch_groq_explanation(user_query, news_context):
    """Send the query + news context to Groq and return the AI analysis."""
    system_prompt = (
        "You are a professional, highly analytical financial AI assistant. "
        "You MUST follow these strict rules:\n"
        "1. You MUST only use the provided articles.\n"
        "2. Each article is labeled as ARTICLE 1, ARTICLE 2, etc.\n"
        "3. When referencing, you MUST use [1], [2], etc (matching ARTICLE numbers).\n"
        "4. You MUST NOT invent numbers like [7] or [25].\n"
        "5. You MUST include ALL referenced articles in the Sources section.\n"
        "6. You MUST include article title, source name, and full URL.\n\n"
        "FINAL OUTPUT FORMAT:\n"
        "Answer...\n\n"
        "Sources:\n"
        "[1] Title - Source Name - URL\n"
        "Do NOT predict future prices. Only analyze based on provided data."
    )
    user_prompt = (
        f"Here is recent financial news:\n\n{news_context}\n\n"
        f"User question: {user_query}\n\n"
        "Answer using ONLY these articles. Cite using [ARTICLE NUMBER]. "
        "At the end, list ALL used sources with title, source name, and URL."
    )

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt},
            ],
            temperature=0.3,
            max_tokens=1000,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error connecting to Groq service: {str(e)}"


@api_view(['POST'])
def ask_ai(request):
    """
    POST /ai/ask/
    Body: { message: string }
    Returns: { status: 'success', response: string }

    No auth required — the AI chat is public.
    CSRF is handled by DRF's JWT mechanism (not Django's session CSRF).
    """
    user_message = request.data.get('message', '').strip()
    if not user_message:
        return Response({'status': 'error', 'message': 'No message provided.'}, status=400)

    news_context = fetch_financial_news(user_message)
    ai_response  = fetch_groq_explanation(user_message, news_context)

    return Response({'status': 'success', 'response': ai_response})
