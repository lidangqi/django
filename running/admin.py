from django.contrib import admin

# Register your models here.

from .models import Continents, Countries, Area, States, Cities, Regions

class ReadOnlyAdmin(admin.ModelAdmin):
    readonly_fields = []

    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
            [field.name for field in obj._meta.fields] + \
            [field.name for field in obj._meta.many_to_many]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

@admin.register(Continents)
class ContinentsAdmin(ReadOnlyAdmin):
    search_fields = ('cname', 'name',)

@admin.register(Countries)
class CountriesAdmin(ReadOnlyAdmin):
    search_fields = ('cname', 'name',)

@admin.register(Area)
class AreaAdmin(ReadOnlyAdmin):
    search_fields = ('cname', 'name',)

@admin.register(States)
class StatesAdmin(ReadOnlyAdmin):
    search_fields = ('cname', 'name',)

@admin.register(Cities)
class CitiesAdmin(admin.ModelAdmin):
    search_fields = ('cname', 'name',)
    list_display = ('cname', 'name', 'city_id', 'state_id', 'code', 'lower_name', 'code_full')
    autocomplete_fields = ['state_id', ]

@admin.register(Regions)
class RegionsAdmin(admin.ModelAdmin):
    search_fields = ('cname', 'name',)
    list_display = ('id', 'city_id', 'code', 'name', 'cname', 'lower_name', 'code_full')
    autocomplete_fields = ['city_id', ]
