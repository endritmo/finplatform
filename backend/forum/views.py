from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Category, Thread, Reply


def serialize_thread(t, short=True):
    """Convert a Thread instance to a JSON-serialisable dict."""
    d = {
        'id':         t.id,
        'title':      t.title,
        'author':     t.author.username,
        'symbol':     t.symbol,
        'category':   {'name': t.category.name, 'slug': t.category.slug} if t.category else None,
        'is_pinned':  t.is_pinned,
        'is_locked':  t.is_locked,
        'reply_count': t.reply_count,
        'created_at': t.created_at.isoformat(),
        'updated_at': t.updated_at.isoformat(),
    }
    if short:
        d['content'] = t.content[:120]
    else:
        d['content'] = t.content
    return d


def serialize_reply(r):
    return {
        'id':         r.id,
        'content':    r.content,
        'author':     r.author.username,
        'created_at': r.created_at.isoformat(),
        'updated_at': r.updated_at.isoformat(),
        'thread_id':  r.thread_id,
    }


# ── Threads ────────────────────────────────────────────────────────────────────

@api_view(['GET'])
def thread_list(request):
    """GET /api/forum/threads/ — List all threads (public)."""
    qs = Thread.objects.all().order_by('-is_pinned', '-updated_at')

    category_slug = request.GET.get('category')
    symbol_query  = request.GET.get('symbol')
    if category_slug:
        qs = qs.filter(category__slug=category_slug)
    if symbol_query:
        qs = qs.filter(symbol__icontains=symbol_query)

    categories = list(Category.objects.values('name', 'slug'))
    return Response({
        'threads':          [serialize_thread(t) for t in qs],
        'categories':       categories,
        'current_category': category_slug,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def thread_create(request):
    """POST /api/forum/threads/ — Create a new thread (auth required)."""
    title    = request.data.get('title', '').strip()
    content  = request.data.get('content', '').strip()
    symbol   = request.data.get('symbol', '').strip()
    category_slug = request.data.get('category', '')

    if not title or not content:
        return Response({'error': 'Title and content are required.'}, status=400)

    category = None
    if category_slug:
        category = Category.objects.filter(slug=category_slug).first()

    thread = Thread.objects.create(
        title=title, content=content, symbol=symbol,
        category=category, author=request.user,
    )
    return Response(serialize_thread(thread, short=False), status=201)


@api_view(['GET'])
def thread_detail(request, pk):
    """GET /api/forum/threads/<pk>/ — Single thread with replies (public)."""
    thread  = get_object_or_404(Thread, pk=pk)
    replies = thread.replies.all().order_by('created_at')
    return Response({
        'thread':  serialize_thread(thread, short=False),
        'replies': [serialize_reply(r) for r in replies],
    })


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def thread_edit(request, pk):
    """PUT /api/forum/threads/<pk>/edit/ — Edit own thread (auth required)."""
    thread = get_object_or_404(Thread, pk=pk)
    if request.user != thread.author:
        return Response({'error': 'Permission denied.'}, status=403)

    thread.title   = request.data.get('title',   thread.title)
    thread.content = request.data.get('content', thread.content)
    thread.symbol  = request.data.get('symbol',  thread.symbol)
    thread.save()
    return Response(serialize_thread(thread, short=False))


# ── Replies ────────────────────────────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reply_create(request, thread_pk):
    """POST /api/forum/threads/<thread_pk>/replies/ — Post a reply."""
    thread = get_object_or_404(Thread, pk=thread_pk)
    if thread.is_locked:
        return Response({'error': 'This thread is locked.'}, status=403)

    content = request.data.get('content', '').strip()
    if not content:
        return Response({'error': 'Reply content cannot be empty.'}, status=400)

    reply = Reply.objects.create(thread=thread, author=request.user, content=content)
    thread.save()  # bump updated_at so the thread surfaces in the list
    return Response(serialize_reply(reply), status=201)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def reply_edit(request, pk):
    """PUT /api/forum/replies/<pk>/edit/ — Edit own reply."""
    reply = get_object_or_404(Reply, pk=pk)
    if request.user != reply.author:
        return Response({'error': 'Permission denied.'}, status=403)

    reply.content = request.data.get('content', reply.content)
    reply.save()
    return Response(serialize_reply(reply))


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def reply_delete(request, pk):
    """DELETE /api/forum/replies/<pk>/ — Delete own reply."""
    reply = get_object_or_404(Reply, pk=pk)
    if request.user != reply.author:
        return Response({'error': 'Permission denied.'}, status=403)

    thread_pk = reply.thread_id
    reply.delete()
    return Response({'message': 'Reply deleted.', 'thread_id': thread_pk})
