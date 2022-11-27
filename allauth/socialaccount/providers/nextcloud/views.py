import xml.etree.ElementTree as ET

import requests

from allauth.socialaccount import app_settings
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

from .provider import NextCloudProvider


class NextCloudAdapter(OAuth2Adapter):
    provider_id = NextCloudProvider.id
    settings = app_settings.PROVIDERS.get(provider_id, {})
    server = settings.get("SERVER", "https://nextcloud.example.org")
    access_token_url = f"{server}/apps/oauth2/api/v1/token"
    authorize_url = f"{server}/apps/oauth2/authorize"
    profile_url = f"{server}/ocs/v1.php/cloud/users/"

    def complete_login(self, request, app, token, **kwargs):
        extra_data = self.get_user_info(token, kwargs["response"]["user_id"])
        return self.get_provider().sociallogin_from_response(request, extra_data)

    def get_user_info(self, token, user_id):
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(self.profile_url + user_id, headers=headers)
        resp.raise_for_status()
        data = ET.fromstring(resp.content.decode())[1]
        return {d.tag: d.text.strip() for d in data if d.text is not None}


oauth2_login = OAuth2LoginView.adapter_view(NextCloudAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(NextCloudAdapter)