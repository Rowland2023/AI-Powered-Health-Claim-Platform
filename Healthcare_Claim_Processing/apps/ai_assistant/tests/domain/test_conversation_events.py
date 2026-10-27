from uuid import uuid4

from ai_assistant.domain.entities.conversation import Conversation
from ai_assistant.domain.events.assistant_message_added import (
    AssistantMessageAdded,
)
from ai_assistant.domain.events.conversation_started import ConversationStarted
from ai_assistant.domain.events.user_message_added import UserMessageAdded


def test_start_records_conversation_started_event():
    user_id = uuid4()

    conversation = Conversation.start(user_id)

    assert len(conversation.domain_events) == 1

    event = conversation.domain_events[0]
    assert isinstance(event, ConversationStarted)
    assert event.conversation_id == conversation.id
    assert event.user_id == user_id
    assert event.aggregate_id == conversation.id
    assert event.event_name == "ConversationStarted"


def test_add_user_message_records_event():
    conversation = Conversation.start(uuid4())
    conversation.clear_domain_events()

    message = conversation.add_user_message("Hello")

    assert conversation.messages == (message,)
    assert len(conversation.domain_events) == 1

    event = conversation.domain_events[0]
    assert isinstance(event, UserMessageAdded)
    assert event.conversation_id == conversation.id
    assert event.message_id == message.id
    assert event.aggregate_id == conversation.id


def test_add_assistant_message_records_event():
    conversation = Conversation.start(uuid4())
    conversation.clear_domain_events()

    message = conversation.add_assistant_message("How can I help?")

    assert conversation.messages == (message,)
    assert len(conversation.domain_events) == 1

    event = conversation.domain_events[0]
    assert isinstance(event, AssistantMessageAdded)
    assert event.conversation_id == conversation.id
    assert event.message_id == message.id
    assert event.aggregate_id == conversation.id
