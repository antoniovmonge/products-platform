from django.contrib.auth import get_user_model
from django.urls import reverse

# from appo_app.users.models import CustomUser


User = get_user_model()


class TestUserAdmin:
    def test_changelist(self, admin_client):
        url = reverse("admin:users_customuser_changelist")
        response = admin_client.get(url)
        assert response.status_code == 200

    def test_search(self, admin_client):
        url = reverse("admin:users_customuser_changelist")
        response = admin_client.get(url, data={"q": "test"})
        assert response.status_code == 200

    def test_add(self, admin_client):
        url = reverse("admin:users_customuser_add")
        response = admin_client.get(url)
        assert response.status_code == 200

        response = admin_client.post(
            url,
            data={
                "email": "mrtest@email.com",
                "password": "My_R@ndom-P@ssw0rd",
                "password2": "My_R@ndom-P@ssw0rd",
            },
        )
        assert response.status_code == 200
        # assert User.objects.filter(email="mrtest@email.com").exists()

    def test_view_user(self, admin_client):
        user, _ = User.objects.get_or_create(email="mrtest@email.com")
        url = reverse("admin:users_customuser_change", kwargs={"object_id": user.pk})
        response = admin_client.get(url)
        assert response.status_code == 200
