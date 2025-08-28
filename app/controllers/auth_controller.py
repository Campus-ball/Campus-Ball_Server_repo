from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.dto.auth.request.loginRequest import LoginRequest
from app.dto.auth.response.loginResponse import LoginResponse
from app.dto.auth.request.refreshTokenRequest import RefreshTokenRequest
from app.dto.auth.response.refreshTokenResponse import RefreshTokenResponse
from app.dto.auth.response.logoutResponse import LogoutResponse
from app.dto.auth.request.signupClubLeaderRequest import SignUpClubLeaderRequest
from app.dto.auth.response.signupClubLeaderResponse import SignUpClubLeaderResponse
from app.repositories.auth_repository import AuthRepository
from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["auth"])
auth_service = AuthService(AuthRepository())
security = HTTPBearer(auto_error=True)


@router.post("/signup/club-leader", response_model=SignUpClubLeaderResponse)
def signup_club_leader(
    req: SignUpClubLeaderRequest, db: Session = Depends(get_db)
) -> SignUpClubLeaderResponse:
    return auth_service.signup_club_leader(db, req)


@router.post("/login", response_model=LoginResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)) -> LoginResponse:
    return auth_service.login(db, req)


@router.post("/token/refresh", response_model=RefreshTokenResponse)
def refresh_token(
    req: RefreshTokenRequest, db: Session = Depends(get_db)
) -> RefreshTokenResponse:
    return auth_service.refresh_access_token(db, req)


@router.post("/logout", response_model=LogoutResponse)
def logout(
    cred: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> LogoutResponse:
    auth_service.logout(db, cred.credentials)
    return LogoutResponse(status=200, message="성공", data=None)
