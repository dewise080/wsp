from django.http import HttpResponse
from django.template import loader
from home.models import *
from blog.models import *

def generate_sitemap(request):
    apps = [
        'home',
        'about',
        'service',
        'project',
        'blog',
        'pricing',
        'contact',
    ]

    urls = []

    for app_name in apps:
        try:
            urlconf = __import__(f'{app_name}.urls', fromlist=['urlpatterns'])
            urlpatterns = getattr(urlconf, 'urlpatterns', [])

            # Extract URL patterns from the resolver
            for pattern in urlpatterns:
                if hasattr(pattern, 'url_patterns'):
                    # If it's an included namespace, extract its URL patterns
                    urls.extend([f'/{url.pattern}' for url in pattern.url_patterns])
                else:
                    # Otherwise, add the URL pattern itself
                    urls.append(f'/{pattern.pattern}')
        except ImportError:
            pass
    

    # URLs for the Service model
    service_slugs = serviceSection.objects.values_list('slug', flat=True)
    if service_slugs:
        for slug in service_slugs:
            service_url = f'/service/details/{slug}/'
            urls.append(service_url)
    
    # URLs for the Project model
    project_slugs = projectSection.objects.values_list('slug', flat=True)
    if project_slugs:
        for slug in project_slugs:
            project_url = f'/project/details/{slug}/'
            urls.append(project_url)

    # URLs for the Blog model
    blog_slugs = Blogs.objects.values_list('slug', flat=True)
    if blog_slugs:
        for slug in blog_slugs:
            blog_url = f'/blog/{slug}/'
            urls.append(blog_url)
    
    blog_category_slugs = blogCategory.objects.values_list('slug', flat=True)
    if blog_category_slugs:
        for slug in blog_category_slugs:
            category_url = f'/blog/category/{slug}/'
            urls.append(category_url)

    # Filter out the unwanted URLs with placeholders
    urls = [url for url in urls if '<slug:slug>' not in url and '<int:id>' not in url and '<str:slug>' not in url and '<slug:category_slug>' not in url and '/contact/' not in url and '/subscribe/' not in url]
    

    context = {
        'urls': urls,
        'request': request,
    }

    sitemap_xml = loader.render_to_string('sitemap/sitemap.xml', context)
    sitemap_xml = sitemap_xml.replace('<priority>0.8</priority>', '<priority>1.0</priority>', 1)


    return HttpResponse(sitemap_xml, content_type="application/xml")
