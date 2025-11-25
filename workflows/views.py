from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
