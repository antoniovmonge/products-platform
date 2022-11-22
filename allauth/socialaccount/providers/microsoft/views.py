import json

import requests

from allauth.socialaccount import app_settings
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

from .provider import MicrosoftGraphProvider


def _check_errors(response):
    try:
        data = response.json()
    except json.decoder.JSONDecodeError:
        raise OAuth2Error(f"Invalid JSON from Microsoft Graph API: {response.text}")

    if "id" not in data:
        error_message = "Error retrieving Microsoft profile"
        microsoft_error_message = data.get("error", {}).get("message")
        if microsoft_error_message:
            error_message = ": ".join((error_message, microsoft_error_message))
        raise OAuth2Error(error_message)

    return data


class MicrosoftGraphOAuth2Adapter(OAuth2Adapter):
    provider_id = MicrosoftGraphProvider.id

    settings = app_settings.PROVIDERS.get(provider_id, {})
    # Lower case "tenant" for backwards compatibility
    tenant = settings.get("TENANT", settings.get("tenant", "common"))

    provider_base_url = f"https://login.microsoftonline.com/{tenant}"
    access_token_url = f"{provider_base_url}/oauth2/v2.0/token"
    authorize_url = f"{provider_base_url}/oauth2/v2.0/authorize"
    profile_url = "https://graph.microsoft.com/v1.0/me"

    user_properties = (
        "businessPhones",
        "displayName",
        "givenName",
        "id",
        "jobTitle",
        "mail",
        "mobilePhone",
        "officeLocation",
        "preferredLanguage",
        "surname",
        "userPrincipalName",
        "mailNickname",
        "companyName",
    )
    profile_url_params = {"$select": ",".join(user_properties)}

    def complete_login(self, request, app, token, **kwargs):
        headers = {"Authorization": f"Bearer {token.token}"}
        response = requests.get(
            self.profile_url,
            params=self.profile_url_params,
            headers=headers,
        )
        extra_data = _check_errors(response)
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(MicrosoftGraphOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(MicrosoftGraphOAuth2Adapter)