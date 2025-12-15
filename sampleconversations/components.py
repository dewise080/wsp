import json
import uuid

from django_components import component


@component.register("sample_conversation")
class SampleConversation(component.Component):
    template_name = "sampleconversations/components/sample_conversation.html"

    def get_context_data(
        self,
        conversations=None,
        title="Sample Conversations",
        subtitle="Grab a prompt and see how the assistant replies.",
    ):
        default_conversations = [
            {
                "topic": "Launch messaging",
                "user_message": "Draft a short teaser for our upcoming release focused on reliability.",
                "assistant_message": "Here's a teaser that spotlights reliability and invites early access signups.",
                "tone": "Upbeat",
            },
            {
                "topic": "Support reply",
                "user_message": "Answer a customer asking whether we integrate with HubSpot.",
                "assistant_message": "Friendly confirmation plus a link to the integration guide and a CTA to book help.",
                "tone": "Helpful",
            },
        ]

        return {
            "title": title,
            "subtitle": subtitle,
            "conversations": conversations or default_conversations,
        }

    class Media:
        css = ["sampleconversations/sample_conversation.css"]
        js = ["sampleconversations/sample_conversation.js"]


@component.register("whatsapp_sim")
class WhatsappSimulator(component.Component):
    template_name = "sampleconversations/components/whatsapp_sim.html"

    def get_context_data(
        self,
        sample_text=None,
        primary_author="Ashwin",
        replay_type="word",
        title="WhatsApp Chat Simulator",
        subtitle="Replay a chat transcript with bundled styles and scripts.",
    ):
        default_text = (
            "21/11/14, 8:16 PM - Ashwin created group \"Whatsapp Simulator\"\n"
            "02/12/14, 7:13 PM - John: Hey! what's this?\n"
            "02/12/14, 7:08 PM - Ashwin: Hi There!\n"
            "02/12/14, 7:08 PM - Ashwin: Want to re-live some of those old conversations?\n"
            "02/12/14, 7:09 PM - Doe: Yeah, its pretty simple too!\n"
            "02/12/14, 7:10 PM - Siri: How so!?\n"
            "02/12/14, 7:11 PM - Ashwin: Just paste your chat in the menu\n"
            "02/12/14, 7:11 PM - Ashwin: Select who you are\n"
            "02/12/14, 7:11 PM - Ashwin: and hit play!!!\n"
            "02/12/14, 7:13 PM - Siri: 😱😱😱"
        )

        component_id = uuid.uuid4().hex[:8]
        text = sample_text or default_text

        return {
            "title": title,
            "subtitle": subtitle,
            "primary_author": primary_author,
            "replay_type": replay_type,
            "component_id": component_id,
            "sample_text_json": json.dumps(text),
        }

    class Media:
        css = [
            "whatsapp_sim/devices.min.css",
            "whatsapp_sim/whatsapp_sim.css",
        ]
        js = [
            "whatsapp_sim/WhatsappSimClass.js",
            "whatsapp_sim/whatsapp_sim_component.js",
        ]
