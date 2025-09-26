"""
Luna AI Authentication & Authorization Manager
Supabase Auth + JWT + API Key System
"""
import os
import jwt
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client
import logging
import hashlib
import secrets
from database.supabase_client import supabase_client
from database.upstash_client import upstash_client

security = HTTPBearer()


class LunaAuthManager:
    """Comprehensive authentication and authorization manager"""

    def __init__(self):
        self.supabase = supabase_client
        self.cache = upstash_client
        self.jwt_secret = os.getenv("JWT_SECRET_KEY", secrets.token_urlsafe(32))
        self.jwt_algorithm = "HS256"
        self.jwt_expiry_hours = 24

        # API key settings
        self.api_key_prefix = "luna_"

    def create_access_token(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create JWT access token for authenticated user"""
        try:
            # Token payload
            payload = {
                "user_id": user_data["id"],
                "email": user_data.get("email"),
                "exp": datetime.utcnow() + timedelta(hours=self.jwt_expiry_hours),
                "iat": datetime.utcnow(),
                "type": "access_token"
            }

            # Generate JWT
            access_token = jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)

            # Store token in Redis for quick validation
            self.cache.set_session(f"token:{user_data['id']}", {
                "access_token": access_token,
                "user_data": user_data,
                "created_at": datetime.utcnow().isoformat()
            }, ttl=self.jwt_expiry_hours * 3600)

            return {
                "access_token": access_token,
                "token_type": "Bearer",
                "expires_in": self.jwt_expiry_hours * 3600,
                "user_id": user_data["id"]
            }

        except Exception as e:
            logging.error(f"Error creating access token: {e}")
            raise HTTPException(status_code=500, detail="Token creation failed")

    def verify_access_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode JWT access token"""
        try:
            # Decode JWT
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])

            # Check token type
            if payload.get("type") != "access_token":
                raise HTTPException(status_code=401, detail="Invalid token type")

            # Check if token is cached (quick validation)
            cached_session = self.cache.get_session(f"token:{payload['user_id']}")
            if not cached_session or cached_session.get("access_token") != token:
                raise HTTPException(status_code=401, detail="Token not found in session")

            return payload

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
        except Exception as e:
            logging.error(f"Token verification error: {e}")
            raise HTTPException(status_code=401, detail="Token verification failed")

    def authenticate_user(self, email: str, password: str) -> Dict[str, Any]:
        """Authenticate user with Supabase Auth"""
        try:
            # Authenticate with Supabase
            auth_response = self.supabase.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            if not auth_response.user:
                raise HTTPException(status_code=401, detail="Invalid credentials")

            user_data = {
                "id": auth_response.user.id,
                "email": auth_response.user.email,
                "created_at": auth_response.user.created_at
            }

            # Get or create user profile
            profile = self.supabase.get_user_profile(user_data["id"])
            if not profile:
                profile = self.supabase.create_user_profile({
                    "id": user_data["id"],
                    "email": user_data["email"]
                })

            user_data.update(profile)
            return user_data

        except Exception as e:
            logging.error(f"Authentication error: {e}")
            raise HTTPException(status_code=401, detail="Authentication failed")

    def register_user(self, email: str, password: str, profile_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Register new user with Supabase Auth"""
        try:
            # Register with Supabase
            auth_response = self.supabase.client.auth.sign_up({
                "email": email,
                "password": password
            })

            if not auth_response.user:
                raise HTTPException(status_code=400, detail="Registration failed")

            user_data = {
                "id": auth_response.user.id,
                "email": auth_response.user.email,
                "created_at": auth_response.user.created_at
            }

            # Create user profile with additional data
            profile_data = profile_data or {}
            profile_data.update({
                "id": user_data["id"],
                "email": user_data["email"]
            })

            profile = self.supabase.create_user_profile(profile_data)
            user_data.update(profile)

            return user_data

        except Exception as e:
            logging.error(f"Registration error: {e}")
            raise HTTPException(status_code=400, detail="Registration failed")

    def generate_api_key(self, user_id: str, name: str = "Default API Key") -> Dict[str, Any]:
        """Generate API key for user"""
        try:
            # Generate secure API key
            raw_key = secrets.token_urlsafe(32)
            api_key = f"{self.api_key_prefix}{raw_key}"

            # Hash for storage
            key_hash = hashlib.sha256(api_key.encode()).hexdigest()

            # Store API key metadata
            key_data = {
                "user_id": user_id,
                "key_hash": key_hash,
                "name": name,
                "created_at": datetime.utcnow().isoformat(),
                "last_used": None,
                "is_active": True
            }

            # Store in Redis and Supabase
            self.cache.store_user_context(f"api_key:{key_hash}", key_data, ttl=86400 * 365)  # 1 year

            return {
                "api_key": api_key,
                "name": name,
                "created_at": key_data["created_at"]
            }

        except Exception as e:
            logging.error(f"API key generation error: {e}")
            raise HTTPException(status_code=500, detail="API key generation failed")

    def verify_api_key(self, api_key: str) -> Dict[str, Any]:
        """Verify API key and return user data"""
        try:
            if not api_key.startswith(self.api_key_prefix):
                raise HTTPException(status_code=401, detail="Invalid API key format")

            # Hash the provided key
            key_hash = hashlib.sha256(api_key.encode()).hexdigest()

            # Get key data from cache
            key_data = self.cache.get_user_context(f"api_key:{key_hash}")
            if not key_data or not key_data.get("is_active"):
                raise HTTPException(status_code=401, detail="Invalid or inactive API key")

            # Update last used timestamp
            key_data["last_used"] = datetime.utcnow().isoformat()
            self.cache.store_user_context(f"api_key:{key_hash}", key_data, ttl=86400 * 365)

            # Get user profile
            user_profile = self.supabase.get_user_profile(key_data["user_id"])
            if not user_profile:
                raise HTTPException(status_code=401, detail="User not found")

            return {
                "user_id": key_data["user_id"],
                "auth_method": "api_key",
                "user_data": user_profile
            }

        except Exception as e:
            logging.error(f"API key verification error: {e}")
            raise HTTPException(status_code=401, detail="API key verification failed")

    def logout_user(self, user_id: str) -> bool:
        """Logout user by invalidating tokens"""
        try:
            # Remove from Redis cache
            self.cache.delete_session(f"token:{user_id}")

            # Logout from Supabase
            self.supabase.client.auth.sign_out()

            return True

        except Exception as e:
            logging.error(f"Logout error: {e}")
            return False


# Global auth manager instance
auth_manager = LunaAuthManager()


# FastAPI Dependencies
async def get_current_user_jwt(credentials: HTTPAuthorizationCredentials = Security(security)) -> Dict[str, Any]:
    """FastAPI dependency to get current user from JWT token"""
    try:
        token = credentials.credentials
        payload = auth_manager.verify_access_token(token)

        # Get fresh user data
        user_profile = auth_manager.supabase.get_user_profile(payload["user_id"])
        if not user_profile:
            raise HTTPException(status_code=401, detail="User not found")

        return {
            "user_id": payload["user_id"],
            "email": payload["email"],
            "auth_method": "jwt",
            "user_data": user_profile
        }

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"JWT authentication error: {e}")
        raise HTTPException(status_code=401, detail="Authentication required")


async def get_current_user_api_key(api_key: str) -> Dict[str, Any]:
    """Authenticate user via API key"""
    return auth_manager.verify_api_key(api_key)


async def get_current_user(
    jwt_auth: Optional[Dict[str, Any]] = Depends(get_current_user_jwt),
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """Flexible authentication - JWT or API key"""
    if jwt_auth:
        return jwt_auth
    elif api_key:
        return await get_current_user_api_key(api_key)
    else:
        raise HTTPException(status_code=401, detail="Authentication required")
