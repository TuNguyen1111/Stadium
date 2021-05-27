from django.apps import AppConfig


class BookStadiumConfig(AppConfig):
    name = 'book_stadium'

    def ready(self):
        import book_stadium.signals
