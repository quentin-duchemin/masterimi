from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from master_imi.permissions import IsOwner
from messaging.models import Conversation
from messaging.serializers import ConversationSerializer


class ConversationViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)
