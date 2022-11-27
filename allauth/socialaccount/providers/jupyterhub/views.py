import requests

from allauth.socialaccount import app_settings
from allauth.socialaccount.providers.jupyterhub.provider import JupyterHubProvider
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)


class JupyterHubAdapter(OAuth2Adapter):
    provider_id = JupyterHubProvider.id

    settings = app_settings.PROVIDERS.get(provider_id, {})
    provider_base_url = settings.get("API_URL", "")

    access_token_url = f"{provider_base_url}/hub/api/oauth2/token"
    authorize_url = f"{provider_base_url}/hub/api/oauth2/authorize"
    profile_url = f"{provider_base_url}/hub/api/user"

    def complete_login(self, request, app, access_token, **kwargs):
        headers = {"Authorization": f"Bearer {access_token}"}

        extra_data = requests.get(self.profile_url, headers=headers)

        user_profile = extra_data.json()

        return self.get_provider().sociallogin_from_response(request, user_profile)


oauth2_login = OAuth2LoginView.adapter_view(JupyterHubAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(JupyterHubAdapter)