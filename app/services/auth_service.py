from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.dto.auth.request.signupClubLeaderRequest import SignUpClubLeaderRequest
from app.dto.auth.response.signupClubLeaderResponse import SignUpClubLeaderResponse
from app.dto.auth.request.loginRequest import LoginRequest
from app.dto.auth.response.loginResponse import LoginResponse, TokenPair
from app.dto.auth.request.refreshTokenRequest import RefreshTokenRequest
from app.dto.auth.response.refreshTokenResponse import (
    RefreshTokenResponse,
    AccessTokenData,
)
from app.core.security import (
    verify_password,
    create_token_pair,
    decode_token,
    create_access_token,
)
from app.repositories.token_repository import TokenRepository
from app.repositories.auth_repository import AuthRepository


class AuthService:
    def __init__(
        self,
        repository: AuthRepository,
        token_repository: TokenRepository | None = None,
    ):
        self.repository = repository
        self.token_repository = token_repository or TokenRepository()

    def signup_club_leader(
        self, db: Session, req: SignUpClubLeaderRequest
    ) -> SignUpClubLeaderResponse:
        password_hash = hash_password(req.password)

        self.repository.create_user_and_club(
            db,
            user_id=req.userId,
            password_hash=password_hash,
            name=req.name,
            nickname=req.nickname,
            phone_number=req.phoneNumber,
            gender=req.gender,
            college_id=req.collegeId,
            department_id=req.departmentId,
            club_name=req.clubName,
            club_description=req.clubDescription,
            club_logo_url=req.clubLogoUrl,
            chat_url=req.chatUrl,
        )

        return SignUpClubLeaderResponse(status=200, message="회원가입 성공", data=None)

    def login(self, db: Session, req: LoginRequest) -> LoginResponse:
        user = self.repository.find_user_by_id(db, req.userId)
        if user is None:
            raise ValueError("Invalid credentials")
        if not verify_password(req.password, user.password_hash):
            raise ValueError("Invalid credentials")

        pair = create_token_pair(user.user_id)
        return LoginResponse(
            status=200,
            message="로그인 성공",
            data=TokenPair(
                accessToken=pair["access_token"],
                refreshToken=pair["refresh_token"],
                tokenType=pair["token_type"],
            ),
        )

    def refresh_access_token(
        self, db: Session, req: RefreshTokenRequest
    ) -> RefreshTokenResponse:
        payload = decode_token(req.refreshToken)
        if payload.get("type") != "refresh":
            raise ValueError("Invalid token type")
        jti = payload.get("jti")
        if jti and self.token_repository.is_revoked(jti):
            raise ValueError("Token revoked")
        # NOTE: No persistence check per ERD policy
        sub = payload.get("sub")
        access = create_access_token(sub)
        return RefreshTokenResponse(
            status=200,
            message="Access Token이 성공적으로 재발급되었습니다.",
            data=AccessTokenData(accessToken=access),
        )

    def logout(self, db: Session, token: str) -> None:
        payload = decode_token(token)
        jti = payload.get("jti")
        exp = payload.get("exp")
        if jti and exp:
            # exp는 epoch seconds
            expires_at = datetime.fromtimestamp(exp, tz=timezone.utc)
            self.token_repository.revoke(jti, expires_at)
            # NOTE: No stored token to delete per ERD policy
