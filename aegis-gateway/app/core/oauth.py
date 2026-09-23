import httpx

from app.core.config import settings
from app.core.exceptions import InvalidCredentialsError
from app.modules.auth.schemas import OauthProfile,OAuthProvider

async def fetch_google_user(code:str)->OauthProfile:
  """exchange code for google user details."""
  data={
    "code":code,
    "client_id":settings.GOOGLE_CLIENT_ID,
    "client_secret":settings.GOOGLE_CLIENT_SECRET,
    "redirect_uri":settings.GOOGLE_REDIRECT_URI,
    "grant_type":"authorization_code"
  }
  async with httpx.AsyncClient(timeout=10.0) as client:
    token_resp=await client.post(settings.GOOGLE_TOKEN_URL,data=data)
    if token_resp.is_error:
      raise InvalidCredentialsError()
    token_data=token_resp.json()
    access_token=token_data.get("access_token")
    user_resp=await client.get(
      settings.GOOGLE_USERINFO_URL,
      headers={"Authorization":f"Bearer {access_token}"}
      )
    if user_resp.is_error:
      raise InvalidCredentialsError()
    info=user_resp.json()
    if not info.get("email_verified"):
      raise InvalidCredentialsError()
    return OauthProfile(
      oauth_id=str(info["sub"]),
      oauth_provider=OAuthProvider.GOOGLE,
      email=info["email"],
      name=info["name"]
    )

async def fetch_github_user(code:str)->OauthProfile:
  """exchange code for github user details."""
  data={
    "code":code,
    "client_id":settings.GITHUB_CLIENT_ID,
    "client_secret":settings.GITHUB_CLIENT_SECRET,
    "redirect_uri":settings.GITHUB_REDIRECT_URI
  }
  headers={"Accept":"application/json"}
  async with httpx.AsyncClient() as client:
    token_resp=await client.post(settings.GITHUB_TOKEN_URL,data=data,headers=headers)
    if token_resp.is_error:
      raise InvalidCredentialsError()
    token_data=token_resp.json()
    access_token=token_data.get("access_token")
    if not access_token:
      raise InvalidCredentialsError()
    auth_headers = {
      "Authorization": f"Bearer {access_token}",
      "Accept": "application/vnd.github+json",
    }
    user_resp=await client.get(settings.GITHUB_USER_URL,headers=auth_headers)
    if user_resp.is_error:
      raise InvalidCredentialsError()
    user_info=user_resp.json()
    email_resp=await client.get(settings.GITHUB_EMAILS_URL,headers=auth_headers)
    if email_resp.is_error:
      raise InvalidCredentialsError()
    emails=email_resp.json()
    verified_primary = next(
      (e["email"] for e in emails if e.get("primary") and e.get("verified")), 
      None
    )
    if not verified_primary:
        raise InvalidCredentialsError()

    return OauthProfile(
        oauth_provider=OAuthProvider.GITHUB,
        oauth_id=str(user_info["id"]),
        email=verified_primary,
        name=user_info.get("name"),
    )


async def get_oauth_user(provider: OAuthProvider, code: str) -> OauthProfile:
    """Dispatches to the correct OAuth handler."""
    if provider == OAuthProvider.GOOGLE:
        return await fetch_google_user(code)
    elif provider == OAuthProvider.GITHUB:
        return await fetch_github_user(code)
    raise InvalidCredentialsError("Unsupported OAuth provider.")