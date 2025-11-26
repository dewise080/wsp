from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from core.decorators import admin_role_required, both_role_required
from .models import Workflow, WorkflowNode, WorkflowNodeItem, WorkflowEdge, WorkflowPageSEO
from .forms import WorkflowForm, WorkflowNodeForm, WorkflowEdgeForm, WorkflowPageSEOForm
import json


# # # # # # # # # # # # # # # # # #
#      Admin Workflow Views       #
# # # # # # # # # # # # # # # # # #

@login_required(login_url='logIn')
@both_role_required
def adminWorkflowList(request):
    """List all workflows in admin dashboard."""
    workflows = Workflow.objects.all()
    context = {
        'title': 'Workflows',
        'workflows': workflows,
    }
    return render(request, 'dashboard/main/workflows/workflows.html', context)


@login_required(login_url='logIn')
@both_role_required
def adminWorkflowCreate(request):
    """Create a new workflow - displays the modifier.html for visual editing."""
    if request.method == 'POST':
        form = WorkflowForm(request.POST)
        if form.is_valid():
            workflow = form.save()
            messages.success(request, 'Workflow created successfully!')
            return redirect('adminWorkflowEdit', slug=workflow.slug)
    else:
        form = WorkflowForm()
    
    context = {
        'title': 'Create Workflow',
        'form': form,
    }
    return render(request, 'dashboard/main/workflows/create.html', context)


@login_required(login_url='logIn')
@both_role_required
def adminWorkflowEdit(request, slug):
    """Edit a workflow using the visual modifier interface."""
    workflow = get_object_or_404(Workflow, slug=slug)
    
    if request.method == 'POST':
        form = WorkflowForm(request.POST, instance=workflow)
        if form.is_valid():
            form.save()
            messages.success(request, 'Workflow updated successfully!')
            return redirect('adminWorkflowList')
    else:
        form = WorkflowForm(instance=workflow)
    
    context = {
        'title': f'Edit Workflow: {workflow.name}',
        'workflow': workflow,
        'form': form,
        'flow_data': workflow.get_flow_data_json(),
    }
    return render(request, 'dashboard/main/workflows/edit.html', context)


@login_required(login_url='logIn')
@both_role_required
def adminWorkflowModifier(request, slug):
    """Visual flow modifier interface for a workflow."""
    workflow = get_object_or_404(Workflow, slug=slug)
    
    context = {
        'title': f'Modify Workflow: {workflow.name}',
        'workflow': workflow,
        'flow_data': workflow.get_flow_data_json(),
    }
    return render(request, 'dashboard/main/workflows/modifier.html', context)


@login_required(login_url='logIn')
@both_role_required
def adminWorkflowDelete(request, id):
    """Delete a workflow."""
    workflow = get_object_or_404(Workflow, id=id)
    workflow.delete()
    messages.warning(request, 'Workflow deleted!')
    return redirect('adminWorkflowList')


