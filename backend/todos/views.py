"""Views for Todo application."""

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Todo
from .serializers import TodoSerializer


class TodoViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing todo items."""

    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    @action(detail=False, methods=["post"])
    def reorder(self, request):
        """Reorder todos based on provided order values."""
        for item in request.data:
            Todo.objects.filter(id=item["id"]).update(order=item["order"])
        return Response(status=status.HTTP_200_OK)
