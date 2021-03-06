import datetime
from django.db import models
from django.contrib.auth.models import User


def year_choices():
    choices = ()
    for r in range(1950, datetime.date.today().year+1):
        choices = choices+((r, r),)
    return tuple(choices)


def current_year():
    return datetime.date.today().year


class CustomUser(models.Model):
    """Пользователь"""
    SEX_CHOICES = (("N", "Не указан"), ("M", "Мужской"), ("F", "Женский"))
    user = models.OneToOneField(
        User, verbose_name="Пользователь", on_delete=models.CASCADE)
    surname = models.CharField("Фамилия", max_length=150, blank=True)
    name = models.CharField("Имя", max_length=150, blank=True)
    patricity = models.CharField("Отчество", max_length=150, blank=True)
    birthday = models.DateField("Дата рождения", blank=True, null=True)
    sex = models.CharField(verbose_name="Пол", max_length=1,
                           choices=SEX_CHOICES, default="N", blank=False)
    photo = models.ImageField(verbose_name="Загрузка фото",
                              upload_to='photo', blank=True)
    native_language = models.CharField(
        "Родной язык", max_length=150, blank=True)
    citizenship = models.CharField("Гражданство", max_length=150, blank=True)
    martial_status = models.CharField(
        "Семейное положение", max_length=150, blank=True)
    organization = models.CharField("Организация", max_length=150, blank=True)
    job_position = models.CharField(
        "Занимаемая должность", max_length=150, blank=True)
    # TODO: запрашиваемая категория аттестации
    # TODO: Заявленная сфера деятельности FK
    education = models.CharField("Образование", max_length=150, blank=True)
    main_diploma_scan = models.ImageField(verbose_name="Скан диплома об образовании",
                                          upload_to='main_diploma', blank=True)
    gesture_diploma_scan = models.ImageField(verbose_name="Скан диплома о подготовке по жестовому языку",
                                             upload_to='gesture_diploma', blank=True)
    home_address = models.CharField(
        "Домашний адрес", max_length=150, blank=True)
    passport = models.CharField("Данные паспорта", max_length=150, blank=True)
    passport_part1_scan = models.ImageField(verbose_name="Скан паспорта (часть 1)",
                                            upload_to='passport_part1', blank=True)
    passport_part2_scan = models.ImageField(verbose_name="Скан паспорта (часть 2)",
                                            upload_to='passport_part2', blank=True)
    email = models.EmailField("E-mail", max_length=150, blank=True)
    personal_phone = models.CharField(
        "Мобильный телефон", max_length=150, blank=True)
    home_phone = models.CharField(
        "Домашний телефон", max_length=150, blank=True)
    work_phone = models.CharField(
        "Рабочий телефон", max_length=150, blank=True)
    full_work_experience_start_year = models.IntegerField(
        "Год начала трудовой деятельности", choices=year_choices(), default=current_year(), blank=True)
    current_job_experience_start_year = models.IntegerField(
        "Год начала текущей трудовой деятельности", choices=year_choices(), default=current_year(), blank=True)
    awards = models.TextField("Наличие наград", blank=True)
    training = models.TextField("Повышение квалификации", blank=True)
    organization_membership = models.TextField(
        "Членство в организациях", blank=True)
    characteristic = models.ImageField(verbose_name="Характеристика",
                                       upload_to='characteristic', blank=True)
    employment_history = models.FileField(
        verbose_name="Заверенная копия трудовой книжки (все страницы)", upload_to='employment_history', blank=True, help_text="Прикрепите документ в формате pdf")
    attestation_certificate_number = models.CharField(
        "Номер сертификата аттестации", max_length=150, blank=True)
    attestation_certificate_date = models.DateField(
        "Дата выдачи сертификата аттестации", blank=True, null=True)
    attestation_certificate_scan = models.ImageField(verbose_name="Скан сертификата аттестации",
                                                     upload_to='attestation_certificate', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.surname + " " + self.name)

    class Meta:
        # db_table = 'CustomUser'
        managed = True
        verbose_name = 'Пользователь системы'
        verbose_name_plural = 'Пользователи системы'


class Request(models.Model):
    """Заявка"""
    STATUS_CHOICES = (("step_1", "Шаг 1"), ("step_2", "Шаг 2"),
                      ("step_3", "Шаг 3"), ("step_4", "Шаг 4"), ("step_5", "Шаг 5"), ("step_6", "Шаг 6"), ("on_check", "Отправлена на проверку"), ("canceled", "Отклонена"), ("returned", "Возвращена на доработку"), ("confirmed", "Успешно подтверждена"), ("completed", "Завершена работа"))
    user = models.ForeignKey(
        CustomUser, verbose_name="Пользователь",
        related_name='custom_user', on_delete=models.CASCADE)
    status = models.CharField(verbose_name="Статус заявки", max_length=9,
                              choices=STATUS_CHOICES, default="step_1")
    is_paid = models.BooleanField(verbose_name="Оплачена ли", default=False)
    cheque = models.ImageField(verbose_name="Чек об оплате организационного взноса",
                               upload_to='cheque', blank=True)
    comment = models.TextField(verbose_name="Комментарий", blank=True)
    created_at = models.DateTimeField(
        verbose_name="Когда создана", auto_now_add=True)
    updated_at = models.DateTimeField(
        verbose_name="Когда обновлена последний раз", auto_now=True)

    def __str__(self):
        return str(f"Заявка #{self.id}")

    class Meta:
        # db_table = 'CustomUser'
        managed = True
        verbose_name = 'Заявка на аттестацию'
        verbose_name_plural = 'Заявки на аттестацию'


class RequestRegister(models.Model):
    """Заявка в реестре"""
    request = models.ForeignKey(
        Request, verbose_name="Заявка",
        related_name='request', on_delete=models.CASCADE)
    order = models.IntegerField("Порядковый номер")
    request_number = models.CharField(
        verbose_name="Номер заявки", max_length=11)

    def request_number(self):
        additional_nulls = ""
        if self.order < 10:
            additional_nulls += "00"
        elif self.order < 100:
            additional_nulls += "0"
        return "06-10-"+additional_nulls+str(self.order)
    request_number.short_description = "Номер заявки"

    def __str__(self):
        additional_nulls = ""
        if self.order < 10:
            additional_nulls += "00"
        elif self.order < 100:
            additional_nulls += "0"
        return "Заявка 06-10-"+additional_nulls+str(self.order)

    class Meta:
        managed = True
        verbose_name = 'Заявка в реестре'
        verbose_name_plural = 'Реестр заявок'


class LastRequestOrder(models.Model):
    """Настроки реестра"""
    last_order = models.IntegerField("Последний порядковый номер", default=0)

    class Meta:
        managed = True
        verbose_name = 'Настроки реестра'
        verbose_name_plural = 'Настроки реестра'

    def __str__(self):
        return str(f"Последний порядковый номер: {self.last_order}")
