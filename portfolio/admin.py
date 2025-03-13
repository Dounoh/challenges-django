from django.contrib import admin
from portfolio.models import UserInfos,Competences,Experiences,Realisation,Contact

@admin.register(UserInfos)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(Competences)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(Experiences)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(Realisation)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Contact)
class AuthorAdmin(admin.ModelAdmin):
    pass

