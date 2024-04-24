from rest_framework import serializers
from users.models import User


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('phone_number',)
        model = User
        read_only_fields = ('referral_code', 'invite_code')


class UserSerializer(serializers.ModelSerializer):
    referred_users = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('phone_number', 'referral_code', 'referred_users', 'invite_code')
        read_only_fields = ('referral_code', 'referred_users')

    def get_referred_users(self, obj):
        referred_users_filter = User.objects.filter(
            invite_code=obj.referral_code)
        referred_users = [str(user) for user in referred_users_filter]
        return referred_users

    def validate_invite_code(self, invite_code):
        inviter = User.objects.filter(referral_code=invite_code)

        if not inviter:
            raise serializers.ValidationError('Неверный код')
        return invite_code