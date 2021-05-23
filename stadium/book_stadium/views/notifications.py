from notifications.signals import notify
from swapper import load_model

from django.shortcuts import render, get_object_or_404
from django.views import View

from book_stadium.models import Stadium


Notification = load_model('notifications', 'Notification')


class Notifications(View):
    def get(self, request):
        user = request.user
        notifications = user.notifications.all()
        stadiums_by_owner = Stadium.objects.filter(owner=request.user)

        for notification in notifications:
            if notification.unread:
                notification.unread = False
                notification.save()

        context = {
            'fields': stadiums_by_owner,
            'notifications': notifications
        }
        return render(request, 'book_stadium/notifications.html', context)


class NotificationDetail(View):
    def get(self, request, pk):
        notify = Notification.objects.get(pk=pk)
        stadiums_by_owner = Stadium.objects.filter(owner=request.user)

        if notify.unread:
            notify.unread = False
            notify.save()

        context = {
            'fields': stadiums_by_owner,
            'notify': notify
        }
        return render(request, 'book_stadium/notification_detail.html', context)
