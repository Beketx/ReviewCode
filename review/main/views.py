from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework.response import Response

from main.serializers import CompanySerializer, ReviewSerializer
from main.models import Company
from main.models import Review

class CompanyViewSet(viewsets.ModelViewSet):

    http_method_names = ['get']
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    
class ReviewViewSet(viewsets.ViewSet):

    http_method_names = ['get', 'post']

    def list(self, request):

        reviwer = Token.objects.get(user=request.user)
        queryset = Review.objects.filter(reviewer=reviwer).order_by('submission_date')
        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):

        request_data = request.data
        request_data['reviewer'] = {'user': {'username': request.user.username, 'email': request.user.email}, 'key': '-'}

        request_data['ip_address'] = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR')).split(',')[0]
            
        serializer = ReviewSerializer(data=request_data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=500)
        serializer.save()
        return Response(serializer.data, status=201)
        