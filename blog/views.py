import json

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import get_language

from blog.models import *
from core.translation_hooks import trigger_auto_translate
from home.utils import download_image_to_field
from sampleconversations.models import BlogSampleConversation
from sampleconversations.utils import build_whatsapp_text

def blogPageFront(request):
    categories = blogCategory.objects.all().order_by('?')
    blogs_list = Blogs.objects.all().order_by('-created_at')

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        blogs_list = blogs_list.filter(title__icontains=search_query)

    # Pagination
    paginator = Paginator(blogs_list, 6)
    page = request.GET.get('page')
    blogs = paginator.get_page(page)

    context = {
        'title': 'Blogs',
        'blogs': blogs,
        'categories': categories,
    }
    return render(request, 'front/main/blog.html', context)

def blogDetails(request, slug):
    blog = get_object_or_404(Blogs, slug=slug)
    blogs = Blogs.objects.all().order_by('-created_at')
    categories = blogCategory.objects.all().order_by('?')
    sample_conversation = BlogSampleConversation.objects.filter(blog=blog).first()
    sample_conversation_entries = []
    if sample_conversation:
        lang = (get_language() or "").lower()
        if lang.startswith("tr") and sample_conversation.conversations_tr:
            sample_conversation_entries = sample_conversation.conversations_tr
        elif lang.startswith("en") and sample_conversation.conversations_en:
            sample_conversation_entries = sample_conversation.conversations_en
        elif sample_conversation.conversations:
            sample_conversation_entries = sample_conversation.conversations
        elif sample_conversation.conversations_en:
            # Fallback to English if default is empty.
            sample_conversation_entries = sample_conversation.conversations_en
    sample_conversation_whatsapp = None
    if sample_conversation_entries:
        author_name = blog.author or "Author"
        sample_conversation_whatsapp = build_whatsapp_text(
            sample_conversation_entries,
            user_name=author_name,
            assistant_name="Assistant",
        )

    context = {
        'blog': blog,
        'blogs' : blogs,
        'categories' : categories,
        'blog_sample_conversation': sample_conversation,
        'blog_sample_conversation_entries': sample_conversation_entries,
        'blog_sample_conversation_whatsapp': sample_conversation_whatsapp,
    }
    return render(request, 'front/main/partial/blog-details.html', context)

def blogsByCategory(request, category_slug):
    categories = blogCategory.objects.all().order_by('?')
    category = get_object_or_404(blogCategory, slug=category_slug)
    blogs_list = Blogs.objects.filter(category=category).order_by('-created_at')

    # Pagination
    paginator = Paginator(blogs_list, 6)
    page = request.GET.get('page')
    blogs = paginator.get_page(page)

    context = {
        'title': category.title,
        'blogs': blogs,
        'category': category,
        'categories' : categories,
    }
    return render(request, 'front/main/partial/blog_category.html', context)

def error_404(request, exception):
    return render(request, 'error/404.html', status=404)


def serialize_blog_category(cat):
    return {
        'id': cat.id,
        'title': cat.title,
        'slug': cat.slug,
    }


def serialize_blog(blog):
    return {
        'id': blog.id,
        'title': blog.title,
        'slug': blog.slug,
        'description': blog.description,
        'author': blog.author,
        'category': serialize_blog_category(blog.category) if blog.category else None,
        'thumbnail': blog.thumbnail.url if blog.thumbnail else None,
        'created_at': blog.created_at.isoformat() if blog.created_at else None,
        'updated_at': blog.updated_at.isoformat() if blog.updated_at else None,
    }


