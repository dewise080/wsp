import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.urls import reverse
from home.utils import download_image_to_field
from home.models import *
from pricing.models import pricingSection
from about.models import teamSection
from blog.models import *
from settings.models import templateSettings
from analytics.views import visitor_data
from core.translation_hooks import trigger_auto_translate
# ===============> Front Home Page View <===============

def homePageFront(request):
    visitor_data(request)
    
    meta = homePageSEO.objects.first()
    sliders = sliderSection.objects.all()
    services = serviceSection.objects.all()
    about = aboutSection.objects.first()
    funfacts = funFactSection.objects.all()
    project_categories= projectCategory.objects.all()
    projects = projectSection.objects.all().order_by('?')
    clients = clientSection.objects.all()
    testimonials = testimonialsSection.objects.all()
    pricings = pricingSection.objects.all()
    teams = teamSection.objects.all()
    blogs = Blogs.objects.all().order_by('?')
    
    template_settings = templateSettings.objects.first()
    
    if not template_settings:
        template_settings = templateSettings.objects.create(template1=True)

    context = {
        'meta' : meta,
        'sliders' : sliders,
        'services' : services,
        'about' : about,
        'funfacts' : funfacts,
        'project_categories' : project_categories,
        'projects': projects,
        'clients' : clients,
        'testimonials' : testimonials,
        'pricings' : pricings,
        'teams' : teams,
        'blogs' : blogs,
    }
   
    
    if template_settings.template1 == True:
        return render(request, 'front/main/index.html', context)
    elif template_settings.template2 == True:
        return render(request, 'front/main/home2.html', context)
    else:
        return render(request, 'front/main/index.html', context)

def serialize_service(service):
    return {
        'id': service.id,
        'name': service.name,
        'slug': service.slug,
        'short_description': service.short_description,
        'fontawesome_icon_class': service.fontawesome_icon_class,
        'detail_page_description': service.detail_page_description,
        'show_call_now_widget': True,
        'detail_page_image': service.detail_page_image.url if service.detail_page_image else None,
    }

def serialize_testimonial(testimonial):
    return {
        'id': testimonial.id,
        'name': testimonial.name,
        'position': testimonial.position,
        'description': testimonial.description,
        'star': testimonial.star,
        'image': testimonial.image.url if getattr(testimonial, "image", None) else None,
    }

def serialize_about(about):
    return {
        'id': about.id,
        'subtitle': about.subtitle,
        'title': about.title,
        'short_description': about.short_description,
        'long_description': about.long_description,
        'ranking_number': about.ranking_number,
        'tag_line': about.tag_line,
        'experience': about.experience,
        'video_url': about.video_url,
        'image': about.image.url if about.image else None,
        'video_thumbnail': about.video_thumbnail.url if about.video_thumbnail else None,
    }

def serialize_funfact(fact):
    return {
        'id': fact.id,
        'fontawesome_icon_class': fact.fontawesome_icon_class,
        'count': fact.count,
        'count_after': fact.count_after,
        'title': fact.title,
    }

def serialize_client(client):
    return {
        'id': client.id,
        'client_name': client.client_name,
        'image': client.image.url if client.image else None,
    }

@csrf_exempt
def api_services(request):
    if request.method == 'GET':
        service_id = request.GET.get('id')
        search = request.GET.get('search')

        if service_id:
            try:
                service = serviceSection.objects.get(pk=int(service_id))
            except (ValueError, serviceSection.DoesNotExist):
                return JsonResponse({'detail': 'Service not found'}, status=404)
            return JsonResponse(serialize_service(service), status=200)

        qs = serviceSection.objects.all()
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(short_description__icontains=search))

        data = [serialize_service(s) for s in qs]
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
        name = payload.get('name')
        if not name:
            return JsonResponse({'detail': 'name is required'}, status=400)

        service = serviceSection(
            name=name,
            short_description=payload.get('short_description'),
            fontawesome_icon_class=payload.get('fontawesome_icon_class'),
            detail_page_description=payload.get('detail_page_description'),
            show_call_now_widget=True,
        )

        if request.FILES.get('detail_page_image'):
            service.detail_page_image = request.FILES['detail_page_image']
        else:
            image_url = payload.get('detail_page_image_url')
            if image_url:
                ok, msg = download_image_to_field(image_url, service, 'detail_page_image')
                if not ok:
                    return JsonResponse({'detail': msg}, status=400)

        service.save()
        trigger_auto_translate('home.servicesection', service.id)
        return JsonResponse(serialize_service(service), status=201)

    # PATCH/PUT update
    service_id = request.GET.get('id')
    if not service_id:
        return JsonResponse({'detail': 'id is required for update'}, status=400)
    try:
        service = serviceSection.objects.get(pk=int(service_id))
    except (ValueError, serviceSection.DoesNotExist):
        return JsonResponse({'detail': 'Service not found'}, status=404)

    for field in ['name', 'short_description', 'fontawesome_icon_class', 'detail_page_description']:
        if field in payload:
            setattr(service, field, payload.get(field))

    if request.FILES.get('detail_page_image'):
        service.detail_page_image = request.FILES['detail_page_image']
    else:
        image_url = payload.get('detail_page_image_url')
        if image_url:
            ok, msg = download_image_to_field(image_url, service, 'detail_page_image')
            if not ok:
                return JsonResponse({'detail': msg}, status=400)

    service.save()
    trigger_auto_translate('home.servicesection', service.id)
    return JsonResponse(serialize_service(service), status=200)

@csrf_exempt
def api_testimonials(request):
    if request.method == 'GET':
        testimonial_id = request.GET.get('id')
        if testimonial_id:
            try:
                testimonial = testimonialsSection.objects.get(pk=int(testimonial_id))
            except (ValueError, testimonialsSection.DoesNotExist):
                return JsonResponse({'detail': 'Testimonial not found'}, status=404)
            return JsonResponse(serialize_testimonial(testimonial), status=200)

        data = [serialize_testimonial(t) for t in testimonialsSection.objects.all()]
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
        name = payload.get('name')
        if not name:
            return JsonResponse({'detail': 'name is required'}, status=400)
        testimonial = testimonialsSection(
            name=name,
            position=payload.get('position'),
            description=payload.get('description'),
        )
        star_val = payload.get('star')
        if star_val not in [None, '']:
            try:
                testimonial.star = int(star_val)
            except (TypeError, ValueError):
                return JsonResponse({'detail': 'star must be an integer'}, status=400)
        testimonial.save()
        trigger_auto_translate('home.testimonialssection', testimonial.id)
        return JsonResponse(serialize_testimonial(testimonial), status=201)

    testimonial_id = request.GET.get('id')
    if not testimonial_id:
        return JsonResponse({'detail': 'id is required for update'}, status=400)
    try:
        testimonial = testimonialsSection.objects.get(pk=int(testimonial_id))
    except (ValueError, testimonialsSection.DoesNotExist):
        return JsonResponse({'detail': 'Testimonial not found'}, status=404)

    for field in ['name', 'position', 'description']:
        if field in payload:
            setattr(testimonial, field, payload.get(field))

    if 'star' in payload:
        try:
            testimonial.star = int(payload.get('star'))
        except (TypeError, ValueError):
            return JsonResponse({'detail': 'star must be an integer'}, status=400)

    testimonial.save()
    trigger_auto_translate('home.testimonialssection', testimonial.id)
    return JsonResponse(serialize_testimonial(testimonial), status=200)

