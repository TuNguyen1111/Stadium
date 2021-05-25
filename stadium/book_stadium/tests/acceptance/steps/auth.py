from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from faker import Faker

from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()
fake = Faker()


@given('Ông {name} đang mở màn hình tạo tài khoản mới')
def step_impl(context, name):
    context.browser.get(context.url)

    button = context.browser.find_element(By.XPATH, '//button[text()="Đăng nhập"]')
    button.click()

    link = context.browser.find_element(By.LINK_TEXT, 'Tạo tài khoản mới')
    link.click()


@when('Với input "Bạn là", chọn "{text}"')
def step_impl(context, text):
    select = context.browser.find_element(By.ID, 'id_role')
    select.click()
    Select(select).select_by_visible_text(text)


@when('Với input "Email hoặc số điện thoại", nhập "{text}"')
def step_impl(context, text):
    input = context.browser.find_element(By.ID, 'id_email_or_phone')
    input.clear()
    input.send_keys(text)


@when('Với input "Mật khẩu", nhập "{text}"')
def step_impl(context, text):
    input = context.browser.find_element(By.ID, 'id_password1')
    input.clear()
    input.send_keys(text)


@when('Với input "Nhập lại mật khẩu", nhập "{text}"')
def step_impl(context, text):
    input = context.browser.find_element(By.ID, 'id_password2')
    input.clear()
    input.send_keys(text)


@when('Nhập form hợp lệ để đăng ký {role}')
def step_impl(context, role):
    role = role[0].upper() + role[1:]  # Uppercase first letter
    steps = '''
        When Với input "Bạn là", chọn "{role}"
         And Với input "Email hoặc số điện thoại", nhập "{email}"
         And Với input "Mật khẩu", nhập "{password}"
         And Với input "Nhập lại mật khẩu", nhập "{password}"
    '''
    steps = steps.format(role=role, email=fake.email(), password=fake.password())
    context.execute_steps(steps)


@when('Bấm đăng ký')
def step_impl(context):
    button = context.browser.find_element(By.XPATH, '//button[text()="Đăng ký"]')
    button.click()


@then('Tài khoản "{email_or_phone}" đã được tạo')
def step_impl(context, email_or_phone):
    condition = Q(email=email_or_phone) | Q(phone_number=email_or_phone)
    user_exists = User.objects.filter(condition).exists()
    context.test.assertTrue(user_exists)


@then('Được chuyển đến trang tạo sân')
def step_impl(context):
    context.test.assertEqual(
        context.browser.current_url,
        f'{context.url}/them-san/'
    )


@then('Nhìn thấy thông báo "{message}"')
def step_impl(context, message):
    element = context.browser.find_element(By.XPATH, f'//div[contains(text(), "{message}")]')
    context.test.assertTrue(element.is_displayed())


@then('Được chuyển đến trang thông tin tài khoản "{email_or_phone}"')
def step_impl(context, email_or_phone):
    condition = Q(email=email_or_phone) | Q(phone_number=email_or_phone)
    user = User.objects.filter(condition).first()
    context.test.assertIsNotNone(user)
    context.test.assertEqual(
        context.browser.current_url,
        f'{context.url}/trang-ca-nhan/{user.pk}'
    )


@then('Được chuyển đến trang đặt sân')
def step_impl(context):
    context.test.assertEqual(
        context.browser.current_url,
        f'{context.url}'
    )
