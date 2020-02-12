from rest_framework import serializers

from user.models import UserInfo


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        # fields = '__all__'
        fields = ('id', 'username', 'password', 'user_type', 'language', 'create_time', 'update_time')
