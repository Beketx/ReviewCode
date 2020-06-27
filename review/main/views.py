from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from main.serializers import CompanySerializer, ReviewSerializer
from main.models import Company
from main.models import Review
from rest_framework.views import APIView

class CompanyView(generics.ListAPIView):

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (IsAuthenticated,)


class ReviewView(APIView):

    def get(self, request):

        user_review = Token.objects.get(user=request.user)
        queryset = Review.objects.filter(reviewer=user_review)
        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):

        request_data = request.data
        request_data['reviewer'] = {'user': {'username': request.user.username, 'email': request.user.email},
                                    'key': '-'}
        request_data['ip_address'] = \
        request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR')).split(',')[0]
        serializer = ReviewSerializer(data=request_data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=404)
        serializer.save()
        return Response(serializer.data, status=200)