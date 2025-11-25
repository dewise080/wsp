from django.db import models
from django.utils.text import slugify
import json


class Workflow(models.Model):
    """
    Main workflow model that stores the complete workflow configuration.
    Each workflow contains multiple nodes and edges.
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Workflow'
        verbose_name_plural = 'Workflows'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name:
            base_slug = slugify(self.name) or "workflow"
            slug = base_slug
            queryset = Workflow.objects.exclude(pk=self.pk)
            counter = 1

            while queryset.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug
        super().save(*args, **kwargs)

    def get_flow_data_json(self):
        """
        Returns the workflow data in the JSON format expected by React Flow.
        """
        nodes_data = []
        for node in self.nodes.all():
            node_data = {
                "id": str(node.node_id),
                "type": node.node_type,
                "label": node.label,
                "description": node.description or "",
                "iconSlug": node.icon_slug or "",
                "iconColor": node.icon_color or "",
                "iconAlt": node.icon_alt or node.label,
                "items": [],
                "posDesktop": {
                    "x": node.pos_desktop_x,
                    "y": node.pos_desktop_y
                },
                "posMobile": {
                    "x": node.pos_mobile_x,
                    "y": node.pos_mobile_y
                }
            }
            # Add items for connector nodes
            for item in node.items.all():
                node_data["items"].append({
                    "slug": item.slug,
                    "name": item.name,
                    "color": item.color or ""
                })
            nodes_data.append(node_data)

        edges_data = []
        for edge in self.edges.all():
            edges_data.append({
                "id": edge.edge_id,
                "source": str(edge.source_node.node_id),
                "target": str(edge.target_node.node_id)
            })

        return json.dumps({
            "nodes": nodes_data,
            "edges": edges_data
        })


class WorkflowNode(models.Model):
    """
    Represents a single node in a workflow.
    Node types: eventNode, agentNode, connectorNode, actionNode, logicNode
    """
    NODE_TYPE_CHOICES = [
        ('eventNode', 'Event Node'),
        ('agentNode', 'Agent Node'),
        ('connectorNode', 'Connector Node'),
        ('actionNode', 'Action Node'),
        ('logicNode', 'Logic Node'),
    ]

    workflow = models.ForeignKey(
        Workflow,
        on_delete=models.CASCADE,
        related_name='nodes'
    )
    node_id = models.CharField(max_length=50, help_text="Unique ID within the workflow")
    node_type = models.CharField(
        max_length=20,
        choices=NODE_TYPE_CHOICES,
        default='connectorNode'
    )
    label = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True, null=True)
    
    # Icon configuration
    icon_slug = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="SimpleIcons slug (e.g., 'whatsapp', 'openai', 'slack')"
    )
    icon_color = models.CharField(
        max_length=10, 
        blank=True, 
        null=True,
        help_text="Hex color without # (e.g., '25D366')"
    )
    icon_alt = models.CharField(max_length=100, blank=True, null=True)

    # Position for desktop layout
    pos_desktop_x = models.IntegerField(default=140)
    pos_desktop_y = models.IntegerField(default=140)

    # Position for mobile layout
    pos_mobile_x = models.IntegerField(default=140)
    pos_mobile_y = models.IntegerField(default=140)

    class Meta:
        ordering = ['node_id']
        unique_together = ['workflow', 'node_id']
        verbose_name = 'Workflow Node'
        verbose_name_plural = 'Workflow Nodes'

    def __str__(self):
        return f"{self.workflow.name} - {self.label} ({self.node_id})"


class WorkflowNodeItem(models.Model):
    """
    Represents an item/integration within a connector node.
    Used to display multiple service icons within a single node.
    """
    node = models.ForeignKey(
        WorkflowNode,
        on_delete=models.CASCADE,
        related_name='items'
    )
    slug = models.CharField(
        max_length=100,
        help_text="SimpleIcons slug (e.g., 'googlecalendar', 'slack')"
    )
    name = models.CharField(max_length=100)
    color = models.CharField(
        max_length=10, 
        blank=True, 
        null=True,
        help_text="Hex color without # (e.g., '1A73E8')"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Node Item'
        verbose_name_plural = 'Node Items'

    def __str__(self):
        return f"{self.node.label} - {self.name}"


class WorkflowEdge(models.Model):
    """
    Represents a connection/edge between two nodes in a workflow.
    """
    workflow = models.ForeignKey(
        Workflow,
        on_delete=models.CASCADE,
        related_name='edges'
    )
    edge_id = models.CharField(max_length=50, help_text="Unique edge ID (e.g., 'e1-2')")
    source_node = models.ForeignKey(
        WorkflowNode,
        on_delete=models.CASCADE,
        related_name='outgoing_edges'
    )
    target_node = models.ForeignKey(
        WorkflowNode,
        on_delete=models.CASCADE,
        related_name='incoming_edges'
    )

    class Meta:
        ordering = ['edge_id']
        unique_together = ['workflow', 'edge_id']
        verbose_name = 'Workflow Edge'
        verbose_name_plural = 'Workflow Edges'

    def __str__(self):
        return f"{self.workflow.name}: {self.source_node.label} -> {self.target_node.label}"


class WorkflowPageSEO(models.Model):
    """
    SEO settings for the workflows page.
    """
    meta_title = models.CharField(max_length=200, blank=True, null=True)
    meta_description = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        verbose_name = 'Workflow Page SEO'
        verbose_name_plural = 'Workflow Page SEO'

    def __str__(self):
        return self.meta_title or "Workflow Page SEO"
