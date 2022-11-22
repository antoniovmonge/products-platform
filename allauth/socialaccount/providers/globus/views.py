import requests

from allauth.socialaccount.providers.globus.provider import GlobusProvider
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)


class GlobusAdapter(OAuth2Adapter):
    provider_id = GlobusProvider.id
    provider_default_url = "https://auth.globus.org/v2/oauth2"

    provider_base_url = "https://auth.globus.org/v2/oauth2"

    access_token_url = f"{provider_base_url}/token"
    authorize_url = f"{provider_base_url}/authorize"
    profile_url = f"{provider_base_url}/userinfo"

    def complete_login(self, request, app, token, response):
        extra_data = requests.get(
            self.profile_url,
            params={"access_token": token.token},
            headers={
                "Authorization": "Bearer " + token.token,
            },
        )

        return self.get_provider().sociallogin_from_response(request, extra_data.json())


oauth2_login = OAuth2LoginView.adapter_view(GlobusAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(GlobusAdapter)
