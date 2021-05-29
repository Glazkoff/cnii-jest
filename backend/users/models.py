from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    """Пользователь"""
    SEX_CHOICES = (("M", "Мужской"), ("F", "Женский"))
    surname = models.CharField("Фамилия", max_length=150, blank=True)
    name = models.CharField("Имя", max_length=150, blank=True)
    patricity = models.CharField("Отчество", max_length=150, blank=True)
    birthday = models.DateField("Дата рождения", blank=True, null=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True)
    native_language = models.CharField(
        "Родной язык", max_length=150, blank=True)
    citizenship = models.CharField("Гражданство", max_length=150, blank=True)
    martial_status = models.CharField(
        "Семейное положение", max_length=150, blank=True)
    organization = models.CharField("Организация", max_length=150, blank=True)
    job_position = models.CharField(
        "Занимаемая должность", max_length=150, blank=True)
    education = models.CharField("Образование", max_length=150, blank=True)
    home_address = models.CharField(
        "Домашний адрес", max_length=150, blank=True)
    passport = models.CharField("Данные паспорта", max_length=150, blank=True)
    passport_part1_scan_url = models.URLField(
        "URLСканаПаспортаРазворот1", blank=True)
    passport_part2_scan_url = models.URLField(
        "URLСканаПаспортаРазворот2", blank=True)
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

    def __str__(self):
        return str(self.name + " " + self.surname)
