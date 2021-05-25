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

        # REVIEW:
        #   1. Đoạn này có phải là tự động chuyển trạng thái thành "đã đọc" khi người dùng vào trang danh sách noti không?
        #       Anh nghĩ chỉ nên chuyển trạng thái khi người dùng vào xem chi tiết noti thôi
        #   2. Trường hợp cần update thuộc tính của nhiều objects cùng một lúc, sử dụng hàm .update() sẽ hiệu quả hơn:
        #       `user.notifications.all().update(unread=False)`
        #       Câu hỏi 1: Tại sao như thế hiệu quả hơn?
        #       Câu hỏi 2: Hàm .update() có nhược điểm gì so với hàm .save()?
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
        # REVIEW: chú ý thống nhất cách đặt tên, bên trên là "notification", ở đây lại là "notify"
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
