from django.core.management.base import BaseCommand
from book_stadium.models import TimeFrame


class Command(BaseCommand):
    def handle(self, *args, **options):
        timeframes = TimeFrame.objects.all()
        if not timeframes:
            TimeFrame.objects.bulk_create([
                TimeFrame(start_time='7:00:00', end_time='8:30:00'),
                TimeFrame(start_time='8:30:00', end_time='10:00:00'),
                TimeFrame(start_time='10:00:00', end_time='11:30:00'),
                TimeFrame(start_time='11:30:00', end_time='13:00:00'),
                TimeFrame(start_time='13:00:00', end_time='14:30:00'),
                TimeFrame(start_time='14:30:00', end_time='16:00:00'),
                TimeFrame(start_time='16:00:00', end_time='17:30:00'),
                TimeFrame(start_time='17:30:00', end_time='19:00:00'),
                TimeFrame(start_time='19:00:00', end_time='20:30:00'),
                TimeFrame(start_time='20:30:00', end_time='22:00:00'),
            ])
            self.stdout.write(self.style.SUCCESS('Tạo khung giờ thành công!'))
        else:
            self.stdout.write(self.style.WARNING(
                'Khung giờ đã có sẵn trong database!'))
