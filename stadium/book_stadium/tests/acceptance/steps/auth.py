from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from faker import Faker
from model_bakery import baker

from django.contrib.auth import get_user_model
from django.db.models import Q

from book_stadium.models import Roles, User, Stadium

User = get_user_model()
fake = Faker()


def get_person_name(person):
    person_name = person.replace('Ông', '').replace('Bà', '').strip()
    return person_name


@given('Ông {name} đang mở màn hình tạo tài khoản mới')
def step_impl(context, name):
    context.browser.get(context.url)

    button = context.browser.find_element(By.XPATH, '//button[contains(text(), "Đăng nhập")]')
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
    if not input.is_displayed():
        input = context.browser.find_element(By.XPATH, '//label[contains(text(), "Email hoặc số điện thoại")]/following-sibling::input')

    input.clear()
    input.send_keys(text)


@when('Với input "Mật khẩu", nhập "{text}"')
def step_impl(context, text):
    input = context.browser.find_element(By.ID, 'id_password1')
    if not input.is_displayed():
        input = context.browser.find_element(By.XPATH, '//label[contains(text(), "Mật khẩu")]/following-sibling::input')

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
    button = context.browser.find_element(By.XPATH, '//button[contains(text(), "Đăng ký")]')
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


@then('Được chuyển đến trang thông tin tài khoản "{email_or_phone_or_name}"')
def step_impl(context, email_or_phone_or_name):
    condition = (
        Q(email=email_or_phone_or_name) |
        Q(phone_number=email_or_phone_or_name) |
        Q(name=email_or_phone_or_name)
    )
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


@given('Ông Trung là chủ sân, đã tạo 2 sân')
def step_impl(context):
    user = baker.make(
        User,
        name='Trung',
        role=Roles.OWNER,
        email=fake.email(),
        phone_number=fake.phone_number()[:12],  # phone_number max_length is 12
    )
    password = fake.password()
    user.set_password(password)
    user.save()
    context.password_of_Trung = password
    context.email_of_Trung = user.email
    context.phone_number_of_Trung = user.phone_number

    context.stadium_of_Trung_1 = baker.make(Stadium, owner=user)
    context.stadium_of_Trung_2 = baker.make(Stadium, owner=user)


@given('Ông Tú là chủ sân, chưa tạo sân nào')
def step_impl(context):
    user = baker.make(
        User,
        name='Tú',
        role=Roles.OWNER,
        email=fake.email(),
        phone_number=fake.phone_number()[:12],  # phone_number max_length is 12
    )
    password = fake.password()
    user.set_password(password)
    user.save()
    context.password_of_Tú = password
    context.email_of_Tú = user.email
    context.phone_number_of_Tú = user.phone_number


@given('Bà Ánh là người đặt đã cập nhật điện thoại')
def step_impl(context):
    user = baker.make(
        User,
        name='Ánh',
        role=Roles.PLAYER,
        email=fake.email(),
        phone_number=fake.phone_number()[:12],  # phone_number max_length is 12
    )
    password = fake.password()
    user.set_password(password)
    user.save()
    context.password_of_Ánh = password
    context.email_of_Ánh = user.email
    context.phone_number_of_Ánh = user.phone_number


@given('Ông Đạt là người đặt chưa cập nhật điện thoại')
def step_impl(context):
    user = baker.make(
        User,
        name='Đạt',
        role=Roles.PLAYER,
        email=fake.email(),
        phone_number='',
    )
    password = fake.password()
    user.set_password(password)
    user.save()
    context.password_of_Đạt = password
    context.email_of_Đạt = user.email


@given('{person} đang mở màn hình đăng nhập')
def step_impl(context, person):
    context.browser.get(context.url)
    button = context.browser.find_element(By.XPATH, '//button[contains(text(), "Đăng nhập")]')
    button.click()


@when('{person} nhập form hợp lệ để đăng nhập bằng {method}')
def step_impl(context, person, method):
    person_name = get_person_name(person)
    if method == 'email':
        email_or_phone = getattr(context, f'email_of_{person_name}')
    else:
        email_or_phone = getattr(context, f'phone_number_of_{person_name}')
    password = getattr(context, f'password_of_{person_name}')

    steps = '''
        When Với input "Email hoặc số điện thoại", nhập "{email_or_phone}"
         And Với input "Mật khẩu", nhập "{password}"
    '''
    steps = steps.format(email_or_phone=email_or_phone, password=password)
    context.execute_steps(steps)


@when('Bấm đăng nhập')
def step_impl(context):
    button = context.browser.find_element(By.XPATH, '//div[@id="login-modal"]//button[contains(text(), "Đăng nhập")]')
    button.click()


@then('{person} nhìn thấy trang "Trạng thái đặt sân" của sân đầu tiên')
def step_impl(context, person):
    person_name = get_person_name(person)
    stadium_pk = getattr(context, f'stadium_of_{person_name}_1').pk
    context.test.assertEqual(
        context.browser.current_url,
        f'{context.url}/owner/{stadium_pk}'
    )
