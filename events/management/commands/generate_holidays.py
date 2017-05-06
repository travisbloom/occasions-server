from django.core.management.base import BaseCommand
from workalendar.core import ChristianMixin
from workalendar.usa import UnitedStates


class HolidaysToGenerate(UnitedStates, ChristianMixin):
    include_ash_wednesday = True
    include_palm_sunday = True
    include_good_friday = True
    include_easter_sunday = True
    include_christmas = True


class Command(BaseCommand):
    help = 'Generate holidays'

    def handle(self, *args, **options):
        holidays = HolidaysToGenerate()
        import pdb
        pdb.set_trace()
