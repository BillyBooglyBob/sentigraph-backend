from django.contrib import admin

from .models import Company, RawTweet, ClassifiedTweet, Aspect, CompanyAspectSentiment

admin.site.register(Company)
admin.site.register(RawTweet)
admin.site.register(ClassifiedTweet)
admin.site.register(Aspect)
admin.site.register(CompanyAspectSentiment)
