from django.shortcuts import get_object_or_404
from rest_framework import serializers
from tickets.models import FreshmanTicket, OrderTransaction

class FreshmanAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreshmanTicket
        ordering = ['-id']  # 최신순으로 정렬
        fields = [
            'id',
            'buyer',
            'phone_num',
            'count',
            'major',
            'student_id',
            'meeting',
            'reservation_id',
        ]


class GeneralTicketAdminListSerializer(serializers.ModelSerializer):
    buyer = serializers.SerializerMethodField()
    phone_num = serializers.SerializerMethodField()
    member = serializers.SerializerMethodField()
    participants = serializers.SerializerMethodField()

    class Meta:
        model = OrderTransaction
        ordering = ['-id']
        fields = [
            'id',
            'buyer',
            'phone_num',
            'member',
            'merchant_order_id',
            'transaction_status',
            'participants',
        ]

    def get_buyer(self, obj):
        '''
            티켓의 구매자를 알려주기 위한 함수
        '''
        ticket = obj.order
        return ticket.buyer
    
    def get_phone_num(self, obj):
        '''
            티켓의 구매자를 알려주기 위한 함수
        '''
        ticket = obj.order
        return ticket.phone_num
    
    def get_member(self, obj):
        '''
            구매자가 결제한 인원을 알려주기 위한 함수
        '''
        ticket = obj.order
        return ticket.member
    
    def get_participants(self, obj):
        '''
            구매자가 구매한 티켓의 참석자를 알려주기 위한 함수
        '''
        participants_list = []
        for participant in obj.order.participants.all():
            participants_list.append({'name': participant.name, 'phone_num': participant.phone_num})
        return participants_list