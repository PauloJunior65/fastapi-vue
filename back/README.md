# Comandos:
### Altualizar o pip do python
```python
python -m pip install --upgrade pip
```
### Criar um ambiente virtual
```python
python -m venv .venv
```
### Desinstalar todas as dependências
```python
pip freeze | xargs pip uninstall -y
```
### Criar o arquivo requirementos com suas dependencias
```python
pip3 freeze > requirements.txt
```
### Instalar as dependências do arquivo de requerimentos
```python
pip3 install -r requirements.txt --upgrade
```
### Rodar a aplicação
```python
uvicorn main:app --reload
```
### Gerar Tradução - [DOC](https://github.com/Anbarryprojects/fastapi-babel)
```python
pybabel extract -F utils/babel.cfg -o utils/messages.pot .
pybabel extract -F utils/babel.cfg -o messages.pot .
pybabel init -i utils/messages.pot -d lang -l en
pybabel init -i utils/messages.pot -d lang -l pt_br
pybabel compile -d lang
```
### Gerar arquivo de migração no banco
```python
alembic revision --autogenerate -m "First migration"
alembic upgrade head
```
### Sincronizar permissões e grupos
```python
echo SQLALCHEMY_WARN_20=0 python permissions.py
```