@csrf_exempt
def api_about(request):
    if request.method == 'GET':
        about_id = request.GET.get('id')
        if about_id:
            try:
                about = aboutSection.objects.get(pk=int(about_id))
            except (ValueError, aboutSection.DoesNotExist):
                return JsonResponse({'detail': 'About not found'}, status=404)
            return JsonResponse(serialize_about(about), status=200)

        data = [serialize_about(a) for a in aboutSection.objects.all()]
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
        about = aboutSection.objects.create(
            subtitle=payload.get('subtitle'),
            title=payload.get('title'),
            short_description=payload.get('short_description'),
            long_description=payload.get('long_description'),
            ranking_number=payload.get('ranking_number'),
            tag_line=payload.get('tag_line'),
            experience=payload.get('experience'),
            video_url=payload.get('video_url'),
        )
        trigger_auto_translate('home.aboutsection', about.id)
        return JsonResponse(serialize_about(about), status=201)

    about_id = request.GET.get('id')
    if not about_id:
        return JsonResponse({'detail': 'id is required for update'}, status=400)
    try:
        about = aboutSection.objects.get(pk=int(about_id))
    except (ValueError, aboutSection.DoesNotExist):
        return JsonResponse({'detail': 'About not found'}, status=404)

    for field in ['subtitle', 'title', 'short_description', 'long_description', 'tag_line', 'experience', 'video_url']:
        if field in payload:
            setattr(about, field, payload.get(field))

    if 'ranking_number' in payload:
        try:
            about.ranking_number = int(payload.get('ranking_number')) if payload.get('ranking_number') not in (None, '') else None
        except (TypeError, ValueError):
            return JsonResponse({'detail': 'ranking_number must be an integer'}, status=400)

    about.save()
    trigger_auto_translate('home.aboutsection', about.id)
    return JsonResponse(serialize_about(about), status=200)

@csrf_exempt
def api_funfacts(request):
    if request.method == 'GET':
        fact_id = request.GET.get('id')
        if fact_id:
            try:
                fact = funFactSection.objects.get(pk=int(fact_id))
            except (ValueError, funFactSection.DoesNotExist):
                return JsonResponse({'detail': 'Fun fact not found'}, status=404)
            return JsonResponse(serialize_funfact(fact), status=200)

        data = [serialize_funfact(f) for f in funFactSection.objects.all()]
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
        fact = funFactSection.objects.create(
            fontawesome_icon_class=payload.get('fontawesome_icon_class'),
            count=payload.get('count') or None,
            count_after=payload.get('count_after'),
            title=payload.get('title'),
        )
        trigger_auto_translate('home.funfactsection', fact.id)
        return JsonResponse(serialize_funfact(fact), status=201)

    fact_id = request.GET.get('id')
    if not fact_id:
        return JsonResponse({'detail': 'id is required for update'}, status=400)
    try:
        fact = funFactSection.objects.get(pk=int(fact_id))
    except (ValueError, funFactSection.DoesNotExist):
        return JsonResponse({'detail': 'Fun fact not found'}, status=404)

    if 'fontawesome_icon_class' in payload:
        fact.fontawesome_icon_class = payload.get('fontawesome_icon_class')
    if 'count' in payload:
        try:
            fact.count = int(payload.get('count')) if payload.get('count') not in (None, '') else None
        except (TypeError, ValueError):
            return JsonResponse({'detail': 'count must be an integer'}, status=400)
    if 'count_after' in payload:
        fact.count_after = payload.get('count_after')
    if 'title' in payload:
        fact.title = payload.get('title')

    fact.save()
    trigger_auto_translate('home.funfactsection', fact.id)
    return JsonResponse(serialize_funfact(fact), status=200)

@csrf_exempt
def api_clients(request):
    if request.method == 'GET':
        client_id = request.GET.get('id')
        if client_id:
            try:
                client = clientSection.objects.get(pk=int(client_id))
            except (ValueError, clientSection.DoesNotExist):
                return JsonResponse({'detail': 'Client not found'}, status=404)
            return JsonResponse(serialize_client(client), status=200)

        data = [serialize_client(c) for c in clientSection.objects.all()]
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
        client = clientSection(client_name=payload.get('client_name'))
        if files.get('image'):
            client.image = files['image']
        client.save()
        trigger_auto_translate('home.clientsection', client.id)
        return JsonResponse(serialize_client(client), status=201)

    client_id = request.GET.get('id')
    if not client_id:
        return JsonResponse({'detail': 'id is required for update'}, status=400)
    try:
        client = clientSection.objects.get(pk=int(client_id))
    except (ValueError, clientSection.DoesNotExist):
        return JsonResponse({'detail': 'Client not found'}, status=404)

    if 'client_name' in payload:
        client.client_name = payload.get('client_name')
    if files.get('image'):
        client.image = files['image']

    client.save()
    trigger_auto_translate('home.clientsection', client.id)
    return JsonResponse(serialize_client(client), status=200)

def serialize_project_category(cat):
    return {
        'id': cat.id,
        'name': cat.name,
        'slug': cat.slug,
    }

def serialize_project(project):
    return {
        'id': project.id,
        'title': project.title,
        'slug': project.slug,
        'description': project.description,
        'client': project.client,
        'company': project.company,
        'duration': project.duration,
        'category': serialize_project_category(project.category) if project.category else None,
        'image': project.image.url if project.image else None,
    }

