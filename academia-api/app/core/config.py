# Este arquivo lê as configurações do projeto (vindas do arquivo .env)
# e as entrega prontas para o resto da aplicação.

from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuracoes(BaseSettings):
    # Estes nomes são iguais aos do .env. Se algum faltar lá, o programa
    # para logo na partida, com um erro claro (melhor do que falhar depois).
    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    CHAVE_SECRETA_JWT: str
    EXPIRACAO_DO_TOKEN_MINUTOS: int = 30
    ALGORITMO_JWT: str = "HS256"



    # Onde o banco está. Os valores abaixo são os padrões para rodar a API
    # no seu computador: o Docker abriu a porta 3307 para o banco.
    BANCO_HOST: str = "127.0.0.1"
    BANCO_PORTA: int = 3307

    # Diz de onde ler as variáveis. "extra=ignore" é necessário porque o .env
    # também tem a MYSQL_ROOT_PASSWORD, que a API NÃO usa: sem isso, o
    # Pydantic daria erro por causa dessa variável "sobrando".
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def url_do_banco(self) -> str:
        # Monta o "endereço" completo do banco no formato do SQLAlchemy.
        # quote_plus protege caracteres especiais da senha (como @ ou #),
        # que quebrariam o endereço se fossem colocados direto.
        senha_protegida = quote_plus(self.MYSQL_PASSWORD)
        return (
            f"mysql+pymysql://{self.MYSQL_USER}:{senha_protegida}"
            f"@{self.BANCO_HOST}:{self.BANCO_PORTA}/{self.MYSQL_DATABASE}"
        )


# Criamos uma instância única. Quem precisar de configuração importa esta.
configuracoes = Configuracoes()