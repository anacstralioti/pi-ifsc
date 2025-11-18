def perfil_context(request):
    if request.user.is_authenticated:
        perfil = getattr(request.user, 'perfil', None)
        return {'perfil': perfil}
    return {}