@csrf_exempt
def api_blog_categories(request):
    if request.method == 'GET':
        cat_id = request.GET.get('id')
        search = request.GET.get('search')

        if cat_id:
            try:
                cat = blogCategory.objects.get(pk=int(cat_id))
            except (ValueError, blogCategory.DoesNotExist):
                return JsonResponse({'detail': 'Category not found'}, status=404)
            return JsonResponse(serialize_blog_category(cat), status=200)

        qs = blogCategory.objects.all()
        if search:
            qs = qs.filter(title__icontains=search)

        data = [serialize_blog_category(c) for c in qs]
        return JsonResponse({'count': len(data), 'items': data}, status=200)

    if request.method not in ['POST', 'PATCH', 'PUT']:
        return JsonResponse({'detail': 'Method not allowed'}, status=405)

    payload = {}
    if request.content_type and 'application/json' in request.content_type:
        try:
            payload = json.loads(request.body.decode() or "{}")
        except json.JSONDecodeError:
            return JsonResponse({'detail': 'Invalid JSON payload'}, status=400)
    else:
        payload = request.POST

    if request.method == 'POST':
        title = payload.get('title')
        if not title:
            return JsonResponse({'detail': 'title is required'}, status=400)

        cat = blogCategory(title=title)
        cat.save()
        trigger_auto_translate('blog.blogcategory', cat.id)
        return JsonResponse(serialize_blog_category(cat), status=201)

    cat_id = request.GET.get('id')
    if not cat_id:
        return JsonResponse({'detail': 'id is required for update'}, status=400)
    try:
        cat = blogCategory.objects.get(pk=int(cat_id))
    except (ValueError, blogCategory.DoesNotExist):
        return JsonResponse({'detail': 'Category not found'}, status=404)

    if 'title' in payload:
        cat.title = payload.get('title')

    cat.save()
    trigger_auto_translate('blog.blogcategory', cat.id)
    return JsonResponse(serialize_blog_category(cat), status=200)


@csrf_exempt
def api_blogs(request):
    if request.method == 'GET':
        blog_id = request.GET.get('id')
        search = request.GET.get('search')
        category_id = request.GET.get('category')

        if blog_id:
            try:
                blog = Blogs.objects.select_related('category').get(pk=int(blog_id))
            except (ValueError, Blogs.DoesNotExist):
                return JsonResponse({'detail': 'Blog not found'}, status=404)
            return JsonResponse(serialize_blog(blog), status=200)

        qs = Blogs.objects.select_related('category').all()
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(description__icontains=search))
        if category_id:
            try:
                qs = qs.filter(category__id=int(category_id))
            except ValueError:
                return JsonResponse({'detail': 'Invalid category'}, status=400)

        data = [serialize_blog(b) for b in qs]
        return JsonResponse({'count': len(data), 'items': data}, status=200)

    if request.method not in ['POST', 'PATCH', 'PUT']:
        return JsonResponse({'detail': 'Method not allowed'}, status=405)

    payload = {}
    files = request.FILES
    if request.content_type and 'application/json' in request.content_type:
        try:
            payload = json.loads(request.body.decode() or "{}")
        except json.JSONDecodeError:
            return JsonResponse({'detail': 'Invalid JSON payload'}, status=400)
    else:
        payload = request.POST

    if request.method == 'POST':
        title = payload.get('title')
        if not title:
            return JsonResponse({'detail': 'title is required'}, status=400)

        blog = Blogs(
            title=title,
            author=payload.get('author'),
            description=payload.get('description'),
        )

        cat_id = payload.get('category_id')
        if cat_id:
            try:
                blog.category = blogCategory.objects.get(pk=int(cat_id))
            except (ValueError, blogCategory.DoesNotExist):
                return JsonResponse({'detail': 'category_id not found'}, status=400)

        if files.get('thumbnail'):
            blog.thumbnail = files['thumbnail']
        else:
            image_url = payload.get('thumbnail_url')
            if image_url:
                ok, msg = download_image_to_field(image_url, blog, 'thumbnail')
                if not ok:
                    return JsonResponse({'detail': msg}, status=400)

        blog.save()
        trigger_auto_translate('blog.blogs', blog.id)
        return JsonResponse(serialize_blog(blog), status=201)

    blog_id = request.GET.get('id')
    if not blog_id:
        return JsonResponse({'detail': 'id is required for update'}, status=400)
    try:
        blog = Blogs.objects.select_related('category').get(pk=int(blog_id))
    except (ValueError, Blogs.DoesNotExist):
        return JsonResponse({'detail': 'Blog not found'}, status=404)

    for field in ['title', 'author', 'description']:
        if field in payload:
            setattr(blog, field, payload.get(field))

    cat_id = payload.get('category_id')
    if cat_id is not None:
        if cat_id == '' or cat_id is None:
            blog.category = None
        else:
            try:
                blog.category = blogCategory.objects.get(pk=int(cat_id))
            except (ValueError, blogCategory.DoesNotExist):
                return JsonResponse({'detail': 'category_id not found'}, status=400)

    if files.get('thumbnail'):
        blog.thumbnail = files['thumbnail']
    else:
        image_url = payload.get('thumbnail_url')
        if image_url:
            ok, msg = download_image_to_field(image_url, blog, 'thumbnail')
            if not ok:
                return JsonResponse({'detail': msg}, status=400)

    blog.save()
    trigger_auto_translate('blog.blogs', blog.id)
    return JsonResponse(serialize_blog(blog), status=200)
