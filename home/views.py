import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from home.utils import download_image_to_field
from home.models import *
from pricing.models import pricingSection
from about.models import teamSection
from blog.models import *
from settings.models import templateSettings
from analytics.views import visitor_data
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
    return JsonResponse(serialize_service(service), status=200)

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
    return JsonResponse(serialize_project(proj), status=200)

def openapi_json(request):
    """
    Minimal OpenAPI 3.1 schema describing the service creation endpoint.
    """
    # Prefer Origin header for correct scheme (e.g., https). Fallback forces https for known host if needed.
    origin = request.headers.get("Origin")
    if origin:
        server_url = origin.rstrip("/")
    else:
        host = request.get_host()
        forwarded_proto = request.headers.get("X-Forwarded-Proto", "").split(",")[0].strip().lower()
        # Force https for known deployments and when a proxy tells us the original scheme
        if forwarded_proto == "https" or request.is_secure() or host in ("wsp.lotfinity.tech", "automate.beyondclinic.online", "www.automate.beyondclinic.online"):
            scheme = "https"
        else:
            scheme = request.scheme
        server_url = f"{scheme}://{host}"
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
                        "400": {"description": "Invalid input"},
                        "405": {"description": "Method not allowed"},
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
                        "400": {"description": "Invalid input"},
                        "404": {"description": "Service not found"},
                        "405": {"description": "Method not allowed"},
                    },
                },
                "get": {
                    "operationId": "listServices",
                    "summary": "List or retrieve services",
                    "description": "Retrieve all services, search by keyword in name/description, or fetch a single service by id.",
                    "parameters": [
                        {
                            "in": "query",
                            "name": "id",
                            "required": False,
                            "schema": {"type": "integer"},
                            "description": "If provided, return a single service by ID."
                        },
                        {
                            "in": "query",
                            "name": "search",
                            "required": False,
                            "schema": {"type": "string"},
                            "description": "Case-insensitive search in service name and short description."
                        },
                    ],
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
                        "404": {"description": "Service not found"},
                        "405": {"description": "Method not allowed"},
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
                        "400": {"description": "Invalid input"},
                        "405": {"description": "Method not allowed"},
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
                        "400": {"description": "Invalid input"},
                        "404": {"description": "Category not found"},
                        "405": {"description": "Method not allowed"},
                    },
                },
                "get": {
                    "operationId": "listProjectCategories",
                    "summary": "List or retrieve project categories",
                    "parameters": [
                        {
                            "in": "query",
                            "name": "id",
                            "schema": {"type": "integer"},
                            "description": "If provided, return a single category by ID."
                        },
                        {
                            "in": "query",
                            "name": "search",
                            "schema": {"type": "string"},
                            "description": "Case-insensitive search in category name."
                        },
                    ],
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
                        "404": {"description": "Category not found"},
                        "405": {"description": "Method not allowed"},
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
                        "400": {"description": "Invalid input"},
                        "405": {"description": "Method not allowed"},
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
                        "400": {"description": "Invalid input"},
                        "404": {"description": "Project not found"},
                        "405": {"description": "Method not allowed"},
                    },
                },
                "get": {
                    "operationId": "listProjects",
                    "summary": "List or retrieve projects",
                    "parameters": [
                        {
                            "in": "query",
                            "name": "id",
                            "schema": {"type": "integer"},
                            "description": "If provided, return a single project by ID."
                        },
                        {
                            "in": "query",
                            "name": "search",
                            "schema": {"type": "string"},
                            "description": "Case-insensitive search in project title or description."
                        },
                        {
                            "in": "query",
                            "name": "category",
                            "schema": {"type": "integer"},
                            "description": "Filter by category ID."
                        },
                    ],
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
                        "404": {"description": "Project not found"},
                        "405": {"description": "Method not allowed"},
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
                        "400": {"description": "Invalid input"},
                        "405": {"description": "Method not allowed"},
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
                        "400": {"description": "Invalid input"},
                        "404": {"description": "Category not found"},
                        "405": {"description": "Method not allowed"},
                    },
                },
                "get": {
                    "operationId": "listBlogCategories",
                    "summary": "List or retrieve blog categories",
                    "parameters": [
                        {
                            "in": "query",
                            "name": "id",
                            "schema": {"type": "integer"},
                            "description": "If provided, return a single category by ID."
                        },
                        {
                            "in": "query",
                            "name": "search",
                            "schema": {"type": "string"},
                            "description": "Case-insensitive search in category title."
                        },
                    ],
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
                        "404": {"description": "Category not found"},
                        "405": {"description": "Method not allowed"},
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
                        "400": {"description": "Invalid input"},
                        "405": {"description": "Method not allowed"},
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
                        "400": {"description": "Invalid input"},
                        "404": {"description": "Blog not found"},
                        "405": {"description": "Method not allowed"},
                    },
                },
                "get": {
                    "operationId": "listBlogs",
                    "summary": "List or retrieve blog posts",
                    "parameters": [
                        {
                            "in": "query",
                            "name": "id",
                            "schema": {"type": "integer"},
                            "description": "If provided, return a single blog by ID."
                        },
                        {
                            "in": "query",
                            "name": "search",
                            "schema": {"type": "string"},
                            "description": "Case-insensitive search in title or description."
                        },
                        {
                            "in": "query",
                            "name": "category",
                            "schema": {"type": "integer"},
                            "description": "Filter by category ID."
                        },
                    ],
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
                        "404": {"description": "Blog not found"},
                        "405": {"description": "Method not allowed"},
                    },
                },
            },
        },
        "components": {
            "schemas": {
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
            }
        },
    }
    return JsonResponse(schema, json_dumps_params={"indent": 2})

def error_404(request, exception):
    return render(request, 'error/404.html', status=404)
