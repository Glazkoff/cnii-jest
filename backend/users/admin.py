from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from admin_interface.models import Theme
from .models import CustomUser, Request
from django.utils.safestring import mark_safe
from django.utils.html import format_html


class CustomUserAdmin(admin.ModelAdmin):

    list_display_links = ('id', 'surname', 'name', 'patricity',)
    search_fields = ('surname', 'name', 'patricity',)
    list_filter = ('organization',)
    readonly_fields = ['id', 'photo_image', 'passport_part1_scan_image',
                       'passport_part2_scan_image', ]

    def photo_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.photo.url,
            width=obj.photo.width,
            height=obj.photo.height,
        ))
    photo_image.short_description = "Фото"

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

    def action_set(self, obj):
        tag_string = ""
        tag_string += f'<a target="_blank" style="margin-bottom: 1rem;" href="/api/documents/">Сформировать заявление на аттестацию</a>'
        return format_html(tag_string)
    action_set.short_description = "Действия"
    list_display = ('id', 'surname', 'name', 'patricity',
                    'organization', 'action_set')


class RequestsAdmin(admin.ModelAdmin):
    list_display = ("request_number", "user", "status",
                    "created_at", "updated_at")
    list_filter = ('status',)

    class Meta:
        model = Request


admin.site.register(Request, RequestsAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Theme)

admin.site.site_header = "Админпанель системы ЦНИИ Русского жестового языка"
admin.site.site_title = "Админпанель системы ЦНИИ Русского жестового языка"
admin.site.index_title = "Административная часть сайта ЦНИИ Русского жестового языка"