@csrf_exempt
def api_project_categories(request):
    if request.method == 'GET':
        cat_id = request.GET.get('id')
        search = request.GET.get('search')

        if cat_id:
            try:
                cat = projectCategory.objects.get(pk=int(cat_id))
            except (ValueError, projectCategory.DoesNotExist):
                return JsonResponse({'detail': 'Category not found'}, status=404)
            return JsonResponse(serialize_project_category(cat), status=200)

        qs = projectCategory.objects.all()
        if search:
            qs = qs.filter(name__icontains=search)

        data = [serialize_project_category(c) for c in qs]
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
        name = payload.get('name')
        if not name:
            return JsonResponse({'detail': 'name is required'}, status=400)

        cat = projectCategory(name=name)
        cat.save()
        trigger_auto_translate('home.projectcategory', cat.id)
        return JsonResponse(serialize_project_category(cat), status=201)

    cat_id = request.GET.get('id')
    if not cat_id:
        return JsonResponse({'detail': 'id is required for update'}, status=400)
    try:
        cat = projectCategory.objects.get(pk=int(cat_id))
    except (ValueError, projectCategory.DoesNotExist):
        return JsonResponse({'detail': 'Category not found'}, status=404)

    if 'name' in payload:
        cat.name = payload.get('name')

    cat.save()
    trigger_auto_translate('home.projectcategory', cat.id)
    return JsonResponse(serialize_project_category(cat), status=200)

@csrf_exempt
def api_projects(request):
    if request.method == 'GET':
        proj_id = request.GET.get('id')
        search = request.GET.get('search')
        category_id = request.GET.get('category')

        if proj_id:
            try:
                proj = projectSection.objects.select_related('category').get(pk=int(proj_id))
            except (ValueError, projectSection.DoesNotExist):
                return JsonResponse({'detail': 'Project not found'}, status=404)
            return JsonResponse(serialize_project(proj), status=200)

        qs = projectSection.objects.select_related('category').all()
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(description__icontains=search))
        if category_id:
            try:
                qs = qs.filter(category__id=int(category_id))
            except ValueError:
                return JsonResponse({'detail': 'Invalid category'}, status=400)

        data = [serialize_project(p) for p in qs]
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

        proj = projectSection(
            title=title,
            description=payload.get('description'),
            client=payload.get('client'),
            company=payload.get('company'),
            duration=payload.get('duration'),
        )

        cat_id = payload.get('category_id')
        if cat_id:
            try:
                proj.category = projectCategory.objects.get(pk=int(cat_id))
            except (ValueError, projectCategory.DoesNotExist):
                return JsonResponse({'detail': 'category_id not found'}, status=400)

        if files.get('image'):
            proj.image = files['image']
        else:
            image_url = payload.get('image_url')
            if image_url:
                ok, msg = download_image_to_field(image_url, proj, 'image')
                if not ok:
                    return JsonResponse({'detail': msg}, status=400)

        proj.save()
        trigger_auto_translate('home.projectsection', proj.id)
        return JsonResponse(serialize_project(proj), status=201)

    proj_id = request.GET.get('id')
    if not proj_id:
        return JsonResponse({'detail': 'id is required for update'}, status=400)
    try:
        proj = projectSection.objects.select_related('category').get(pk=int(proj_id))
    except (ValueError, projectSection.DoesNotExist):
        return JsonResponse({'detail': 'Project not found'}, status=404)

    for field in ['title', 'description', 'client', 'company', 'duration']:
        if field in payload:
            setattr(proj, field, payload.get(field))

    cat_id = payload.get('category_id')
    if cat_id is not None:
        if cat_id == '' or cat_id is None:
            proj.category = None
        else:
            try:
                proj.category = projectCategory.objects.get(pk=int(cat_id))
            except (ValueError, projectCategory.DoesNotExist):
                return JsonResponse({'detail': 'category_id not found'}, status=400)

    if files.get('image'):
        proj.image = files['image']
    else:
        image_url = payload.get('image_url')
        if image_url:
            ok, msg = download_image_to_field(image_url, proj, 'image')
            if not ok:
                return JsonResponse({'detail': msg}, status=400)

    proj.save()
    trigger_auto_translate('home.projectsection', proj.id)
    return JsonResponse(serialize_project(proj), status=200)

