Feature: Đăng nhập bằng email hoặc điện thoại

    Background: Hệ thống đã có những người dùng sau:
        Given Ông Trung là chủ sân, đã tạo 2 sân
          And Ông Tú là chủ sân, chưa tạo sân nào
          And Bà Ánh là người đặt đã cập nhật điện thoại
          And Ông Đạt là người đặt chưa cập nhật điện thoại

    Scenario: Chủ sân đăng nhập bằng email khi đã tạo sân
        Given Ông Trung đang mở màn hình đăng nhập
        When Ông Trung nhập form hợp lệ để đăng nhập bằng email
         And Bấm đăng nhập
        Then Ông Trung nhìn thấy trang "Trạng thái đặt sân" của sân đầu tiên

    Scenario: Chủ sân đăng nhập bằng điện thoại khi chưa tạo sân
        Given Ông Tú đang mở màn hình đăng nhập
        When Ông Tú nhập form hợp lệ để đăng nhập bằng điện thoại
         And Bấm đăng nhập
        Then Được chuyển đến trang tạo sân
         And Nhìn thấy thông báo "Hãy nhập thông tin sân của bạn"

    Scenario: Người đặt đăng nhập bằng điện thoại
        Given Bà Ánh đang mở màn hình đăng nhập
        When Bà Ánh nhập form hợp lệ để đăng nhập bằng điện thoại
         And Bấm đăng nhập
        Then Được chuyển đến trang đặt sân


    Scenario: Người đặt đăng nhập bằng email
        Given Ông Đạt đang mở màn hình đăng nhập
        When Ông Đạt nhập form hợp lệ để đăng nhập bằng email
         And Bấm đăng nhập
        Then Được chuyển đến trang thông tin tài khoản "Đạt"
         And Nhìn thấy thông báo "Hãy nhập số điện thoại và tên của bạn để đặt sân được tiện lợi hơn"