@login_required(login_url='logIn')
@both_role_required
@csrf_exempt
def adminWorkflowSaveJson(request, slug):
    """
    API endpoint to save workflow data from the visual modifier.
    Receives JSON data and updates the workflow nodes and edges.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    workflow = get_object_or_404(Workflow, slug=slug)
    
    try:
        data = json.loads(request.body)
        nodes_data = data.get('nodes', [])
        edges_data = data.get('edges', [])
        
        # Clear existing nodes and edges
        workflow.nodes.all().delete()
        workflow.edges.all().delete()
        
        # Create nodes
        node_map = {}  # Map node_id to WorkflowNode instance
        for node in nodes_data:
            wf_node = WorkflowNode.objects.create(
                workflow=workflow,
                node_id=node.get('id', ''),
                node_type=node.get('type', 'connectorNode'),
                label=node.get('label', ''),
                description=node.get('description', ''),
                icon_slug=node.get('iconSlug', ''),
                icon_color=node.get('iconColor', ''),
                icon_alt=node.get('iconAlt', ''),
                pos_desktop_x=node.get('posDesktop', {}).get('x', 140),
                pos_desktop_y=node.get('posDesktop', {}).get('y', 140),
                pos_mobile_x=node.get('posMobile', {}).get('x', 140),
                pos_mobile_y=node.get('posMobile', {}).get('y', 140),
            )
            node_map[node.get('id', '')] = wf_node
            
            # Create node items
            for idx, item in enumerate(node.get('items', [])):
                WorkflowNodeItem.objects.create(
                    node=wf_node,
                    slug=item.get('slug', ''),
                    name=item.get('name', ''),
                    color=item.get('color', ''),
                    order=idx
                )
        
        # Create edges
        for edge in edges_data:
            source_id = edge.get('source', '')
            target_id = edge.get('target', '')
            
            if source_id in node_map and target_id in node_map:
                WorkflowEdge.objects.create(
                    workflow=workflow,
                    edge_id=edge.get('id', f'e{source_id}-{target_id}'),
                    source_node=node_map[source_id],
                    target_node=node_map[target_id]
                )
        
        return JsonResponse({'success': True, 'message': 'Workflow saved successfully'})
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Alias for upload - same functionality as save
adminWorkflowUploadJson = adminWorkflowSaveJson

def serialize_workflow_node(node):
    return {
        "id": str(node.node_id),
        "type": node.node_type,
        "label": node.label,
        "description": node.description or "",
        "iconSlug": node.icon_slug or "",
        "iconColor": node.icon_color or "",
        "iconAlt": node.icon_alt or node.label,
        "items": [
            {
                "slug": item.slug,
                "name": item.name,
                "color": item.color or ""
            }
            for item in node.items.all()
        ],
        "posDesktop": {"x": node.pos_desktop_x, "y": node.pos_desktop_y},
        "posMobile": {"x": node.pos_mobile_x, "y": node.pos_mobile_y},
    }


def serialize_workflow(workflow):
    nodes = [serialize_workflow_node(node) for node in workflow.nodes.all()]
    edges = [
        {"id": edge.edge_id, "source": str(edge.source_node.node_id), "target": str(edge.target_node.node_id)}
        for edge in workflow.edges.all()
    ]
    return {
        "id": workflow.id,
        "name": workflow.name,
        "slug": workflow.slug,
        "description": workflow.description,
        "is_active": workflow.is_active,
        "created_at": workflow.created_at.isoformat(),
        "updated_at": workflow.updated_at.isoformat(),
        "nodes": nodes,
        "edges": edges,
    }


def persist_workflow_graph(workflow, nodes_data, edges_data):
    workflow.nodes.all().delete()
    workflow.edges.all().delete()

    node_map = {}
    for node in nodes_data or []:
        wf_node = WorkflowNode.objects.create(
            workflow=workflow,
            node_id=node.get('id', ''),
            node_type=node.get('type', 'connectorNode'),
            label=node.get('label', ''),
            description=node.get('description', ''),
            icon_slug=node.get('iconSlug', ''),
            icon_color=node.get('iconColor', ''),
            icon_alt=node.get('iconAlt', ''),
            pos_desktop_x=node.get('posDesktop', {}).get('x', 140),
            pos_desktop_y=node.get('posDesktop', {}).get('y', 140),
            pos_mobile_x=node.get('posMobile', {}).get('x', 140),
            pos_mobile_y=node.get('posMobile', {}).get('y', 140),
        )
        node_map[node.get('id', '')] = wf_node

        for idx, item in enumerate(node.get('items', [])):
            WorkflowNodeItem.objects.create(
                node=wf_node,
                slug=item.get('slug', ''),
                name=item.get('name', ''),
                color=item.get('color', ''),
                order=idx
            )

    for edge in edges_data or []:
        source_id = edge.get('source', '')
        target_id = edge.get('target', '')
        if source_id in node_map and target_id in node_map:
            WorkflowEdge.objects.create(
                workflow=workflow,
                edge_id=edge.get('id', f"e{source_id}-{target_id}"),
                source_node=node_map[source_id],
                target_node=node_map[target_id]
            )


# # # # # # # # # # # # # # # # # #
#     Public Workflow API (JSON)   #
# # # # # # # # # # # # # # # # # #

@csrf_exempt
def api_workflows(request):
    """
    JSON API for workflows:
    - GET: list workflows, optional ?id= to fetch one, ?search= to filter by name/description.
    - POST: create a workflow with optional nodes/edges payload.
    - PATCH/PUT: update a workflow by ?id=, optionally replacing nodes/edges.
    """
    payload = {}
    if request.method in ['POST', 'PATCH', 'PUT']:
        if request.content_type and 'application/json' in request.content_type:
            try:
                payload = json.loads(request.body.decode() or "{}")
            except json.JSONDecodeError:
                return JsonResponse({'detail': 'Invalid JSON payload'}, status=400)
        else:
            payload = request.POST

    if request.method == 'GET':
        workflow_id = request.GET.get('id')
        search = request.GET.get('search')
        qs = Workflow.objects.all()
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(description__icontains=search))

        if workflow_id:
            try:
                workflow = qs.get(pk=int(workflow_id))
            except (ValueError, Workflow.DoesNotExist):
                return JsonResponse({'detail': 'Workflow not found'}, status=404)
            return JsonResponse(serialize_workflow(workflow), status=200)

        data = [serialize_workflow(w) for w in qs]
        return JsonResponse({'count': len(data), 'items': data}, status=200)

    if request.method == 'POST':
        name = payload.get('name')
        if not name:
            return JsonResponse({'detail': 'name is required'}, status=400)

        workflow = Workflow.objects.create(
            name=name,
            description=payload.get('description'),
            is_active=payload.get('is_active', True),
        )

        nodes = payload.get('nodes', [])
        edges = payload.get('edges', [])
        persist_workflow_graph(workflow, nodes, edges)

        return JsonResponse(serialize_workflow(workflow), status=201)

    if request.method in ['PATCH', 'PUT']:
        workflow_id = request.GET.get('id')
        if not workflow_id:
            return JsonResponse({'detail': 'id is required for update'}, status=400)
        try:
            workflow = Workflow.objects.get(pk=int(workflow_id))
        except (ValueError, Workflow.DoesNotExist):
            return JsonResponse({'detail': 'Workflow not found'}, status=404)

        for field in ['name', 'description']:
            if field in payload:
                setattr(workflow, field, payload.get(field))

        if 'is_active' in payload:
            workflow.is_active = bool(payload.get('is_active'))

        workflow.save()

        if 'nodes' in payload or 'edges' in payload:
            persist_workflow_graph(workflow, payload.get('nodes', []), payload.get('edges', []))

        return JsonResponse(serialize_workflow(workflow), status=200)

    return JsonResponse({'detail': 'Method not allowed'}, status=405)


# # # # # # # # # # # # # # # # # #
#     Frontend Workflow Views     #
# # # # # # # # # # # # # # # # # #

def workflowList(request):
    """Public page listing all active workflows."""
    workflows = Workflow.objects.filter(is_active=True)
    seo = WorkflowPageSEO.objects.first()
    
    context = {
        'title': 'Workflows',
        'workflows': workflows,
        'seo': seo,
    }
    return render(request, 'front/main/workflows/workflows.html', context)


def workflowDetail(request, slug):
    """Public page showing a single workflow visualization."""
    workflow = get_object_or_404(Workflow, slug=slug, is_active=True)
    
    context = {
        'title': workflow.name,
        'workflow': workflow,
        'flow_data': workflow.get_flow_data_json(),
    }
    return render(request, 'front/main/workflows/workflow_detail.html', context)


def workflowJsonApi(request, slug):
    """API endpoint to get workflow JSON data for React Flow."""
    workflow = get_object_or_404(Workflow, slug=slug, is_active=True)
    return JsonResponse(json.loads(workflow.get_flow_data_json()))
