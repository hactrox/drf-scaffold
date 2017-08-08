from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from ..models import Test
from .serializers import (
    TestListSerializer,
    UserCreateSerializer
)


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestListSerializer
    permission_classes = (AllowAny,)


class UserCreateView(generics.CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
