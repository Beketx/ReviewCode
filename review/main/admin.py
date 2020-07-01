from django.contrib import admin

from rest_framework.authtoken.models import Token
from main.models import Company
from main.models import Review

class ReviewAdmin(admin.ModelAdmin):

    def get_queryset(self, request):

        query = super(ReviewAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return query.filter(reviewer=Token.objects.get(user=request.user))
        else:
            return query


admin.site.register(Company)
admin.site.register(Review, ReviewAdmin)