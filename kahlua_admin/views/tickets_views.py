from django.db.models import Q
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from tickets.models import FreshmanTicket, GeneralTicket, OrderTransaction, Participant
from ..serializers.tickets_serializers import FreshmanAdminSerializer, GeneralTicketAdminListSerializer


class TicketsPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'


class FreshmanViewSet(viewsets.ModelViewSet):
    queryset = FreshmanTicket.objects.all().order_by('-id')  #예약 순서대로 정렬
    serializer_class = FreshmanAdminSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TicketsPagination

    @swagger_auto_schema(
        operation_id='신입생 티켓 예약 리스트 가져오기',
        operation_description='''
            모든 신입생 티켓을 리스트로 불러옵니다.<br/>
            기본 정렬은 최신이 가장 위로 올라오도록 정렬됩니다. query params에서 name을 True로 설정하면 이름 순으로 정렬됩니다.<br/>
        ''',
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json": {
                        "status": "success",
                        "data": {
                            "total_count": 1,
                            "tickets": {
                                "id": 1,
                                "buyer": "kahlua",
                                "phone_num": "01012345678",
                                "major": "컴퓨터공학과",
                                "student_id": "C41111",
                                "meeting": True
                            },
                        }
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
            order = FreshmanTicket.objects.all().order_by('buyer')

        total_count = FreshmanTicket.objects.aggregate(count_sum=Sum('count'))['count_sum']

        serializer = self.get_serializer(order, many=True)

        return Response({
            'status': 'Success',
            'data': {
                'total_count': total_count,
                'tickets': serializer.data,
            },
        }, status=status.HTTP_200_OK)
    

class GeneralTicketListViewSet(viewsets.ModelViewSet):
    queryset = OrderTransaction.objects.all().order_by('-id')
    serializer_class = GeneralTicketAdminListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TicketsPagination

    @swagger_auto_schema(
        operation_id='일반 티켓 예매 정보 가져오기',
        operation_description='''
            모든 티켓을 리스트로 불러옵니다.<br/>
            기본 정렬은 최신이 가장 위로 올라오도록 정렬됩니다. query params에서 name을 True로 설정하면 이름 순으로 정렬됩니다.<br/>
        ''',
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json": {
                        "status": "success",
                        "data": {
                            "total_member": 1,
                            "tickets": {
                                "id": 1,
                                "buyer": "kahlua",
                                "phone_num": "01012345678",
                                "member": 2,
                                "merchant_order_id": "734ea4eadf",
                                "transaction_status": "paid"
                            },
                        }
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
            order = OrderTransaction.objects.all().order_by('order__buyer')

        total_member = GeneralTicket.objects.aggregate(member_sum=Sum('member'))['member_sum']

        serializer = self.get_serializer(order, many=True)

        return Response({
            'status': 'Success',
            'data': {
                'total_member': total_member,
                'tickets': serializer.data,
            },
        }, status=status.HTTP_200_OK)
