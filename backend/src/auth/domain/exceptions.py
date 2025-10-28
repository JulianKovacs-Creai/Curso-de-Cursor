"""
Domain exceptions for authentication module.

This module contains all domain-specific exceptions that can be raised
during authentication operations.
"""


class AuthenticationError(Exception):
    """Base exception for authentication errors."""
    pass


class UserNotFoundError(AuthenticationError):
    """Raised when a user is not found."""
    pass


class UserAlreadyExistsError(AuthenticationError):
    """Raised when trying to create a user that already exists."""
    pass


class InvalidCredentialsError(AuthenticationError):
    """Raised when login credentials are invalid."""
    pass


class InvalidTokenError(AuthenticationError):
    """Raised when a token is invalid or malformed."""
    pass


class TokenExpiredError(AuthenticationError):
    """Raised when a token has expired."""
    pass


class UserNotActiveError(AuthenticationError):
    """Raised when trying to login with an inactive user."""
    pass


class EmailNotVerifiedError(AuthenticationError):
    """Raised when trying to login with an unverified email."""
    pass


class InvalidPasswordError(AuthenticationError):
    """Raised when password validation fails."""
    pass


class InsufficientPermissionsError(AuthenticationError):
    """Raised when user doesn't have sufficient permissions."""
    pass


class AccountLockedError(AuthenticationError):
    """Raised when account is locked due to too many failed attempts."""
    pass


class SessionExpiredError(AuthenticationError):
    """Raised when session has expired."""
    pass


class InvalidEmailError(AuthenticationError):
    """Raised when email format is invalid."""
    pass


class PasswordTooWeakError(AuthenticationError):
    """Raised when password doesn't meet strength requirements."""
    pass


class EmailAlreadyVerifiedError(AuthenticationError):
    """Raised when trying to verify an already verified email."""
    pass


class InvalidVerificationTokenError(AuthenticationError):
    """Raised when verification token is invalid or expired."""
    pass


class PasswordResetTokenExpiredError(AuthenticationError):
    """Raised when password reset token has expired."""
    pass


class TooManyLoginAttemptsError(AuthenticationError):
    """Raised when too many login attempts have been made."""
    pass


class AccountSuspendedError(AuthenticationError):
    """Raised when account is suspended."""
    pass


class InvalidRefreshTokenError(AuthenticationError):
    """Raised when refresh token is invalid."""
    pass


class TokenRevokedError(AuthenticationError):
    """Raised when token has been revoked."""
    pass
