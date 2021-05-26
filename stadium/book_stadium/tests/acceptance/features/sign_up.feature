Feature: Đăng ký người dùng bằng email hoặc điện thoại

    Scenario: Chủ sân đăng ký bằng email
        Given Ông Niko Bellic đang mở màn hình tạo tài khoản mới
        When Nhập form hợp lệ để đăng ký chủ sân
         And Với input "Email hoặc số điện thoại", nhập "niko.bellic@eyefind.mail"
         And Bấm đăng ký
        Then Tài khoản "niko.bellic@eyefind.mail" đã được tạo
         And Được chuyển đến trang tạo sân
         And Nhìn thấy thông báo "Hãy nhập thông tin sân của bạn"

    Scenario: Chủ sân đăng ký bằng điện thoại
        Given Ông Carl Johnson đang mở màn hình tạo tài khoản mới
        When Nhập form hợp lệ để đăng ký chủ sân
         And Với input "Email hoặc số điện thoại", nhập "0324512451"
         And Bấm đăng ký
        Then Tài khoản "0324512451" đã được tạo
         And Được chuyển đến trang tạo sân
         And Nhìn thấy thông báo "Hãy nhập thông tin sân của bạn"

    Scenario: Người đặt đăng ký bằng email
        Given Ông Trung đang mở màn hình tạo tài khoản mới
        When Nhập form hợp lệ để đăng ký người đặt
         And Với input "Email hoặc số điện thoại", nhập "trungtran@gmail.com"
         And Bấm đăng ký
        Then Tài khoản "trungtran@gmail.com" đã được tạo
         And Được chuyển đến trang thông tin tài khoản "trungtran@gmail.com"
         And Nhìn thấy thông báo "Hãy nhập số điện thoại và tên của bạn để đặt sân được tiện lợi hơn"

    Scenario: Người đặt đăng ký bằng điện thoại
        Given Ông Trung đang mở màn hình tạo tài khoản mới
        When Nhập form hợp lệ để đăng ký người đặt
         And Với input "Email hoặc số điện thoại", nhập "0325685412"
         And Bấm đăng ký
        Then Tài khoản "0325685412" đã được tạo
         And Được chuyển đến trang đặt sân
