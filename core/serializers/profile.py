
from rest_framework import serializers
from core.models import Profile



class ProfileSerializer(serializers.ModelSerializer):

    email = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["public_key", "email", "name"]

    def get_email(self, obj):
        return obj.user.email