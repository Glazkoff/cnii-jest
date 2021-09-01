from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from admin_interface.models import Theme
from .models import CustomUser, Request, RequestRegister, LastRequestOrder
from django.utils.safestring import mark_safe
from django.utils.html import format_html
import math

new_width = 450


class RequestInline(admin.TabularInline):
    list_display = ['request_number', "request_number", "status", "is_paid",
                    "created_at", "updated_at"]
    model = Request
    extra = 0


class CustomUserAdmin(admin.ModelAdmin):

    list_display = ('id', 'surname', 'name', 'patricity',
                    'organization', 'action_set')
    list_display_links = ('id', 'surname', 'name', 'patricity',)
    list_filter = ('organization',)
    search_fields = ('surname', 'name', 'patricity',)
    readonly_fields = ['id', 'photo_image', 'main_diploma_scan_image', 'gesture_diploma_scan_image', 'passport_part1_scan_image',
                       'passport_part2_scan_image', 'characteristic_image', 'employment_history_frame', 'attestation_certificate_scan_image', 'requests_set']
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
        ("Заявки", {
            'fields': ('requests_set',)}),
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

    def requests_set(self, obj):
        link_set_string = "<table> \
            <tr><th>Ссылка</th><th>Статус</th><th>Оплачена</th><th>Комментарий</th></tr>"
        requests = Request.objects.filter(user=obj)
        for request in requests:

            register = RequestRegister.objects.filter(request=request)
            try:
                if register[0] is not None:
                    additional_nulls = ""
                    if register[0].order < 10:
                        additional_nulls += "00"
                    elif register[0].order < 100:
                        additional_nulls += "0"
                    register_number = "06-10-" + \
                        additional_nulls+str(register[0].order)
            except IndexError:
                register_number = "-"

            status = request.status
            is_paid = "Да" if request.is_paid else "Нет"
            comment = request.comment if request.comment != "" else "-"
            # switch:
            link_set_string += f'<tr><td><a target="_blank" style="margin-bottom: 1rem;" href="/api/documents/">{register_number}</a></td><td>{status}</td><td>{is_paid}</td><td>{comment}</td></tr>'

        link_set_string += "</table>"
        return format_html(link_set_string)
    requests_set.short_description = "Ссылки на заявки"


class RequestsAdmin(admin.ModelAdmin):
    list_display = ("id", "request_number", "user", "status", "is_paid",
                    "created_at", "updated_at")
    readonly_fields = ("request_number", "cheque_image")
    list_filter = ('status',)
    list_display_links = ("id", "request_number",)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('user',)
        else:
            return self.readonly_fields

    def cheque_image(self, obj):
        width = obj.cheque.width
        height = obj.cheque.height
        new_height = math.ceil((height*new_width) / width)
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.cheque.url,
            width=new_width,
            height=new_height
        ))
    cheque_image.short_description = "Изображение чека"

    def request_number(self, obj=None):
        try:
            register = RequestRegister.objects.filter(request=obj)
            if register[0] is not None:
                additional_nulls = ""
                if register[0].order < 10:
                    additional_nulls += "00"
                elif register[0].order < 100:
                    additional_nulls += "0"
                return "06-10-"+additional_nulls+str(register[0].order)
        except:
            return "-"
    request_number.short_description = "Номер в регистре"

    class Meta:
        model = Request


class RequestRegisterAdmin(admin.ModelAdmin):
    class Meta:
        model = RequestRegister


class LastRequestOrderAdmin(admin.ModelAdmin):
    class Meta:
        model = LastRequestOrder

    def has_add_permission(self, request, obj=None):
        return LastRequestOrder.objects.all().count() == 0


admin.site.register(Request, RequestsAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(RequestRegister, RequestRegisterAdmin)
admin.site.register(LastRequestOrder, LastRequestOrderAdmin)

admin.site.unregister(Theme)

admin.site.site_header = "Админпанель системы ЦНИИ Русского жестового языка"
admin.site.site_title = "Админпанель системы ЦНИИ Русского жестового языка"
admin.site.index_title = "Административная часть сайта ЦНИИ Русского жестового языка"
