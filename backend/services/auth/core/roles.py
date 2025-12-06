from enum import Enum
from typing import Callable, Any, Iterable
from fastapi import Depends, HTTPException, status

class UserRole(str, Enum):
    PASSAGER = "PASSAGER"
    COMPAGNIE = "compagnie"
    ATC = "ATC"
    ADMIN = "ADMIN"

    # Remplacez par votre dépendance qui renvoie l'utilisateur courant (p. ex. get_current_active_user)
    # from .dependencies import get_current_active_user as get_current_user

def allow(*allowed_roles: UserRole, get_current_user=Depends(lambda: None)) -> Callable[..., Any]:
        """
        Dépendance FastAPI à utiliser dans les routes pour restreindre l'accès selon les rôles.
        Exemple d'utilisation (après avoir importé et/ou défini get_current_user) :
          @router.get("/admin", dependencies=[Depends(allow(UserRole.ADMIN))])
        Assure que `current_user` retourné par `get_current_user` a un attribut `role` (str) ou `roles` (iterable).
        """
        def _checker(current_user=Depends(get_current_user)):
            if current_user is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

            # récupère le(s) rôle(s) de l'utilisateur
            user_roles = getattr(current_user, "roles", None) or getattr(current_user, "role", None)
            if user_roles is None:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No role information")

            # normalise en iterable de strings
            if isinstance(user_roles, str):
                user_roles_iter = {user_roles}
            else:
                try:
                    user_roles_iter = set(str(r) for r in user_roles)
                except TypeError:
                    user_roles_iter = {str(user_roles)}

            allowed_set = set(r.value if isinstance(r, UserRole) else str(r) for r in allowed_roles)
            if not user_roles_iter.intersection(allowed_set):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")

            return current_user

        return Depends(_checker)
