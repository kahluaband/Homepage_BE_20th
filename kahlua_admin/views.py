from django.shortcuts import render


from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from application.models import ApplyForm  # "application"은 지원서를 만드는 모델이 있는 앱 이름입니다.
from application.serializers import ApplyFormCreateSerializer

# 지원한 애들 정보 관리자페이지에서 볼 수 있게
class ApplicationRetrieveView(APIView):
    queryset = ApplyForm.objects.all()
    serializer_class = ApplyFormCreateSerializer
    permission_classes = (AllowAny, )
    
    @swagger_auto_schema(
        operation_id='지원서 조회 View',
        operation_description='''
            지원서 작성 후 지원서 정보를 조회할 화면을 표시할 때 사용됩니다.<br/>
            주문 번호에 해당하는 지원서 화면을 보여줍니다.<br/>
        ''',
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json": {
                        "status": "success",
                        "data": {'id': 1,
                                 'name':'깔루아1',
                                 'phone_num':'010-6337-5958',
                                 'birthdate':'2002-05-31',
                                 'gender': '여성',
                                 'address': '서울특별시 마포구',
                                 'first_preference': '기타',
                                 'second_preference': '신디',
                                 'play_instrument': '기타는 1년 정도 독학했습니다.',
                                 'motive': '깔루아와 함께 즐거운 대학생활을 하고 싶습니다.',
                                }
                    }
                }
            ),
            "400": openapi.Response(
                description="Bad Request",
            ),
        }
    )
    def get(self, request):
            order_id = request.query_params.get('order_id')
            order = ApplyForm.objects.get(id=order_id)
            serializer = self.get_serializer(order)
            
            return Response({
                    'status': 'success',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)