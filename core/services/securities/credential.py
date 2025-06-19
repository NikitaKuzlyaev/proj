class AccountCredentialVerifier:
    def is_username_available(self, username: str | None) -> bool:
        return not username


def get_credential_verifier() -> AccountCredentialVerifier:
    return AccountCredentialVerifier()


account_credential_verifier: AccountCredentialVerifier = get_credential_verifier()
