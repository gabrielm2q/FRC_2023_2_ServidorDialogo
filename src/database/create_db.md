### Comandos para criacão do novo usuario no banco de dados Postgres

Logado como o usuário padrao _postgres_, executar os comandos abaixo:

```sql
-- Criando novo user
CREATE USER frc WITH SUPERUSER CREATEDB CREATEROLE LOGIN PASSWORD '123123';

-- Criando nova base de dados
CREATE DATABASE chat WITH OWNER frc;

-- Colocando permissoes
GRANT ALL PRIVILEGES ON DATABASE chat TO frc;
```
