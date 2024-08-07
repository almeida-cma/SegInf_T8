# SegInf_T8
LGPD

--------CRIAR TABELA EM DATABASE-----------------------------------
DATABASE: seguro

CREATE TABLE consentimentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    consentimento_comunicacoes BOOLEAN NOT NULL,
    consentimento_cookies BOOLEAN NOT NULL,
    data_consentimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-------------------------------------------------------------------

----------------------TESTE PREFERENCIAS---------------------------
http://localhost/LGPD/preferencias.php?email=usuario@example.com
-------------------------------------------------------------------

------------------------------------------------------------------
Implementação de 2 etapas via Google (senha de apps) - Pasta "2_Etapas_Gmail" deste repositório:

1) Ativar autenticação em 2 etapas na sua conta do Google (pode ser uma nova conta específica para o exemplo);

2) Copiar pasta "src" para seu projeto;

3) Adaptar script "mail.php" confomre informações da sua conta para realizar o envio do e-mail. Não esquecer de referenciar a pasta "src" com o caminho correto no início do script.
