from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token
from rest_framework import serializers

from main.models import Company
from main.models import Review


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ('name')


class UserSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=150)
    email = serializers.CharField(max_length=150, allow_blank=True)


class TokenSerializer(serializers.Serializer):

    user = UserSerializer()
    key = serializers.CharField(max_length=200)


class CompanyReviewSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=1000)


class ReviewSerializer(serializers.ModelSerializer):

    company = CompanyReviewSerializer()
    reviewer = TokenSerializer()

    class Meta:
        model = Review
        fields = ('rating', 'title', 'summary', 'ip_address', 'submission_date', 'company', 'reviewer')

    def validate_company(self, validated_company):

        return Company.objects.get_or_create(
            name=validated_company['name'])

    def validate_reviewer(self, validated_reviewer):

        user = User.objects.get(
            username=validated_reviewer['user']['username'],
            email=validated_reviewer['user']['email'])
        return Token.objects.get(user=user)