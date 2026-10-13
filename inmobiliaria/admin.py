from django.contrib import admin
from .models import Comuna, Propiedad

# 1. Gestión InLine[cite: 3]
class PropiedadInline(admin.TabularInline):
    model = Propiedad
    extra = 1

@admin.register(Comuna)
class ComunaAdmin(admin.ModelAdmin):
    # Solo campos que pertenecen a Comuna[cite: 2, 3]
    list_display = ('nombre', 'codigo_clasificacion', 'region', 'total_propiedades_asociadas')
    inlines = [PropiedadInline] 

    @admin.display(description='Total Propiedades')
    def total_propiedades_asociadas(self, obj):
        return obj.propiedades.count()

@admin.register(Propiedad)
class PropiedadAdmin(admin.ModelAdmin):
    # Solo campos que pertenecen a Propiedad[cite: 2, 3]
    list_display = ('codigo_propiedad', 'direccion', 'comuna', 'tipo_propiedad', 'precio_arriendo', 'disponible')
    search_fields = ('codigo_propiedad', 'direccion', 'comuna__nombre', 'comuna__codigo_clasificacion')
    list_filter = ('disponible', 'tipo_propiedad', 'comuna', 'comuna__codigo_clasificacion')
    list_editable = ('disponible', 'precio_arriendo')
    actions = ['marcar_disponible', 'marcar_arrendado']

    @admin.action(description='Marcar como Disponible')
    def marcar_disponible(self, request, queryset):
        actualizados = queryset.update(disponible=True)
        self.message_user(request, f"{actualizados} propiedades marcadas como disponibles.")

    @admin.action(description='Marcar como Arrendado')
    def marcar_arrendado(self, request, queryset):
        actualizados = queryset.update(disponible=False)
        self.message_user(request, f"{actualizados} propiedades marcadas como arrendadas.")