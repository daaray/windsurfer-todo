from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Max
from .models import Todo
from .serializers import TodoSerializer

# Create your views here.

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def perform_create(self, serializer):
        # Set the order to be the last item
        last_order = Todo.objects.all().aggregate(Max('order'))['order__max']
        order = (last_order or 0) + 1
        serializer.save(order=order)

    @action(detail=False, methods=['post'])
    def reorder(self, request):
        # Expect a list of {id: number, order: number}
        reorder_data = request.data
        
        # Validate input
        if not isinstance(reorder_data, list):
            return Response(
                {"error": "Expected a list of todos with order"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update orders
        for item in reorder_data:
            try:
                todo = Todo.objects.get(id=item['id'])
                todo.order = item['order']
                todo.save()
            except Todo.DoesNotExist:
                return Response(
                    {"error": f"Todo with id {item['id']} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            except KeyError:
                return Response(
                    {"error": "Each item must have id and order"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(status=status.HTTP_200_OK)
