import channels.layers
from asgiref.sync import async_to_sync
from api.serializers import MessageSerializer
from api.models import Message
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Message)
def new_message_handler(sender, instance, **kwargs):
    serializer = MessageSerializer(instance, context={'request': None})
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)('chat', {
        'type': 'chat_message',
        'data': serializer.data
    })