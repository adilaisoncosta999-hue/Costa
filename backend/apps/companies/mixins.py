class CompanyScopedMixin:
    """
    Garante que cada utilizador só vê e cria dados da sua própria empresa.
    O super_admin tem acesso a tudo (usado no painel global do SaaS).
    """

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if not user.is_authenticated:
            return qs.none()
        if user.is_super_admin:
            return qs
        return qs.filter(company=user.company)

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_super_admin and 'company' in serializer.validated_data:
            serializer.save()
        else:
            serializer.save(company=user.company)
