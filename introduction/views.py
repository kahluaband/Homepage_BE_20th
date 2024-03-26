from django.shortcuts import render
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from rest_framework import viewsets, status
# from .models import IntroImageUpload
# from .serializers import IntroImageSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


# Create your views here.

# class IntroImageView(viewsets.ModelViewSet):
#     permission_classes = (IsAuthenticated,)

def image_view(request, image_name):
    storage = S3Boto3Storage()
    file = storage.open(image_name)
    # serializer = self.IntroImageSerializer(data=request.data)
    # serializer.is_valid(raise_exception=True)
    # data = serializer.validated_data

    # image_location = settings.MEDIA_URL + data.image.title

    return Response({
            'data': file
        },status=status.HTTP_200_OK)