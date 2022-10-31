from django.urls import reverse

from pplatform.users.models import User


class TestUserAdmin:
    def test_changelist(self, admin_client):
        url = reverse("admin:users_user_changelist")
        response = admin_client.get(url)
        assert response.status_code == 200

    def test_search(self, admin_client):
        url = reverse("admin:users_user_changelist")
        response = admin_client.get(url, data={"q": "test"})
        assert response.status_code == 200

    def test_add(self, admin_client):
        url = reverse("admin:users_user_add")
        response = admin_client.get(url)
        assert response.status_code == 200

        response = admin_client.post(
            url,
            data={
                "email": "test@email.com",
                "password1": "My_R@ndom-P@ssw0rd",
                "password2": "My_R@ndom-P@ssw0rd",
            },
        )
        assert response.status_code == 302
        assert User.objects.filter(email="test@email.com").exists()

    # def test_view_user(self, admin_client):
    #     user = User.objects.get(email="admin@email.com")
    #     url = reverse("admin:users_user_change", kwargs={"object_id": user.pk})
    #     response = admin_client.get(url)
    #     assert response.status_code == 200
