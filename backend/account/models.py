from django.db import models
# Create your models here.


class ApplicationForm(models.Model):
    """Заявление на аттестацию"""
    application_id = models.AutoField(primary_key=True)
    # ИдентификаторПользователя
    # ИдентификаторЗапрашиваемойКатегории
    # ИдентификаторСферы Деятельности
    basis_for_certification = models.CharField(
        "Основание для аттестации", max_length=150)
    pass_certificate_scan_url = models.URLField(
        "URL свидетельства о прохождении")
    education_scan_url = models.URLField("URL документа об образовании")
    training_url = models.URLField("URL диплом о подготовке")
    is_draft = models.BooleanField("Черновик", default=True)
    review_status = models.CharField(
        "Статус рассмотрения", max_length=150)
    is_paid = models.BooleanField("Оплачено", default=True)
    experience_confirmation_scan_url = models.URLField(
        "URL подтверждения стажа")
    employee_сharacteristics_scan_url = models.URLField(
        "URL характеристики на работника")

    def __str__(self):
        return self.application_id

    class Meta:
        managed = True
        verbose_name = 'Заявление на аттестацию'
        verbose_name_plural = 'Заявления на аттестацию'


class ApplicationAccountNumber(models.Model):
    """Учётный номер заявления"""
    applocation_number_id = models.AutoField(primary_key=True)
    # application_id = models.ForeignKey()

    def __str__(self):
        pass

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'ModelName'
        verbose_name_plural = 'ModelNames'
