from django.core.management.base import BaseCommand
from workflows.models import Workflow, WorkflowNode, WorkflowNodeItem, WorkflowEdge


class Command(BaseCommand):
    help = 'Creates a sample workflow with nodes and edges for users to learn from'

    def handle(self, *args, **options):
        # Check if sample workflow already exists
        if Workflow.objects.filter(slug='sample-whatsapp-ai-workflow').exists():
            self.stdout.write(self.style.WARNING('Sample workflow already exists. Skipping creation.'))
            return
        
        # Create the sample workflow
        workflow = Workflow.objects.create(
            name='Sample WhatsApp AI Workflow',
            description='A sample workflow demonstrating an AI-powered WhatsApp automation with integrations. Use this as a template for your own workflows.',
            is_active=True
        )
        
        self.stdout.write(f'Created workflow: {workflow.name}')
        
        # Create nodes based on the sample flow-data.json
        nodes_data = [
            {
                'node_id': '1',
                'node_type': 'eventNode',
                'label': 'WhatsApp Incoming Message',
                'description': 'Starts when a message arrives',
                'icon_slug': 'whatsapp',
                'icon_color': '25D366',
                'icon_alt': 'WhatsApp',
                'pos_desktop_x': 530,
                'pos_desktop_y': -350,
                'pos_mobile_x': 59,
                'pos_mobile_y': -53,
            },
            {
                'node_id': '2',
                'node_type': 'agentNode',
                'label': 'AI Agent',
                'description': 'Process with AI',
                'icon_slug': 'openai',
                'icon_color': 'ffffff',
                'icon_alt': 'OpenAI',
                'pos_desktop_x': 398,
                'pos_desktop_y': 202,
                'pos_mobile_x': 140,
                'pos_mobile_y': 300,
            },
            {
                'node_id': '6',
                'node_type': 'agentNode',
                'label': 'Multi-Agent',
                'description': 'Orchestrated AI',
                'icon_slug': 'openai',
                'icon_color': 'ffffff',
                'icon_alt': 'OpenAI',
                'pos_desktop_x': 430,
                'pos_desktop_y': 506,
                'pos_mobile_x': 272,
                'pos_mobile_y': 465,
            },
            {
                'node_id': '4',
                'node_type': 'logicNode',
                'label': 'Business Logic',
                'description': 'Route based on rules',
                'icon_slug': '',
                'icon_color': '',
                'icon_alt': 'Business Logic',
                'pos_desktop_x': 778,
                'pos_desktop_y': 86,
                'pos_mobile_x': 17,
                'pos_mobile_y': 520,
            },
            {
                'node_id': '3',
                'node_type': 'connectorNode',
                'label': 'Integrations',
                'description': 'Popular services',
                'icon_slug': '',
                'icon_color': '',
                'icon_alt': 'Integrations',
                'pos_desktop_x': 586,
                'pos_desktop_y': 850,
                'pos_mobile_x': 367,
                'pos_mobile_y': 754,
                'items': [
                    {'slug': 'googlecalendar', 'name': 'Google Calendar', 'color': '1A73E8'},
                    {'slug': 'googlesheets', 'name': 'Google Sheets', 'color': '0F9D58'},
                    {'slug': 'slack', 'name': 'Slack', 'color': '4A154B'},
                    {'slug': 'stripe', 'name': 'Stripe', 'color': '635BFF'},
                    {'slug': 'github', 'name': 'GitHub', 'color': '181717'},
                    {'slug': 'gmail', 'name': 'Gmail', 'color': 'EA4335'},
                ]
            },
            {
                'node_id': '5',
                'node_type': 'actionNode',
                'label': 'Execute Action',
                'description': 'Perform task',
                'icon_slug': '',
                'icon_color': '',
                'icon_alt': 'Execute Action',
                'pos_desktop_x': 752,
                'pos_desktop_y': 340,
                'pos_mobile_x': 80,
                'pos_mobile_y': 791,
            },
            {
                'node_id': '7',
                'node_type': 'eventNode',
                'label': 'Reply to message',
                'description': 'Send response',
                'icon_slug': 'whatsapp',
                'icon_color': '25D366',
                'icon_alt': 'WhatsApp',
                'pos_desktop_x': 912,
                'pos_desktop_y': 592,
                'pos_mobile_x': 99,
                'pos_mobile_y': 1009,
            },
        ]
        
        # Create nodes
        node_map = {}
        for node_data in nodes_data:
            items = node_data.pop('items', [])
            node = WorkflowNode.objects.create(workflow=workflow, **node_data)
            node_map[node_data['node_id']] = node
            
            # Create items for connector nodes
            for idx, item in enumerate(items):
                WorkflowNodeItem.objects.create(
                    node=node,
                    slug=item['slug'],
                    name=item['name'],
                    color=item['color'],
                    order=idx
                )
            
            self.stdout.write(f'  Created node: {node.label}')
        
        # Create edges
        edges_data = [
            {'edge_id': 'e1-2', 'source': '1', 'target': '2'},
            {'edge_id': 'e2-6', 'source': '2', 'target': '6'},
            {'edge_id': 'e2-4', 'source': '2', 'target': '4'},
            {'edge_id': 'e6-3', 'source': '6', 'target': '3'},
            {'edge_id': 'e4-5', 'source': '4', 'target': '5'},
            {'edge_id': 'e6-5', 'source': '6', 'target': '5'},
            {'edge_id': 'e5-7', 'source': '5', 'target': '7'},
        ]
        
        for edge_data in edges_data:
            WorkflowEdge.objects.create(
                workflow=workflow,
                edge_id=edge_data['edge_id'],
                source_node=node_map[edge_data['source']],
                target_node=node_map[edge_data['target']]
            )
            self.stdout.write(f'  Created edge: {edge_data["edge_id"]}')
        
        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully created sample workflow with {len(nodes_data)} nodes and {len(edges_data)} edges!'))
        self.stdout.write(f'View it at: /cpanel/workflows/edit/{workflow.slug}/')
