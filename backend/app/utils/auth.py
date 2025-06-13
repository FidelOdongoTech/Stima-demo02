"""
Authentication utilities and dependencies.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any

# Security scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    Get current authenticated user.
    
    In a production system, this would validate JWT tokens and return user info.
    For demo purposes, we return a mock user.
    """
    # In a real system, you would:
    # 1. Decode and validate the JWT token
    # 2. Check token expiration
    # 3. Retrieve user information from database
    # 4. Handle token refresh if needed
    
    if not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Mock user for demo purposes
    return {
        "user_id": "demo_user",
        "name": "Demo Agent",
        "role": "agent",
        "branch_code": "001"
    }


async def get_current_active_user(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get current active user (additional validation can be added here)."""
    # Add any additional user validation logic here
    return current_user


def require_role(required_role: str):
    """
    Dependency factory to require specific user roles.
    
    Args:
        required_role: The role required to access the endpoint
        
    Returns:
        Dependency function that validates user role
    """
    async def role_checker(
        current_user: Dict[str, Any] = Depends(get_current_active_user)
    ) -> Dict[str, Any]:
        user_role = current_user.get("role")
        
        if user_role != required_role and user_role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role: {required_role}"
            )
        
        return current_user
    
    return role_checker

