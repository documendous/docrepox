from django.contrib.auth import get_user_model


User = get_user_model()


def create_testusers(apps, schema):
    for i in range(10):
        test_user = User.objects.create(
            username=f"testuser{i}",
            email=f"testuser{i}@localhost",
        )
        test_user.set_password("testpass")
        test_user.save()
