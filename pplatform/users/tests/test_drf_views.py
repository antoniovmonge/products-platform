from django.test import RequestFactory

from pplatform.users.api.views import UserViewSet
from pplatform.users.models import CustomUser


class TestUserViewSet:
    def test_get_queryset(self, user: CustomUser, rf: RequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert user in view.get_queryset()

    def test_me(self, user: CustomUser, rf: RequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        response = view.me(request)

        assert response.data == {
            "email": user.email,
            "name": user.name,
            "url": f"http://testserver/api/users/{user.email}/",
        }
