from django.shortcuts import get_object_or_404
from rest_framework import serializers
from application.models import ApplyForm

class ApplyFormListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyForm
        ordering = ['-id']  # 최신순으로 정렬
        fields = '__all__' # 모두 다 가지고 오기
        # fields = [ # 'name', 'phone_num', 'birthdate', 'first_preference', 'second_preference'만 가져오기
        #     'name', 
        #     'phone_num', 
        #     'birthdate', 
        #     'first_preference', 
        #     'second_preference',
        # ]

class ApplyFormDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyForm
        ordering = ['-id']  # 최신순으로 정렬
        fields = '__all__' # 모두 다 가지고 오기