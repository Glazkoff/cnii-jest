from users.models import CustomUser
from .logic import ReportGenerator


def generate_document(request):
    # Model data
    people = CustomUser.objects.all()
    # print('PEOPLE: ' + people.__str__)
    return ReportGenerator().create_report(people)
