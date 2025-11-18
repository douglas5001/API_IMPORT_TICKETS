from fastapi import HTTPException, Depends
from app.utils.user.auth import get_current_user

def permission_required(required_perms: list[str]):
    def wrapper(user = Depends(get_current_user)):
        if user.is_admin:
            return True

        profile = user.profile

        if not profile:
            raise HTTPException(status_code=403, detail="Perfil não associado ao usuário.")

        user_perms = {perm.name for perm in profile.permissions}

        if not any(p in user_perms for p in required_perms):
            raise HTTPException(status_code=403, detail="Permissão negada.")

        return True
    return wrapper
