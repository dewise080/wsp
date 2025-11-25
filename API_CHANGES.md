## API changes and utilities overview

- Added service endpoints (`/api/services/`) with GET (list/search/by id), POST (create), and PATCH/PUT (update by id). Accepts JSON or multipart; optional image upload or `detail_page_image_url` download.
- Added project category endpoints (`/api/project-categories/`) with GET/POST/PATCH and slug auto-generation fixes.
- Added project endpoints (`/api/projects/`) with GET (list/search/by id/filter by category), POST (create), and PATCH/PUT (update). Supports image upload or `image_url` download.
- Added blog category endpoints (`/api/blog-categories/`) with GET/POST/PATCH plus slug fixes.
- Added blog endpoints (`/api/blogs/`) with GET (list/search/by id/filter by category), POST (create), and PATCH/PUT (update). Supports thumbnail upload or `thumbnail_url` download.
- Introduced `home/utils.py` with `download_image_to_field` to fetch remote images (png/jpg/jpeg/webp/gif) and attach to ImageFields.
- Updated `openapi.json` generator (`home/views.py`) to document all endpoints (services, projects, project categories, blogs, blog categories) including create and update operations, request/response schemas, image upload/URL options, and Font Awesome v5 note.
- Fixed slug generation to use name/title with uniqueness and `super().save()` for services, projects, project categories, blog categories, and blogs.
