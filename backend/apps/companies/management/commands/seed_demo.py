from django.core.management.base import BaseCommand
from apps.companies.models import Company, Department, Position, WorkSchedule
from apps.accounts.models import User
from apps.employees.models import Employee


class Command(BaseCommand):
    help = 'Cria dados de demonstração: 1 empresa, 1 admin, departamentos e 3 funcionários.'

    def handle(self, *args, **options):
        company, _ = Company.objects.get_or_create(
            name='Costa Demo Lda',
            defaults={'plan': 'pro', 'max_employees': 50}
        )

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin', email='admin@costa.demo', password='Admin#2026',
                role='super_admin'
            )
            self.stdout.write(self.style.SUCCESS('Super admin criado: admin / Admin#2026'))

        company_admin, created = User.objects.get_or_create(
            username='gestor', defaults={
                'email': 'gestor@costa.demo', 'role': 'company_admin', 'company': company,
            }
        )
        if created:
            company_admin.set_password('Gestor#2026')
            company_admin.save()
            self.stdout.write(self.style.SUCCESS('Admin da empresa criado: gestor / Gestor#2026'))

        dept, _ = Department.objects.get_or_create(company=company, name='Operações')
        position, _ = Position.objects.get_or_create(company=company, department=dept, title='Técnico')
        schedule, _ = WorkSchedule.objects.get_or_create(
            company=company, name='Horário Padrão',
            defaults={'start_time': '08:00', 'end_time': '17:00', 'tolerance_minutes': 10}
        )

        nomes = ['Ana Costa', 'Bruno Fernandes', 'Carla Sousa']
        for i, nome in enumerate(nomes, start=1):
            emp, created = Employee.objects.get_or_create(
                company=company, employee_number=f'F{i:03d}',
                defaults={
                    'full_name': nome, 'department': dept, 'position': position,
                    'schedule': schedule, 'status': 'active',
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Funcionário criado: {nome} (QR token: {emp.qr_token})'))

        self.stdout.write(self.style.SUCCESS('\nDados de demonstração prontos.'))
