from django.core.management import BaseCommand
from patient_info.models import Patient
from faker import Faker
from random import randint

class Command(BaseCommand):

    help = u"Uploads a fake patients"

    def add_arguments(self, parser):
        parser.add_argument('--patients_amount', dest="patients_amount", type=int, default=10)
    
    def handle(self, *args, **options):
        for _ in range(options['patients_amount']):

            fake = Faker("ru_RU")
            fake_profile = fake.simple_profile()
            f_fullname = fake_profile["name"]
            f_birthdate = fake_profile["birthdate"]
            f_room = randint(20, 28)

            patient, _ = Patient.objects.get_or_create(
                fullname = f_fullname,
                dob = f_birthdate,
                room = f_room
            )

            print("Пациент %s добавлен в базу"%(patient.fullname))