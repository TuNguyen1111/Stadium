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
        user.notifications.all().update(unread=False)

        context = {
            'fields': stadiums_by_owner,
            'notifications': notifications
        }
        return render(request, 'book_stadium/notifications.html', context)


class NotificationDetail(View):
    def get(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk)
        stadiums_by_owner = Stadium.objects.filter(owner=request.user)

        Notification.objects.filter(pk=pk).update(unread=False)

        context = {
            'fields': stadiums_by_owner,
            'notification': notification
        }
        return render(request, 'book_stadium/notification_detail.html', context)
