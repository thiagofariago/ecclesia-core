"""
Script de seed para popular o banco de dados com dados iniciais.
Pode ser executado múltiplas vezes (idempotente).
"""
from datetime import date, timedelta
from decimal import Decimal

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.usuario import Usuario, RoleEnum
from app.models.paroquia import Paroquia
from app.models.comunidade import Comunidade
from app.models.dizimista import Dizimista
from app.models.contribuicao import Contribuicao, TipoContribuicaoEnum
from app.auth.utils import get_password_hash


def seed_database():
    """Popula o banco de dados com dados iniciais."""
    db: Session = SessionLocal()

    try:
        print("Iniciando seed do banco de dados...")

        # 1. Criar Paróquia
        paroquia = db.query(Paroquia).filter(Paroquia.nome == "Paróquia São João").first()
        if not paroquia:
            paroquia = Paroquia(nome="Paróquia São João")
            db.add(paroquia)
            db.commit()
            db.refresh(paroquia)
            print("✓ Paróquia criada")
        else:
            print("✓ Paróquia já existe")

        # 2. Criar Comunidades
        comunidade1 = db.query(Comunidade).filter(
            Comunidade.nome == "Comunidade São Pedro",
            Comunidade.paroquia_id == paroquia.id
        ).first()
        if not comunidade1:
            comunidade1 = Comunidade(
                nome="Comunidade São Pedro",
                paroquia_id=paroquia.id
            )
            db.add(comunidade1)
            db.commit()
            db.refresh(comunidade1)
            print("✓ Comunidade São Pedro criada")
        else:
            print("✓ Comunidade São Pedro já existe")

        comunidade2 = db.query(Comunidade).filter(
            Comunidade.nome == "Comunidade Santa Maria",
            Comunidade.paroquia_id == paroquia.id
        ).first()
        if not comunidade2:
            comunidade2 = Comunidade(
                nome="Comunidade Santa Maria",
                paroquia_id=paroquia.id
            )
            db.add(comunidade2)
            db.commit()
            db.refresh(comunidade2)
            print("✓ Comunidade Santa Maria criada")
        else:
            print("✓ Comunidade Santa Maria já existe")

        # 3. Criar Usuários
        admin = db.query(Usuario).filter(Usuario.email == "admin@ecclesia.com").first()
        if not admin:
            admin = Usuario(
                nome="Administrador do Sistema",
                email="admin@ecclesia.com",
                senha_hash=get_password_hash("Admin123!"),
                role=RoleEnum.ADMIN,
                ativo=True
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print("✓ Usuário Admin criado (email: admin@ecclesia.com, senha: Admin123!)")
        else:
            print("✓ Usuário Admin já existe")

        operador = db.query(Usuario).filter(Usuario.email == "operador@ecclesia.com").first()
        if not operador:
            operador = Usuario(
                nome="Operador do Sistema",
                email="operador@ecclesia.com",
                senha_hash=get_password_hash("Opera123!"),
                role=RoleEnum.OPERADOR,
                ativo=True
            )
            db.add(operador)
            db.commit()
            db.refresh(operador)
            print("✓ Usuário Operador criado (email: operador@ecclesia.com, senha: Opera123!)")
        else:
            print("✓ Usuário Operador já existe")

        # 4. Criar Dizimistas
        hoje = date.today()
        mes_atual = hoje.month
        ano_atual = hoje.year

        dizimistas_data = [
            {
                "nome": "João da Silva",
                "comunidade_id": comunidade1.id,
                "cpf": "123.456.789-01",
                "telefone": "(11) 98765-4321",
                "email": "joao.silva@email.com",
                "data_nascimento": date(1975, mes_atual, 10),  # Aniversário este mês
                "endereco": "Rua das Flores, 123",
                "ativo": True,
            },
            {
                "nome": "Maria Santos",
                "comunidade_id": comunidade1.id,
                "cpf": "234.567.890-12",
                "telefone": "(11) 98765-4322",
                "email": "maria.santos@email.com",
                "data_nascimento": date(1980, mes_atual, 20),  # Aniversário este mês
                "endereco": "Av. Principal, 456",
                "ativo": True,
            },
            {
                "nome": "Pedro Oliveira",
                "comunidade_id": comunidade2.id,
                "cpf": "345.678.901-23",
                "telefone": "(11) 98765-4323",
                "email": "pedro.oliveira@email.com",
                "data_nascimento": date(1965, 3, 15),
                "endereco": "Rua dos Pinheiros, 789",
                "ativo": True,
            },
            {
                "nome": "Ana Costa",
                "comunidade_id": comunidade2.id,
                "cpf": None,
                "telefone": "(11) 98765-4324",
                "email": None,
                "data_nascimento": date(1990, mes_atual, 5),  # Aniversário este mês
                "endereco": None,
                "ativo": True,
            },
            {
                "nome": "Carlos Mendes",
                "comunidade_id": comunidade1.id,
                "cpf": "456.789.012-34",
                "telefone": "(11) 98765-4325",
                "email": "carlos.mendes@email.com",
                "data_nascimento": date(1955, 6, 25),
                "endereco": "Praça Central, 101",
                "ativo": False,  # Inativo
            },
        ]

        dizimistas = []
        for data in dizimistas_data:
            dizimista = db.query(Dizimista).filter(Dizimista.cpf == data["cpf"]).first() if data["cpf"] else None
            if not dizimista:
                dizimista = db.query(Dizimista).filter(Dizimista.nome == data["nome"]).first()

            if not dizimista:
                dizimista = Dizimista(**data)
                db.add(dizimista)
                dizimistas.append(dizimista)

        if dizimistas:
            db.commit()
            for diz in dizimistas:
                db.refresh(diz)
            print(f"✓ {len(dizimistas)} dizimista(s) criado(s)")
        else:
            print("✓ Dizimistas já existem")
            dizimistas = db.query(Dizimista).all()

        # 5. Criar Contribuições
        # Verificar se já existem contribuições
        existing_count = db.query(Contribuicao).count()
        if existing_count == 0:
            contribuicoes_data = [
                {
                    "dizimista_id": dizimistas[0].id,
                    "comunidade_id": comunidade1.id,
                    "tipo": TipoContribuicaoEnum.DIZIMO,
                    "valor": Decimal("150.00"),
                    "data_contribuicao": hoje - timedelta(days=30),
                    "forma_pagamento": "PIX",
                    "referencia_mes": (hoje - timedelta(days=30)).strftime("%Y-%m"),
                },
                {
                    "dizimista_id": dizimistas[0].id,
                    "comunidade_id": comunidade1.id,
                    "tipo": TipoContribuicaoEnum.DIZIMO,
                    "valor": Decimal("150.00"),
                    "data_contribuicao": hoje - timedelta(days=60),
                    "forma_pagamento": "PIX",
                    "referencia_mes": (hoje - timedelta(days=60)).strftime("%Y-%m"),
                },
                {
                    "dizimista_id": dizimistas[1].id,
                    "comunidade_id": comunidade1.id,
                    "tipo": TipoContribuicaoEnum.DIZIMO,
                    "valor": Decimal("200.00"),
                    "data_contribuicao": hoje - timedelta(days=15),
                    "forma_pagamento": "Dinheiro",
                    "referencia_mes": hoje.strftime("%Y-%m"),
                },
                {
                    "dizimista_id": dizimistas[1].id,
                    "comunidade_id": comunidade1.id,
                    "tipo": TipoContribuicaoEnum.OFERTA,
                    "valor": Decimal("50.00"),
                    "data_contribuicao": hoje - timedelta(days=7),
                    "forma_pagamento": "Dinheiro",
                },
                {
                    "dizimista_id": dizimistas[2].id,
                    "comunidade_id": comunidade2.id,
                    "tipo": TipoContribuicaoEnum.DIZIMO,
                    "valor": Decimal("300.00"),
                    "data_contribuicao": hoje - timedelta(days=20),
                    "forma_pagamento": "Transferência",
                    "referencia_mes": hoje.strftime("%Y-%m"),
                },
                {
                    "dizimista_id": dizimistas[2].id,
                    "comunidade_id": comunidade2.id,
                    "tipo": TipoContribuicaoEnum.OFERTA,
                    "valor": Decimal("100.00"),
                    "data_contribuicao": hoje - timedelta(days=10),
                    "forma_pagamento": "PIX",
                },
                {
                    "dizimista_id": dizimistas[3].id,
                    "comunidade_id": comunidade2.id,
                    "tipo": TipoContribuicaoEnum.DIZIMO,
                    "valor": Decimal("100.00"),
                    "data_contribuicao": hoje - timedelta(days=5),
                    "forma_pagamento": "Dinheiro",
                    "referencia_mes": hoje.strftime("%Y-%m"),
                },
                {
                    "dizimista_id": None,  # Contribuição anônima
                    "comunidade_id": comunidade1.id,
                    "tipo": TipoContribuicaoEnum.OFERTA,
                    "valor": Decimal("25.00"),
                    "data_contribuicao": hoje - timedelta(days=3),
                    "forma_pagamento": "Dinheiro",
                },
                {
                    "dizimista_id": None,  # Contribuição anônima
                    "comunidade_id": comunidade2.id,
                    "tipo": TipoContribuicaoEnum.OFERTA,
                    "valor": Decimal("30.00"),
                    "data_contribuicao": hoje - timedelta(days=1),
                    "forma_pagamento": "Dinheiro",
                },
                {
                    "dizimista_id": dizimistas[0].id,
                    "comunidade_id": comunidade1.id,
                    "tipo": TipoContribuicaoEnum.OFERTA,
                    "valor": Decimal("75.00"),
                    "data_contribuicao": hoje,
                    "forma_pagamento": "PIX",
                },
            ]

            for contrib_data in contribuicoes_data:
                contribuicao = Contribuicao(**contrib_data)
                db.add(contribuicao)

            db.commit()
            print("✓ 10 contribuições criadas")
        else:
            print(f"✓ Contribuições já existem ({existing_count} registros)")

        print("\n✅ Seed concluído com sucesso!")
        print("\nCredenciais de acesso:")
        print("Admin: admin@ecclesia.com / Admin123!")
        print("Operador: operador@ecclesia.com / Opera123!")

    except Exception as e:
        print(f"\n❌ Erro durante o seed: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
