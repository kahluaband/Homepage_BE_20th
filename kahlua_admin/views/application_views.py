from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from application.models import ApplyForm  # "application"은 지원서를 만드는 모델이 있는 앱 이름입니다.
from ..serializers.application_serializers import ApplyFormListSerializer

class ApplicationsPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'

# 지원서 어드민 페이지에서 볼 수 있게
class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = ApplyForm.objects.all().order_by('-id') # 최근에 지원한 순으로 정렬
    serializer_class = ApplyFormListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ApplicationsPagination
    
    @swagger_auto_schema(
        operation_id='지원서 리스트 전체 또는 세션별로 가져오기',
        operation_description='''
            모든 지원서 또는 세션별 지원서를 리스트로 불러옵니다.<br/>
            기본 정렬은 최신이 가장 위로 올라오고 모든 지원서가 보이도록 정렬됩니다.<br/>
            query params에서 name을 True로 설정하면 이름 순으로 정렬됩니다.<br/>
            query params에서 first_preference를 보컬, 드럼, 베이스, 신디, 기타 등으로 설정하면 해당 세션을 1지망으로 선택한 지원서들이 정렬됩니다.<br/>
        ''',
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json": {
                        "status": "success",
                        "data": {
                            "id": 1,
                            "created": "2024-01-10T12:32:09.198136Z",
                            "updated": "2024-01-10T12:32:09.198178Z",
                            "name": "kahlua",
                            "phone_num": "01012345678",
                            "birthdate": "20050101",
                            "gender": "남성",
                            "address": "서울 마포구",
                            "first_preference": "보컬",
                            "second_preference": "드럼",
                            "play_instrument": "통기타",
                            "motive": "깔루아 들어가고 싶습니다!",
                        },
                    }
                }
            ),
            "400": openapi.Response(
                description="Bad Request",
            ),
        }
    )

    def list(self, request, *args, **kwargs):
        order = self.get_queryset()

        order_name = request.GET.get('name', False)
        if order_name:
            order = ApplyForm.objects.all().order_by('name')
        serializer = self.get_serializer(order, many=True)

        first_preference = request.GET.get('first_preference', False)
        if first_preference:
            order = order.filter(first_preference=first_preference)
        serializer = self.get_serializer(order, many=True)

        return Response({
            'status': 'Success',
            'data': serializer.data,
        }, status=status.HTTP_200_OK)
