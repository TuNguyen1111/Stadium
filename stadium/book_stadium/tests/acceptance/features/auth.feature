Feature: Đăng ký người dùng bằng email hoặc điện thoại

    Scenario: Chủ sân đăng ký bằng email
        Given Ông Trung đang mở màn hình tạo tài khoản mới
        # When Với input "Bạn là", chọn "Chủ sân"
            # And Với input "Email hoặc số điện thoại", nhập email "rockstarr@eyefind.mail"
            # And Với input "Mật khẩu", nhập mật khẩu hợp lệ
            # And Với input "Nhập lại mật khẩu", nhập mật khẩu hợp lệ
        When Nhập form hợp lệ
        Then Ông Trung được tạo tài khoản
            # And Được chuyển đến trang tạo sân
            # And Nhìn thấy thông báo "Hãy nhập thông tin sân của bạn"
