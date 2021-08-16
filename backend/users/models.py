from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class CustomUser(models.Model):
    """Пользователь"""
    SEX_CHOICES = (("M", "Мужской"), ("F", "Женский"))
    user = models.OneToOneField(
        User, verbose_name="Пользователь", on_delete=models.CASCADE)
    surname = models.CharField("Фамилия", max_length=150, blank=True)
    name = models.CharField("Имя", max_length=150, blank=True)
    patricity = models.CharField("Отчество", max_length=150, blank=True)
    birthday = models.DateField("Дата рождения", blank=True, null=True)
    sex = models.CharField(verbose_name="Пол", max_length=1,
                           choices=SEX_CHOICES, blank=True)
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
    work_experience_full_years = models.IntegerField(
        "Стаж полных лет", blank=True, null=True)
    work_experience_current_job = models.IntegerField(
        "Стаж настоящей должности", blank=True, null=True)
    awards = models.TextField("Наличие наград", blank=True)
    training = models.TextField("Повышение квалификации", blank=True)
    organization_membership = models.TextField(
        "Членство в организациях", blank=True)
    characteristic = models.ImageField(verbose_name="Характеристика",
                                       upload_to='characteristic', blank=True)
    employment_history = models.FileField(
        verbose_name="Заверенная копия трудовой книжки (все страницы)", upload_to='employment_history', blank=True)
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
                      ("step_3", "Шаг 3"), ("step_4", "Шаг 4"), ("step_5", "Шаг 5"),("step_6", "Шаг 6"), ("on_check", "Отправлена на проверку"), ("canceled", "Отклонена"), ("confirmed", "Успешно подтверждена"), ("completed", "Завершена работа"))
    request_number = models.CharField(
        verbose_name="Номер заявки", max_length=10)
    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.CASCADE)
    status = models.CharField(verbose_name="Статус заявки", max_length=9,
                              choices=STATUS_CHOICES)
    created_at = models.DateTimeField(
        verbose_name="Когда создана", auto_now_add=True)
    updated_at = models.DateTimeField(
        verbose_name="Когда обновлена последний раз", auto_now=True)

    def request_number(self):
        additional_nulls = ""
        if self.id < 10:
            additional_nulls += "00"
        elif self.id < 100:
            additional_nulls += "0"
        return "06-10-"+additional_nulls+str(self.id)
    request_number.short_description = "Номер заявки"

    def __str__(self):
        return str(f"Заявка #{self.id}")

    class Meta:
        # db_table = 'CustomUser'
        managed = True
        verbose_name = 'Заявка на аттестацию'
        verbose_name_plural = 'Заявки на аттестацию'
