import requests

from allauth.socialaccount import app_settings
from allauth.socialaccount.providers.keycloak.provider import KeycloakProvider
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)


class KeycloakOAuth2Adapter(OAuth2Adapter):
    provider_id = KeycloakProvider.id
    supports_state = True

    settings = app_settings.PROVIDERS.get(provider_id, {})
    provider_base_url = "{}/realms/{}".format(
        settings.get("KEYCLOAK_URL"), settings.get("KEYCLOAK_REALM")
    )

    authorize_url = f"{provider_base_url}/protocol/openid-connect/auth"

    other_url = settings.get("KEYCLOAK_URL_ALT")
    if other_url is None:
        other_url = settings.get("KEYCLOAK_URL")

    server_base_url = "{}/realms/{}".format(other_url, settings.get("KEYCLOAK_REALM"))
    access_token_url = f"{server_base_url}/protocol/openid-connect/token"
    profile_url = f"{server_base_url}/protocol/openid-connect/userinfo"

    def complete_login(self, request, app, token, response):
        response = requests.get(
            self.profile_url, headers={"Authorization": "Bearer " + str(token)}
        )
        response.raise_for_status()
        extra_data = response.json()
        extra_data["id"] = extra_data["sub"]
        del extra_data["sub"]

        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(KeycloakOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(KeycloakOAuth2Adapter)
