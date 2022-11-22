import requests

from allauth.socialaccount import app_settings
from allauth.socialaccount.providers.lemonldap.provider import LemonLDAPProvider
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)


class LemonLDAPOAuth2Adapter(OAuth2Adapter):
    provider_id = LemonLDAPProvider.id
    supports_state = True

    settings = app_settings.PROVIDERS.get(provider_id, {})
    provider_base_url = settings.get("LEMONLDAP_URL")

    access_token_url = f"{provider_base_url}/oauth2/token"
    authorize_url = f"{provider_base_url}/oauth2/authorize"
    profile_url = f"{provider_base_url}/oauth2/userinfo"

    def complete_login(self, request, app, token, response):
        response = requests.post(
            self.profile_url, headers={"Authorization": "Bearer " + str(token)}
        )
        response.raise_for_status()
        extra_data = response.json()
        extra_data["id"] = extra_data["sub"]
        del extra_data["sub"]

        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(LemonLDAPOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(LemonLDAPOAuth2Adapter)
