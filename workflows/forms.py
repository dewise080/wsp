from django import forms
from .models import Workflow, WorkflowNode, WorkflowNodeItem, WorkflowEdge, WorkflowPageSEO


class WorkflowForm(forms.ModelForm):
    """Form for creating and editing workflows."""
    
    class Meta:
        model = Workflow
        fields = ['name', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Workflow Name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Workflow Description',
                'rows': 3
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class WorkflowNodeForm(forms.ModelForm):
    """Form for creating and editing workflow nodes."""
    
    class Meta:
        model = WorkflowNode
        fields = [
            'node_id', 'node_type', 'label', 'description',
            'icon_slug', 'icon_color', 'icon_alt',
            'pos_desktop_x', 'pos_desktop_y',
            'pos_mobile_x', 'pos_mobile_y'
        ]
        widgets = {
            'node_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Node ID (e.g., 1, 2, 3)'
            }),
            'node_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'label': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Node Label'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Node Description'
            }),
            'icon_slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., whatsapp, openai, slack'
            }),
            'icon_color': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Hex color (e.g., 25D366)'
            }),
            'icon_alt': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Icon Alt Text'
            }),
            'pos_desktop_x': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'pos_desktop_y': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'pos_mobile_x': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'pos_mobile_y': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
        }


class WorkflowNodeItemForm(forms.ModelForm):
    """Form for creating and editing node items."""
    
    class Meta:
        model = WorkflowNodeItem
        fields = ['slug', 'name', 'color', 'order']
        widgets = {
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., googlecalendar, slack'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Display Name'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Hex color (e.g., 1A73E8)'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
        }


class WorkflowEdgeForm(forms.ModelForm):
    """Form for creating and editing workflow edges."""
    
    class Meta:
        model = WorkflowEdge
        fields = ['edge_id', 'source_node', 'target_node']
        widgets = {
            'edge_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Edge ID (e.g., e1-2)'
            }),
            'source_node': forms.Select(attrs={
                'class': 'form-control'
            }),
            'target_node': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, workflow=None, **kwargs):
        super().__init__(*args, **kwargs)
        if workflow:
            self.fields['source_node'].queryset = WorkflowNode.objects.filter(workflow=workflow)
            self.fields['target_node'].queryset = WorkflowNode.objects.filter(workflow=workflow)


class WorkflowPageSEOForm(forms.ModelForm):
    """Form for workflow page SEO settings."""
    
    class Meta:
        model = WorkflowPageSEO
        fields = ['meta_title', 'meta_description']
        widgets = {
            'meta_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Meta Title'
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Meta Description',
                'rows': 3
            }),
        }