def openapi_json(request):
    """
    Minimal OpenAPI 3.1 schema describing the service creation endpoint.
    """
    # Prefer Origin header for correct scheme (e.g., https). Also honor proxy headers for host/port/scheme.
    origin = request.headers.get("Origin")
    forwarded_proto = request.headers.get("X-Forwarded-Proto", "").split(",")[0].strip().lower()
    forwarded_host = request.headers.get("X-Forwarded-Host", "").split(",")[0].strip()
    forwarded_port = request.headers.get("X-Forwarded-Port", "").split(",")[0].strip()
    host = forwarded_host or request.get_host()

    if forwarded_port and ":" not in host and forwarded_port not in ("80", "443"):
        host = f"{host}:{forwarded_port}"

    if origin:
        server_url = origin.rstrip("/")
    else:
        known_https_hosts = {"wsp.whatsynaptic.tech", "automate.beyondclinic.online", "www.automate.beyondclinic.online"}
        if forwarded_proto:
            scheme = forwarded_proto
        elif request.is_secure() or host in known_https_hosts:
            scheme = "https"
        else:
            scheme = request.scheme
        server_url = f"{scheme}://{host}"

    bad_request = {"$ref": "#/components/responses/BadRequest"}
    not_found = {"$ref": "#/components/responses/NotFound"}
    method_not_allowed = {"$ref": "#/components/responses/MethodNotAllowed"}
    id_param = {
        "in": "query",
        "name": "id",
        "schema": {"type": "integer"},
        "required": False,
        "description": "Optional primary key used by list endpoints to fetch a single record.",
    }
    search_param = {
        "in": "query",
        "name": "search",
        "schema": {"type": "string"},
        "required": False,
        "description": "Case-insensitive search term.",
    }
    category_param = {
        "in": "query",
        "name": "category",
        "schema": {"type": "integer"},
        "required": False,
        "description": "Filter by category ID where supported.",
    }
    blog_param = {
        "in": "query",
        "name": "blog",
        "schema": {"type": "integer"},
        "required": False,
        "description": "Filter by blog ID where supported.",
    }
    schema = {
        "openapi": "3.1.0",
        "info": {
            "title": "TCG Agency API",
            "version": "1.0.0",
            "description": "Programmatic interface for managing content such as services. Font Awesome icons should be provided using Font Awesome v5 class names (very important).",
        },
        "servers": [{"url": server_url}],
        "paths": {
            "/api/services/": {
                "post": {
                    "operationId": "createService",
                    "summary": "Create a service item",
                    "description": "Creates a new serviceSection entry.",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ServiceCreateRequest"}
                            },
                            "multipart/form-data": {
                                "schema": {
                                    "allOf": [
                                        {"$ref": "#/components/schemas/ServiceCreateRequest"},
                                        {
                                            "type": "object",
                                            "properties": {
                                                "detail_page_image": {
                                                    "type": "string",
                                                    "format": "binary",
                                                    "description": "Optional image upload for the service detail page."
                                                }
                                            }
                                        }
                                    ]
                                }
                            },
                        },
                    },
                    "responses": {
                        "201": {
                            "description": "Service created",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ServiceResponse"}
                                }
                            },
                        },
                        "400": bad_request,
                        "405": method_not_allowed,
                    },
                }
                ,
                "patch": {
                    "operationId": "updateService",
                    "summary": "Update a service item",
                    "description": "Partial update of a service by ID (query param).",
                    "parameters": [
                        {
                            "in": "query",
                            "name": "id",
                            "required": True,
                            "schema": {"type": "integer"},
                            "description": "Service ID to update"
                        }
                    ],
                    "requestBody": {
                        "required": False,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ServiceUpdateRequest"}
                            },
                            "multipart/form-data": {
                                "schema": {
                                    "allOf": [
                                        {"$ref": "#/components/schemas/ServiceUpdateRequest"},
                                        {
                                            "type": "object",
                                            "properties": {
                                                "detail_page_image": {
                                                    "type": "string",
                                                    "format": "binary",
                                                    "description": "Optional image upload for the service detail page."
                                                }
                                            }
                                        }
                                    ]
                                }
                            },
                        },
                    },
                    "responses": {
                        "200": {"description": "Service updated", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ServiceResponse"}}}},
                        "400": bad_request,
                        "404": not_found,
                        "405": method_not_allowed,
                    },
                },
                "get": {
                    "operationId": "listServices",
                    "summary": "List or retrieve services",
                    "description": "Retrieve all services, search by keyword in name/description, or fetch a single service by id.",
                    "parameters": [id_param, search_param],
                    "responses": {
                        "200": {
                            "description": "Services found",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "oneOf": [
                                            {"$ref": "#/components/schemas/ServiceResponse"},
                                            {"$ref": "#/components/schemas/ServiceListResponse"}
                                        ]
                                    }
                                }
                            }
                        },
                        "404": not_found,
                        "405": method_not_allowed,
                    },
                }
            }
            ,
            "/api/workflows/": {
                "post": {
                    "operationId": "createWorkflow",
                    "summary": "Create a workflow",
                    "description": "Creates a workflow with optional nodes and edges payload (React Flow compatible).",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/WorkflowCreateRequest"}
                            }
                        },
                    },
                    "responses": {
                        "201": {
                            "description": "Workflow created",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/WorkflowResponse"}
                                }
                            },
                        },
                        "400": bad_request,
                        "405": method_not_allowed,
                    },
                },
                "patch": {
                    "operationId": "updateWorkflow",
                    "summary": "Update a workflow",
                    "description": "Partial update of a workflow by ID (query param). If nodes/edges are supplied, they replace the existing graph.",
                    "parameters": [
                        {
                            "in": "query",
                            "name": "id",
                            "required": True,
                            "schema": {"type": "integer"},
                            "description": "Workflow ID to update"
                        }
                    ],
                    "requestBody": {
                        "required": False,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/WorkflowUpdateRequest"}
                            }
                        },
                    },
                    "responses": {
                        "200": {"description": "Workflow updated", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/WorkflowResponse"}}}},
                        "400": bad_request,
                        "404": not_found,
                        "405": method_not_allowed,
                    },
                },
                "get": {
                    "operationId": "listWorkflows",
                    "summary": "List or retrieve workflows",
                    "description": "Retrieve all workflows (with nodes/edges), search by name/description, or fetch a single workflow by id.",
                    "parameters": [id_param, search_param],
                    "responses": {
                        "200": {
                            "description": "Workflows found",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "oneOf": [
                                            {"$ref": "#/components/schemas/WorkflowResponse"},
                                            {"$ref": "#/components/schemas/WorkflowListResponse"}
                                        ]
                                    }
                                }
                            }
                        },
                        "404": not_found,
                        "405": method_not_allowed,
                    },
                }
            }
            ,
            "/api/project-categories/": {
                "post": {
                    "operationId": "createProjectCategory",
                    "summary": "Create a project category",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ProjectCategoryCreateRequest"}
                            },
                            "multipart/form-data": {
                                "schema": {"$ref": "#/components/schemas/ProjectCategoryCreateRequest"}
                            },
                        },
                    },
                    "responses": {
                        "201": {
                            "description": "Category created",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ProjectCategoryResponse"}
                                }
                            },
                        },
                        "400": bad_request,
                        "405": method_not_allowed,
                    },
                },
                "patch": {
                    "operationId": "updateProjectCategory",
                    "summary": "Update a project category",
                    "parameters": [
                        {
                            "in": "query",
                            "name": "id",
                            "schema": {"type": "integer"},
                            "required": True,
                            "description": "Category ID to update."
                        }
                    ],
                    "requestBody": {
                        "required": False,
                        "content": {
                            "application/json": {"schema": {"$ref": "#/components/schemas/ProjectCategoryUpdateRequest"}},
                            "multipart/form-data": {"schema": {"$ref": "#/components/schemas/ProjectCategoryUpdateRequest"}},
                        },
                    },
                    "responses": {
                        "200": {"description": "Category updated", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ProjectCategoryResponse"}}}},
                        "400": bad_request,
                        "404": not_found,
                        "405": method_not_allowed,
                    },
                },
                "get": {
                    "operationId": "listProjectCategories",
                    "summary": "List or retrieve project categories",
                    "parameters": [id_param, search_param],
                    "responses": {
                        "200": {
                            "description": "Categories found",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "oneOf": [
                                            {"$ref": "#/components/schemas/ProjectCategoryResponse"},
                                            {"$ref": "#/components/schemas/ProjectCategoryListResponse"}
                                        ]
                                    }
                                }
                            }
                        },
                        "404": not_found,
                        "405": method_not_allowed,
                    },
                },
            },
            "/api/projects/": {
                "post": {
                    "operationId": "createProject",
                    "summary": "Create a project",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ProjectCreateRequest"}
                            },
                            "multipart/form-data": {
                                "schema": {
                                    "allOf": [
                                        {"$ref": "#/components/schemas/ProjectCreateRequest"},
                                        {
                                            "type": "object",
                                            "properties": {
                                                "image": {
                                                    "type": "string",
                                                    "format": "binary",
                                                    "description": "Optional project image upload."
                                                }
                                            }
                                        }
                                    ]
                                }
                            },
                        },
                    },
                    "responses": {
                        "201": {
                            "description": "Project created",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ProjectResponse"}
                                }
                            },
                        },
                        "400": bad_request,
                        "405": method_not_allowed,
                    },
                },
                "patch": {
                    "operationId": "updateProject",
                    "summary": "Update a project",
                    "parameters": [
                        {
                            "in": "query",
                            "name": "id",
                            "schema": {"type": "integer"},
                            "required": True,
                            "description": "Project ID to update."
                        }
                    ],
                    "requestBody": {
                        "required": False,
                        "content": {
                            "application/json": {"schema": {"$ref": "#/components/schemas/ProjectUpdateRequest"}},
                            "multipart/form-data": {
                                "schema": {
                                    "allOf": [
                                        {"$ref": "#/components/schemas/ProjectUpdateRequest"},
                                        {
                                            "type": "object",
                                            "properties": {
                                                "image": {
                                                    "type": "string",
                                                    "format": "binary",
                                                    "description": "Optional project image upload."
                                                }
                                            }
                                        }
                                    ]
                                }
                            },
                        },
                    },
                    "responses": {
                        "200": {"description": "Project updated", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ProjectResponse"}}}},
                        "400": bad_request,
                        "404": not_found,
                        "405": method_not_allowed,
                    },
                },
                "get": {
                    "operationId": "listProjects",
                    "summary": "List or retrieve projects",
                    "parameters": [id_param, search_param, category_param],
                    "responses": {
                        "200": {
                            "description": "Projects found",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "oneOf": [
                                            {"$ref": "#/components/schemas/ProjectResponse"},
                                            {"$ref": "#/components/schemas/ProjectListResponse"}
                                        ]
                                    }
                                }
                            }
                        },
                        "404": not_found,
                        "405": method_not_allowed,
                    },
                },
            },
            "/api/blog-categories/": {
                "post": {
                    "operationId": "createBlogCategory",
                    "summary": "Create a blog category",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/BlogCategoryCreateRequest"}
                            },
                            "multipart/form-data": {
                                "schema": {"$ref": "#/components/schemas/BlogCategoryCreateRequest"}
                            },
                        },
                    },
                    "responses": {
                        "201": {
                            "description": "Category created",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/BlogCategoryResponse"}
                                }
                            },
                        },
                        "400": bad_request,
                        "405": method_not_allowed,
                    },
                },
                "patch": {
                    "operationId": "updateBlogCategory",
                    "summary": "Update a blog category",
                    "parameters": [
                        {"in": "query", "name": "id", "schema": {"type": "integer"}, "required": True, "description": "Category ID to update."}
                    ],
                    "requestBody": {
                        "required": False,
                        "content": {
                            "application/json": {"schema": {"$ref": "#/components/schemas/BlogCategoryUpdateRequest"}},
                            "multipart/form-data": {"schema": {"$ref": "#/components/schemas/BlogCategoryUpdateRequest"}},
                        },
                    },
                    "responses": {
                        "200": {"description": "Category updated", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/BlogCategoryResponse"}}}},
                        "400": bad_request,
                        "404": not_found,
                        "405": method_not_allowed,
                    },
                },
                "get": {
                    "operationId": "listBlogCategories",
                    "summary": "List or retrieve blog categories",
                    "parameters": [id_param, search_param],
                    "responses": {
                        "200": {
                            "description": "Categories found",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "oneOf": [
                                            {"$ref": "#/components/schemas/BlogCategoryResponse"},
                                            {"$ref": "#/components/schemas/BlogCategoryListResponse"}
                                        ]
                                    }
                                }
                            }
                        },
                        "404": not_found,
                        "405": method_not_allowed,
                    },
                },
            },
            "/api/blogs/": {
                "post": {
                    "operationId": "createBlog",
                    "summary": "Create a blog post",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/BlogCreateRequest"}
                            },
                            "multipart/form-data": {
                                "schema": {
                                    "allOf": [
                                        {"$ref": "#/components/schemas/BlogCreateRequest"},
                                        {
                                            "type": "object",
                                            "properties": {
                                                "thumbnail": {
                                                    "type": "string",
                                                    "format": "binary",
                                                    "description": "Optional blog thumbnail upload."
                                                }
                                            }
                                        }
                                    ]
                                }
                            },
                        },
                    },
                    "responses": {
                        "201": {
                            "description": "Blog created",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/BlogResponse"}
                                }
                            },
                        },
                        "400": bad_request,
                        "405": method_not_allowed,
                    },
                },
                "patch": {
                    "operationId": "updateBlog",
                    "summary": "Update a blog post",
                    "parameters": [
                        {"in": "query", "name": "id", "schema": {"type": "integer"}, "required": True, "description": "Blog ID to update."}
                    ],
                    "requestBody": {
                        "required": False,
                        "content": {
                            "application/json": {"schema": {"$ref": "#/components/schemas/BlogUpdateRequest"}},
                            "multipart/form-data": {
                                "schema": {
                                    "allOf": [
                                        {"$ref": "#/components/schemas/BlogUpdateRequest"},
                                        {
                                            "type": "object",
                                            "properties": {
                                                "thumbnail": {
                                                    "type": "string",
                                                    "format": "binary",
                                                    "description": "Optional blog thumbnail upload."
                                                }
                                            }
                                        }
                                    ]
                                }
                            },
                        },
                    },
                    "responses": {
                        "200": {"description": "Blog updated", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/BlogResponse"}}}},
                        "400": bad_request,
                        "404": not_found,
                        "405": method_not_allowed,
                    },
                },
                "get": {
                    "operationId": "listBlogs",
                    "summary": "List or retrieve blog posts",
                    "parameters": [id_param, search_param, category_param],
                    "responses": {
                        "200": {
                            "description": "Blogs found",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "oneOf": [
                                            {"$ref": "#/components/schemas/BlogResponse"},
                                            {"$ref": "#/components/schemas/BlogListResponse"}
                                        ]
                                    }
                                }
                            }
                        },
                        "404": not_found,
                        "405": method_not_allowed,
                    },
                },
            },
            "/api/blog-sample-conversations/": {
                "get": {
                    "operationId": "listBlogSampleConversations",
                    "summary": "List or retrieve blog sample conversations",
                    "parameters": [id_param, blog_param],
                    "responses": {
                        "200": {
                            "description": "List or single item",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "oneOf": [
                                            {"$ref": "#/components/schemas/BlogSampleConversation"},
                                            {"$ref": "#/components/schemas/BlogSampleConversationListResponse"},
                                        ]
                                    }
                                }
                            },
                        }
                    },
                },
                "post": {
                    "operationId": "createBlogSampleConversation",
                    "summary": "Create a blog sample conversation",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/BlogSampleConversationCreate"}
                            }
                        },
                    },
                    "responses": {
                        "201": {
                            "description": "Created (includes success + translation flags)",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/BlogSampleConversationEnvelope"}
                                }
                            },
                        },
                        "400": {"description": "Validation error"},
                    },
                },
                "put": {
                    "operationId": "updateBlogSampleConversation",
                    "summary": "Update a blog sample conversation",
                    "parameters": [id_param, blog_param],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/BlogSampleConversationUpdate"}
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "Updated (includes success + translation flags)",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/BlogSampleConversationEnvelope"}
                                }
                            },
                        },
                        "404": not_found,
                    },
                },
            },
        },
        "components": {
            "parameters": {
                "IdParam": {
                    "in": "query",
                    "name": "id",
                    "schema": {"type": "integer"},
                    "required": False,
                    "description": "Optional primary key used by list endpoints to fetch a single record."
                },
                "SearchParam": {
                    "in": "query",
                    "name": "search",
                    "schema": {"type": "string"},
                    "required": False,
                    "description": "Case-insensitive search term."
                },
                "CategoryParam": {
                    "in": "query",
                    "name": "category",
                    "schema": {"type": "integer"},
                    "required": False,
                    "description": "Filter by category ID where supported."
                },
                "BlogParam": {
                    "in": "query",
                    "name": "blog",
                    "schema": {"type": "integer"},
                    "required": False,
                    "description": "Filter by blog ID where supported."
                },
            },
            "responses": {
                "BadRequest": {"description": "Invalid input"},
                "NotFound": {"description": "Resource not found"},
                "MethodNotAllowed": {"description": "Method not allowed"},
            },
            "schemas": {
                "ConversationEntry": {
                    "type": "object",
                    "properties": {
                        "topic": {"type": "string", "nullable": True},
                        "user_message": {"type": "string", "nullable": True},
                        "assistant_message": {"type": "string", "nullable": True},
                        "tone": {"type": "string", "nullable": True},
                    },
                },
                "BlogSampleConversation": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "blog": {"type": "integer"},
                        "title": {"type": "string", "nullable": True},
                        "subtitle": {"type": "string", "nullable": True},
                        "title_en": {"type": "string", "nullable": True},
                        "title_tr": {"type": "string", "nullable": True},
                        "subtitle_en": {"type": "string", "nullable": True},
                        "subtitle_tr": {"type": "string", "nullable": True},
                        "conversations": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/ConversationEntry"},
                            "default": [],
                            "maxItems": 30,
                            "description": "Default-language conversation entries (max 30).",
                        },
                        "conversations_en": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/ConversationEntry"},
                            "default": [],
                            "maxItems": 30,
                            "description": "Language-specific entries; used when English is active.",
                        },
                        "conversations_tr": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/ConversationEntry"},
                            "default": [],
                            "maxItems": 30,
                            "description": "Language-specific entries; used when Turkish is active.",
                        },
                        "created_at": {"type": "string", "format": "date-time"},
                        "updated_at": {"type": "string", "format": "date-time"},
                    },
                    "required": ["id", "blog"],
                },
                "BlogSampleConversationCreate": {
                    "type": "object",
                    "properties": {
                        "blog": {"type": "integer"},
                        "title": {"type": "string", "nullable": True},
                        "subtitle": {"type": "string", "nullable": True},
                        "title_en": {"type": "string", "nullable": True},
                        "title_tr": {"type": "string", "nullable": True},
                        "subtitle_en": {"type": "string", "nullable": True},
                        "subtitle_tr": {"type": "string", "nullable": True},
                        "conversations": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/ConversationEntry"},
                            "default": [],
                            "maxItems": 30,
                        },
                        "conversations_en": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/ConversationEntry"},
                            "default": [],
                            "maxItems": 30,
                        },
                        "conversations_tr": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/ConversationEntry"},
                            "default": [],
                            "maxItems": 30,
                        },
                    },
                    "required": ["blog"],
                },
                "BlogSampleConversationUpdate": {
                    "type": "object",
                    "properties": {
                        "blog": {"type": "integer"},
                        "title": {"type": "string", "nullable": True},
                        "subtitle": {"type": "string", "nullable": True},
                        "title_en": {"type": "string", "nullable": True},
                        "title_tr": {"type": "string", "nullable": True},
                        "subtitle_en": {"type": "string", "nullable": True},
                        "subtitle_tr": {"type": "string", "nullable": True},
                        "conversations": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/ConversationEntry"},
                            "default": [],
                            "maxItems": 30,
                        },
                        "conversations_en": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/ConversationEntry"},
                            "default": [],
                            "maxItems": 30,
                        },
                        "conversations_tr": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/ConversationEntry"},
                            "default": [],
                            "maxItems": 30,
                        },
                    },
                },
                "BlogSampleConversationListResponse": {
                    "type": "object",
                    "properties": {
                        "count": {"type": "integer"},
                        "items": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/BlogSampleConversation"},
                        },
                    },
                },
                "BlogSampleConversationEnvelope": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "description": "True when the operation succeeded."},
                        "translation_success": {
                            "type": "boolean",
                            "description": "Whether auto-translation ran without errors (may be False if the translation backend failed).",
                        },
                        "item": {"$ref": "#/components/schemas/BlogSampleConversation"},
                    },
                    "required": ["item"],
                    "example": {
                        "success": True,
                        "translation_success": True,
                        "item": {
                            "id": 20,
                            "blog": 17,
                            "title": "Salon Booking Conversation Example",
                            "subtitle": "AI-powered WhatsApp assistant handling client booking and loyalty interaction",
                            "title_tr": "Salon Randevu Sohbet Örneği",
                            "subtitle_tr": "Müşteri randevusu ve sadakat etkileşimlerini yöneten yapay zeka destekli WhatsApp asistanı",
                            "conversations": [],
                            "conversations_en": [],
                            "conversations_tr": [],
                            "created_at": "2025-01-10T12:00:00Z",
                            "updated_at": "2025-01-10T12:00:00Z",
                        },
                    },
                },
                "ServiceCreateRequest": {
                    "type": "object",
                    "required": ["name"],
                    "properties": {
                        "name": {"type": "string", "maxLength": 200},
                        "short_description": {"type": "string", "maxLength": 500},
                        "fontawesome_icon_class": {"type": "string", "maxLength": 100},
                        "detail_page_description": {"type": "string", "description": "HTML body allowed."},
                        "detail_page_image_url": {
                            "type": "string",
                            "format": "uri",
                            "description": "Optional HTTPS URL to download an image (must end with .png/.jpg/.jpeg/.webp/.gif)."
                        },
                    },
                },
                "ServiceResponse": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"},
                        "slug": {"type": "string"},
                        "short_description": {"type": "string"},
                        "fontawesome_icon_class": {"type": "string"},
                        "detail_page_description": {"type": "string"},
                        "show_call_now_widget": {
                            "type": "boolean",
                            "description": "Always true for created services.",
                            "example": True
                        },
                        "detail_page_image": {
                            "type": ["string", "null"],
                            "format": "uri",
                            "description": "URL of the stored image, if provided."
                        },
                    },
                },
                "ServiceUpdateRequest": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "maxLength": 200},
                        "short_description": {"type": "string", "maxLength": 500},
                        "fontawesome_icon_class": {"type": "string", "maxLength": 100},
                        "detail_page_description": {"type": "string"},
                        "detail_page_image_url": {"type": "string", "format": "uri"},
                    },
                },
                "ServiceListResponse": {
                    "type": "object",
                    "properties": {
                        "count": {"type": "integer"},
                        "items": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/ServiceResponse"}
                        }
                    }
                },
                "WorkflowNodeItem": {
                    "type": "object",
                    "properties": {
                        "slug": {"type": "string"},
                        "name": {"type": "string"},
                        "color": {"type": ["string", "null"], "description": "Hex color without # (e.g., 25D366)"}
                    }
                },
                "WorkflowNode": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "description": "Unique node id within a workflow"},
                        "type": {
                            "type": "string",
                            "enum": ["eventNode", "agentNode", "connectorNode", "actionNode", "logicNode"],
                            "description": "Node type"
                        },
                        "label": {"type": "string"},
                        "description": {"type": "string"},
                        "iconSlug": {"type": "string", "description": "SimpleIcons slug"},
                        "iconColor": {"type": ["string", "null"], "description": "Hex color without #"},
                        "iconAlt": {"type": "string"},
                        "items": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/WorkflowNodeItem"}
                        },
                        "posDesktop": {
                            "type": "object",
                            "properties": {
                                "x": {"type": "integer"},
                                "y": {"type": "integer"}
                            }
                        },
                        "posMobile": {
                            "type": "object",
                            "properties": {
                                "x": {"type": "integer"},
                                "y": {"type": "integer"}
                            }
                        }
                    }
                },
                "WorkflowEdge": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "description": "Edge id (e.g., e1-2)"},
                        "source": {"type": "string", "description": "Source node id"},
                        "target": {"type": "string", "description": "Target node id"}
                    }
                },
                "WorkflowCreateRequest": {
                    "type": "object",
                    "required": ["name"],
                    "properties": {
                        "name": {"type": "string", "maxLength": 255},
                        "description": {"type": "string"},
                        "is_active": {"type": "boolean", "default": True},
                        "nodes": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/WorkflowNode"}
                        },
                        "edges": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/WorkflowEdge"}
                        }
                    }
                },
                "WorkflowUpdateRequest": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "maxLength": 255},
                        "description": {"type": "string"},
                        "is_active": {"type": "boolean"},
                        "nodes": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/WorkflowNode"},
                            "description": "If provided, replaces all nodes."
                        },
                        "edges": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/WorkflowEdge"},
                            "description": "If provided, replaces all edges."
                        }
                    }
                },
                "WorkflowResponse": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"},
                        "slug": {"type": "string"},
                        "description": {"type": ["string", "null"]},
                        "is_active": {"type": "boolean"},
                        "created_at": {"type": "string", "format": "date-time"},
                        "updated_at": {"type": "string", "format": "date-time"},
                        "nodes": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/WorkflowNode"}
                        },
                        "edges": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/WorkflowEdge"}
                        }
                    }
                },
                "WorkflowListResponse": {
                    "type": "object",
                    "properties": {
                        "count": {"type": "integer"},
                        "items": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/WorkflowResponse"}
                        }
                    }
                },
                "ProjectCategoryCreateRequest": {
                    "type": "object",
                    "required": ["name"],
                    "properties": {
                        "name": {"type": "string", "maxLength": 200},
                    },
                },
                "ProjectCategoryUpdateRequest": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "maxLength": 200},
                    },
                },
                "ProjectCategoryResponse": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"},
                        "slug": {"type": "string"},
                    },
                },
                "ProjectCategoryListResponse": {
                    "type": "object",
                    "properties": {
                        "count": {"type": "integer"},
                        "items": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/ProjectCategoryResponse"}
                        }
                    }
                },
                "ProjectCreateRequest": {
                    "type": "object",
                    "required": ["title"],
                    "properties": {
                        "title": {"type": "string", "maxLength": 200},
                        "description": {"type": "string"},
                        "client": {"type": "string", "maxLength": 200},
                        "company": {"type": "string", "maxLength": 200},
                        "duration": {"type": "string", "maxLength": 100},
                        "category_id": {"type": "integer", "description": "Optional category ID to associate."},
                        "image_url": {
                            "type": "string",
                            "format": "uri",
                        "description": "Optional HTTPS URL to download an image (must end with .png/.jpg/.jpeg/.webp/.gif)."
                        },
                    },
                },
                "ProjectUpdateRequest": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "maxLength": 200},
                        "description": {"type": "string"},
                        "client": {"type": "string", "maxLength": 200},
                        "company": {"type": "string", "maxLength": 200},
                        "duration": {"type": "string", "maxLength": 100},
                        "category_id": {"type": "integer"},
                        "image_url": {"type": "string", "format": "uri"},
                    },
                },
                "ProjectResponse": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "title": {"type": "string"},
                        "slug": {"type": "string"},
                        "description": {"type": "string"},
                        "client": {"type": "string"},
                        "company": {"type": "string"},
                        "duration": {"type": "string"},
                        "category": {"$ref": "#/components/schemas/ProjectCategoryResponse"},
                        "image": {"type": ["string", "null"], "format": "uri"},
                    },
                },
                "ProjectListResponse": {
                    "type": "object",
                    "properties": {
                        "count": {"type": "integer"},
                        "items": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/ProjectResponse"}
                        }
                    }
                },
                "BlogCategoryCreateRequest": {
                    "type": "object",
                    "required": ["title"],
                    "properties": {
                        "title": {"type": "string", "maxLength": 200},
                    },
                },
                "BlogCategoryUpdateRequest": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "maxLength": 200},
                    },
                },
                "BlogCategoryResponse": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "title": {"type": "string"},
                        "slug": {"type": "string"},
                    },
                },
                "BlogCategoryListResponse": {
                    "type": "object",
                    "properties": {
                        "count": {"type": "integer"},
                        "items": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/BlogCategoryResponse"}
                        }
                    }
                },
                "BlogCreateRequest": {
                    "type": "object",
                    "required": ["title"],
                    "properties": {
                        "title": {"type": "string", "maxLength": 1000},
                        "author": {"type": "string", "maxLength": 100},
                        "description": {"type": "string"},
                        "category_id": {"type": "integer", "description": "Optional blog category ID."},
                        "thumbnail_url": {
                            "type": "string",
                            "format": "uri",
                            "description": "Optional HTTPS URL to download an image (must end with .png/.jpg/.jpeg/.webp/.gif)."
                        },
                    },
                },
                "BlogUpdateRequest": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "maxLength": 1000},
                        "author": {"type": "string", "maxLength": 100},
                        "description": {"type": "string"},
                        "category_id": {"type": "integer"},
                        "thumbnail_url": {"type": "string", "format": "uri"},
                    },
                },
                "BlogResponse": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "title": {"type": "string"},
                        "slug": {"type": "string"},
                        "description": {"type": "string"},
                        "author": {"type": "string"},
                        "category": {"$ref": "#/components/schemas/BlogCategoryResponse"},
                        "thumbnail": {"type": ["string", "null"], "format": "uri"},
                        "created_at": {"type": "string", "format": "date"},
                        "updated_at": {"type": "string", "format": "date"},
                    },
                },
                "BlogListResponse": {
                    "type": "object",
                    "properties": {
                        "count": {"type": "integer"},
                        "items": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/BlogResponse"}
                        }
                    }
                },
                "TestimonialCreateRequest": {
                    "type": "object",
                    "required": ["name"],
                    "properties": {
                        "name": {"type": "string", "maxLength": 200},
                        "position": {"type": "string", "maxLength": 200, "nullable": True},
                        "description": {"type": "string", "nullable": True},
                        "star": {"type": "integer", "minimum": 0, "maximum": 5, "nullable": True},
                    },
                },
                "TestimonialUpdateRequest": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "maxLength": 200},
                        "position": {"type": "string", "maxLength": 200, "nullable": True},
                        "description": {"type": "string", "nullable": True},
                        "star": {"type": "integer", "minimum": 0, "maximum": 5, "nullable": True},
                    },
                },
                "TestimonialResponse": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"},
                        "position": {"type": ["string", "null"]},
                        "description": {"type": ["string", "null"]},
                        "star": {"type": ["integer", "null"]},
                        "image": {"type": ["string", "null"], "format": "uri"},
                    },
                },
                "TestimonialListResponse": {
                    "type": "object",
                    "properties": {
                        "count": {"type": "integer"},
                        "items": {"type": "array", "items": {"$ref": "#/components/schemas/TestimonialResponse"}}
                    }
                },
                "AboutCreateRequest": {
                    "type": "object",
                    "properties": {
                        "subtitle": {"type": "string", "nullable": True},
                        "title": {"type": "string", "nullable": True},
                        "short_description": {"type": "string", "nullable": True},
                        "long_description": {"type": "string", "nullable": True},
                        "ranking_number": {"type": "integer", "nullable": True},
                        "tag_line": {"type": "string", "nullable": True},
                        "experience": {"type": "string", "nullable": True},
                        "video_url": {"type": "string", "format": "uri", "nullable": True},
                    },
                },
                "AboutUpdateRequest": {"$ref": "#/components/schemas/AboutCreateRequest"},
                "AboutResponse": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "subtitle": {"type": ["string", "null"]},
                        "title": {"type": ["string", "null"]},
                        "short_description": {"type": ["string", "null"]},
                        "long_description": {"type": ["string", "null"]},
                        "ranking_number": {"type": ["integer", "null"]},
                        "tag_line": {"type": ["string", "null"]},
                        "experience": {"type": ["string", "null"]},
                        "video_url": {"type": ["string", "null"], "format": "uri"},
                        "image": {"type": ["string", "null"], "format": "uri"},
                        "video_thumbnail": {"type": ["string", "null"], "format": "uri"},
                    },
                },
                "AboutListResponse": {
                    "type": "object",
                    "properties": {
                        "count": {"type": "integer"},
                        "items": {"type": "array", "items": {"$ref": "#/components/schemas/AboutResponse"}}
                    }
                },
            }
        },
    }
    return JsonResponse(schema, json_dumps_params={"indent": 2})

