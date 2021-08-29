from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from admin_interface.models import Theme
from .models import CustomUser, Request
from django.utils.safestring import mark_safe
from django.utils.html import format_html
import math

new_width = 450


class RequestInline(admin.TabularInline):
    model = Request
    extra = 0


class CustomUserAdmin(admin.ModelAdmin):

    list_display = ('id', 'surname', 'name', 'patricity',
                    'organization', 'action_set')
    list_display_links = ('id', 'surname', 'name', 'patricity',)
    list_filter = ('organization',)
    search_fields = ('surname', 'name', 'patricity',)
    readonly_fields = ['id', 'photo_image', 'main_diploma_scan_image', 'gesture_diploma_scan_image', 'passport_part1_scan_image',
                       'passport_part2_scan_image', 'characteristic_image', 'employment_history_frame', 'attestation_certificate_scan_image']
    fieldsets = (
        ("Шаг 1. Личные данные", {
            'classes': ('extrapretty'),
            'fields': ('user', 'surname', 'name', 'patricity', 'birthday', 'sex', 'photo', 'photo_image')
        }),
        ("Шаг 2. Общая информация", {
            'fields': ('native_language', 'citizenship', 'martial_status', 'organization', 'job_position', 'education', 'main_diploma_scan',
                       'main_diploma_scan_image',
                       'gesture_diploma_scan', 'gesture_diploma_scan_image')}),
        ("Шаг 3. Паспортные данные", {
            'fields': ('passport', 'passport_part1_scan', 'passport_part1_scan_image', 'passport_part2_scan', 'passport_part2_scan_image')}),
        ("Шаг 4. Контактные данные", {
            'fields': ('home_address', 'personal_phone', 'home_phone', 'work_phone')}),
        ("Шаг 5. Опыт работы и награды", {
            'fields': ('full_work_experience_start_year', 'current_job_experience_start_year', 'awards', 'training', 'organization_membership', 'characteristic',
                       'characteristic_image', 'employment_history', 'employment_history_frame')}),
        ("Шаг 6. Теоретическая часть аттестации", {
            'fields': ('attestation_certificate_number', 'attestation_certificate_date', 'attestation_certificate_scan', 'attestation_certificate_scan_image')}),
    )
    inlines = (RequestInline,)

    def photo_image(self, obj):
        width = obj.photo.width
        height = obj.photo.height
        new_height = math.ceil((height*new_width) / width)
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.photo.url,
            width=new_width,
            height=new_height
        ))
    photo_image.short_description = "Фото"

    def main_diploma_scan_image(self, obj):
        width = obj.main_diploma_scan.width
        height = obj.main_diploma_scan.height
        new_height = math.ceil((height*new_width) / width)
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.main_diploma_scan.url,
            width=new_width,
            height=new_height
        ))
    main_diploma_scan_image.short_description = "Диплом об образовании"

    def gesture_diploma_scan_image(self, obj):
        width = obj.gesture_diploma_scan.width
        height = obj.gesture_diploma_scan.height
        new_height = math.ceil((height*new_width) / width)
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.gesture_diploma_scan.url,
            width=new_width,
            height=new_height
        ))
    gesture_diploma_scan_image.short_description = "Диплом о подготовке по жестовому языку"

    def passport_part1_scan_image(self, obj):
        width = obj.passport_part1_scan.width
        height = obj.passport_part1_scan.height
        new_height = math.ceil((height*new_width) / width)
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.passport_part1_scan.url,
            width=new_width,
            height=new_height,
        ))
    passport_part1_scan_image.short_description = "Скан паспорта (часть 1) - изображение"

    def passport_part2_scan_image(self, obj):
        width = obj.passport_part2_scan.width
        height = obj.passport_part2_scan.height
        new_height = math.ceil((height*new_width) / width)
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.passport_part2_scan.url,
            width=new_width,
            height=new_height,
        ))
    passport_part2_scan_image.short_description = "Скан паспорта (часть 2) - изображение"

    def characteristic_image(self, obj):
        width = obj.characteristic.width
        height = obj.characteristic.height
        new_height = math.ceil((height*new_width) / width)
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.characteristic.url,
            width=new_width,
            height=new_height
        ))
    characteristic_image.short_description = "Характеристика"

    def employment_history_frame(self, obj):
        return mark_safe('<embed src="{url}" width="{width}" height={height} />'.format(
            url=obj.employment_history.url,
            width=new_width,
            height=300
        ))
    employment_history_frame.short_description = "Трудовая книжка (все страницы)"

    def attestation_certificate_scan_image(self, obj):
        width = obj.attestation_certificate_scan.width
        height = obj.attestation_certificate_scan.height
        new_height = math.ceil((height*new_width) / width)
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.attestation_certificate_scan.url,
            width=new_width,
            height=new_height
        ))
    attestation_certificate_scan_image.short_description = "Cертификат аттестации"

    def action_set(self, obj):
        tag_string = ""
        tag_string += f'<a target="_blank" style="margin-bottom: 1rem;" href="/api/documents/">Сформировать заявление на аттестацию</a>'
        return format_html(tag_string)
    action_set.short_description = "Действия"


class RequestsAdmin(admin.ModelAdmin):
    list_display = ("request_number", "user", "status", "is_paid",
                    "created_at", "updated_at")
    # readonly_fields = ("user",)
    list_filter = ('status',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('user',)
        else:
            return self.readonly_fields

    class Meta:
        model = Request


admin.site.register(Request, RequestsAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Theme)

admin.site.site_header = "Админпанель системы ЦНИИ Русского жестового языка"
admin.site.site_title = "Админпанель системы ЦНИИ Русского жестового языка"
admin.site.index_title = "Административная часть сайта ЦНИИ Русского жестового языка"
