import time

from behave import given, then, when
from django.contrib.auth.models import User
from seleniumlogin import force_login

from bdd.models import Item


@given(u'the following items')
def set_up_items(context):
    Item.objects.bulk_create([
        Item(pk=row['pk'], sort_order=i)
        for i, row
        in enumerate(context.table)
    ])


@given(u'we are on the item list page')
def go_to_admin_page(context):
    user = User.objects.create_superuser(
        email='user@example.com',
        password='password',
        username='myuser',
    )
    force_login(user, context.browser.driver, context.test.live_server_url)
    context.item_list_page.open(context)


@when(u'item {initial_position:d} is moved to position {new_position:d}')
def move_items(context, initial_position, new_position):
    context.item_list_page.move_item(initial_position, new_position)
    time.sleep(.1)


@then(u'the items should be ordered thus')
def check_item_order(context):
    items = list(Item.objects.values_list('pk', flat=True))
    expected = []
    for row in context.table:
        expected.append(int(row['pk']))

    assert items == expected, (items, expected)