def openapi_docs(request):
    """
    Lightweight Swagger UI page that points to the generated openapi.json.
    """
    origin = request.headers.get("Origin")
    forwarded_proto = request.headers.get("X-Forwarded-Proto", "").split(",")[0].strip().lower()
    forwarded_host = request.headers.get("X-Forwarded-Host", "").split(",")[0].strip()
    forwarded_port = request.headers.get("X-Forwarded-Port", "").split(",")[0].strip()
    host = forwarded_host or request.get_host()

    if forwarded_port and ":" not in host and forwarded_port not in ("80", "443"):
        host = f"{host}:{forwarded_port}"

    if origin:
        server_url = origin.rstrip("/")
    else:
        known_https_hosts = {"wsp.whatsynaptic.tech", "automate.beyondclinic.online", "www.automate.beyondclinic.online"}
        if forwarded_proto:
            scheme = forwarded_proto
        elif request.is_secure() or host in known_https_hosts:
            scheme = "https"
        else:
            scheme = request.scheme
        server_url = f"{scheme}://{host}"

    spec_url = f"{server_url}{reverse('openapi_json')}"
    html = f"""
    <!doctype html>
    <html>
    <head>
      <meta charset="utf-8"/>
      <title>API Docs</title>
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css" />
      <style>
        body {{ margin: 0; padding: 0; }}
        #swagger-ui {{ min-height: 100vh; }}
      </style>
    </head>
    <body>
      <div id="swagger-ui"></div>
      <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
      <script>
        window.onload = () => {{
          SwaggerUIBundle({{
            url: "{spec_url}",
            dom_id: '#swagger-ui',
            presets: [SwaggerUIBundle.presets.apis],
          }});
        }};
      </script>
    </body>
    </html>
    """
    return HttpResponse(html)

def error_404(request, exception):
    return render(request, 'error/404.html', status=404)
