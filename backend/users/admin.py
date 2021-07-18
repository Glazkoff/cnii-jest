from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from admin_interface.models import Theme
from .models import CustomUser
from django.utils.safestring import mark_safe


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'surname', 'name', 'patricity', 'organization')
    list_display_links = ('id', 'surname', 'name', 'patricity',)
    search_fields = ('surname', 'name', 'patricity',)
    list_filter = ('organization',)
    readonly_fields = ['id', 'passport_part1_scan_image',
                       'passport_part2_scan_image', ]

    def passport_part1_scan_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.passport_part1_scan.url,
            width=obj.passport_part1_scan.width,
            height=obj.passport_part1_scan.height,
        ))
    passport_part1_scan_image.short_description = "Скан паспорта (часть 1) - изображение"

    def passport_part2_scan_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.passport_part2_scan.url,
            width=obj.passport_part2_scan.width,
            height=obj.passport_part2_scan.height,
        ))
    passport_part2_scan_image.short_description = "Скан паспорта (часть 2) - изображение"


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Theme)

admin.site.site_header = "Админпанель системы ЦНИИ Русского жестового языка"
admin.site.site_title = "Админпанель ЦНИИ Русского жестового языка"
admin.site.index_title = "Административная часть сайта ЦНИИ Русского жестового языка"
