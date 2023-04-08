from utils.database import get_engine
from sqlalchemy import text, Connection
from fastapi_babel import _
import click

permissions = {
    'user': {
        'name': _("Usuários"),
        'description': _("Permite a criação, edição e remoção de usuários."),
        'permissions': {
            'view': _("Visualizar usuários."),
            'add': _("Adicionar usuários."),
            'edit': _("Editar usuários."),
            'delete': _("Remover usuários."),
        }
    },
    'group': {
        'name': _("Grupos"),
        'description': _("Permite a criação, edição e remoção de grupos."),
        'permissions': {
            'view': _("Visualizar grupos."),
            'add': _("Adicionar grupos."),
            'edit': _("Editar grupos."),
            'delete': _("Remover grupos."),
        }
    }
}

groups = [
    {
        'name': "Administrador",
        'modules': None
    },
    # {
    #     'name': "Teste 1",
    #     # 'modules': ['user'],
    # },
    # {
    #     'name': "Teste 2",
    #     'modules': {
    #         'user': ['view'],
    #         'group': None,
    #     },
    # },
]


help_group_perms = """
Manipulação de grupos e permissões do sistema:\n
    - sync: Sincroniza as permissões do sistema com o banco de dados.\n
"""


def cmd_group_perms(cmd: click.Group):
    @cmd.command(
        "sync",
        help="""Sincroniza as permissões do sistema com o banco de dados.""",
    )
    def sync():
        with get_engine().connect() as db:
            sync_perms(db)
            db.commit()

    def sync_perms(db: Connection):
        click.echo("Validando permissões...")
        for group, data in permissions.items():
            if not isinstance(group, str):
                click.echo(f"O código do grupo {group} não é uma string.")
                raise click.Abort
            if not isinstance(data, dict):
                click.echo(f"Os dados do grupo {group} não são um dicionário.")
                raise click.Abort
            if all(key not in data for key in ['name', 'description', 'permissions']):
                click.echo(
                    f"Os dados do grupo {group} não contém os campos 'name', 'description' e 'permissions'.")
                raise click.Abort
            if not isinstance(data['name'], str):
                click.echo(
                    f"O nome do grupo {group} não é uma string.")
                raise click.Abort
            if not isinstance(data['description'], str):
                click.echo(
                    f"A descrição do grupo {group} não é uma string.")
                raise click.Abort
            if not isinstance(data['permissions'], dict):
                click.echo(
                    f"As permissões do grupo {group} não são um dicionário.")
                raise click.Abort
            for perm, name in data['permissions'].items():
                if not isinstance(perm, str):
                    click.echo(
                        f"O código da permissão {perm} do grupo {group} não é uma string.")
                    raise click.Abort
                if not isinstance(name, str):
                    click.echo(
                        f"O nome da permissão {perm} do grupo {group} não é uma string.")
                    raise click.Abort
        click.echo("Sincronizando permissões...")
        code_group_perms = list()
        code_perms = list()
        for group, data in permissions.items():
            db.execute(text("INSERT INTO `auth_permission_group`(`group`, `name`, `description`) VALUES (:group,:name,:description) ON DUPLICATE KEY UPDATE `group`=:group, name=:name,description=:description;"), {
                'group': group,
                'name': data['name'],
                'description': data['description']
            })
            code_group_perms.append(group)
            click.echo(f"\tGrupo {group} sincronizado.")
            for perm, name in data['permissions'].items():
                db.execute(text("INSERT INTO `auth_permission`(`group`, `code`, `name`) VALUES (:group,:code,:name) ON DUPLICATE KEY UPDATE `group`=:group, `code`=:code,name=:name;"), {
                    'group': group,
                    'code': perm,
                    'name': name
                })
                code_perms.append(f'{group}.{perm}')
                click.echo(f"\t\tPermissão {group}.{perm} sincronizada.")
        for item in db.execute(text("SELECT `group` FROM `auth_permission_group`;")).fetchall():
            if item.group not in code_group_perms:
                db.execute(text("DELETE FROM `auth_permission_group` WHERE `group`=:group;"), {
                    'group': item.group
                })
                click.echo(f"\tGrupo {item.group} removido.")
        for item in db.execute(text("SELECT CONCAT(`group`,'.',`code`) as `perm`,`group`,`code` FROM `auth_permission`;")).fetchall():
            if item.perm not in code_perms:
                db.execute(text("DELETE FROM `auth_permission` WHERE `group`=:group AND `code`=:code;"), {
                    'group': item.group,
                    'code': item.code
                })
                click.echo(
                    f"\tPermissão {item.group}.{item.code} removida.")

    @cmd.command(
        "sync-groups",
        help="""Sicroniza os grupos do sistema com o banco de dados.""",
    )
    def sync_groups():
        with get_engine().connect() as db:
            sync_perms(db)
            list_perms = [(group, perm) for group, data in permissions.items()
                          for perm in data['permissions'].keys()]
            # Validação dos grupos
            click.echo("Validando grupos...")
            for n, group in enumerate(groups):
                if not isinstance(group, dict):
                    click.echo(
                        f"Grupo {n} inválido | Deve ser um dicionário.", err=True)
                    raise click.Abort
                if not all([i in group.keys() for i in ['name', 'modules']]):
                    click.echo(
                        f"Grupo {n} inválido | Campos obrigatórios: name, modules.", err=True)
                    raise click.Abort
                if not isinstance(group['name'], str):
                    click.echo(
                        f"Grupo {n} inválido | Campo name deve ser uma string.", err=True)
                    raise click.Abort
                if not isinstance(group['modules'], (list, dict, type(None))):
                    click.echo(
                        f"Grupo {n} inválido | Campo modules deve ser uma lista, dicionário ou None.", err=True)
                    raise click.Abort
                if isinstance(group['modules'], list):
                    for n, module in enumerate(group['modules']):
                        if not isinstance(module, str):
                            click.echo(
                                f"Grupo {n} inválido | Campo modules[{n}] deve ser uma string.", err=True)
                            raise click.Abort
                        if module not in permissions.keys():
                            click.echo(
                                f"Grupo {n} inválido | Módulo {module} não encontrado.", err=True)
                            raise click.Abort
                if isinstance(group['modules'], dict):
                    for module, perms in group['modules'].items():
                        if not isinstance(module, str):
                            click.echo(
                                f"Grupo {n} inválido | A chave do campo modules deve ser uma string. | {module}", err=True)
                            raise click.Abort
                        if module not in permissions.keys():
                            click.echo(
                                f"Grupo {n} inválido | Módulo {module} não encontrado.", err=True)
                            raise click.Abort
                        if not isinstance(perms, (list, type(None))):
                            click.echo(
                                f"Grupo {n} inválido | Campo modules[{module}] deve ser uma lista ou None.", err=True)
                            raise click.Abort
                        if isinstance(perms, list):
                            for n, perm in enumerate(perms):
                                if not isinstance(perm, str):
                                    click.echo(
                                        f"Grupo {n} inválido | Campo modules[{module}][{n}] deve ser uma string.", err=True)
                                    raise click.Abort
                                if perm not in permissions[module]['permissions'].keys():
                                    click.echo(
                                        f"Grupo {n} inválido | Permissão {perm} não encontrada no módulo {module}.", err=True)
                                    raise click.Abort
            # Sincronização dos grupos
            click.echo("Sincronizando grupos...")
            for group in groups:
                item = db.execute(text("SELECT id FROM `auth_group` WHERE `name`=:name LIMIT 1;"), {
                    'name': group['name']
                }).fetchone()
                if item is None:
                    item = db.execute(text("INSERT INTO `auth_group`(`name`) VALUES (:name);"), {
                        'name': group['name']
                    }).lastrowid
                else:
                    item = item.id
                click.echo(f"\tGrupo {group['name']} sincronizado.")
                db.execute(text("DELETE FROM `auth_group_has_permission` WHERE `group_id`=:group_id;"), {
                    'group_id': item
                })
                modules = group['modules']
                for group_name, perm_name in list_perms:
                    if modules is None or \
                        (isinstance(modules, list) and group_name in modules) or \
                            (isinstance(modules, dict) and group_name in modules.keys() and (modules[group_name] is None or perm_name in modules[group_name])):
                        db.execute(text("INSERT INTO `auth_group_has_permission`(`group_id`, `permission_group`, `permission_code`) VALUES (:group_id,:permission_group,:permission_code);"), {
                            'group_id': item,
                            'permission_group': group_name,
                            'permission_code': perm_name
                        })
                        click.echo(
                            f"\t\tPermissão {group_name}.{perm_name} sincronizada.")
            db.commit()
