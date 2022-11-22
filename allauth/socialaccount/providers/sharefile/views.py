import requests

from allauth.socialaccount import app_settings
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

from .provider import ShareFileProvider


class ShareFileOAuth2Adapter(OAuth2Adapter):
    provider_id = ShareFileProvider.id
    settings = app_settings.PROVIDERS.get(provider_id, {})
    subdomain = settings.get("SUBDOMAIN", "secure")
    apicp = settings.get("APICP", "sharefile.com")

    provider_default_url = settings.get("DEFAULT_URL", "https://secure.sharefile.com")
    provider_default_api_url = f"https://{subdomain}.sf-api.com"
    provider_api_version = "v3"

    access_token_url = f"https://{subdomain}.{apicp}/oauth/token"
    refresh_token_url = f"https://{subdomain}.{apicp}/oauth/token"
    authorize_url = f"{provider_default_url}/oauth/authorize"
    profile_url = "{}/sf/{}/Users".format(
        provider_default_api_url, provider_api_version
    )

    def complete_login(self, request, app, token, response):
        headers = {"Authorization": f"Bearer {token.token}"}
        extra_data = requests.get(self.profile_url, headers=headers).json()
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(ShareFileOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(ShareFileOAuth2Adapter)
