# SecureVault - Gerenciador de Senhas 🔒

<div align="center">

![SecureVault Logo](docs/images/logo.png)

[![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-green.svg)](https://github.com/JoaoSantosCodes/SecureVault)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-yellow.svg)](https://www.python.org/)
[![Qt](https://img.shields.io/badge/Qt-5.15+-green.svg)](https://www.qt.io/)

</div>

## 📋 Sobre

SecureVault é um gerenciador de senhas seguro e fácil de usar, desenvolvido em Python com interface gráfica em PyQt5. Ele permite armazenar e gerenciar suas senhas de forma criptografada e segura.

## ✨ Funcionalidades

### 🎨 Interface Moderna
- Design minimalista e intuitivo
- Tema escuro por padrão
- Botões de ação com feedback visual
- Tooltips informativos
- Animações suaves
- Hierarquia visual com cores sutis

### 🔑 Gerenciamento de Senhas
- Armazenamento seguro com criptografia AES
- Visualização rápida de senhas
- Edição de entradas existentes
- Exclusão segura de dados
- Sistema de múltiplos usuários
- Geração de senhas fortes

### 🔄 Recuperação de Senha
- Recuperação via email com código de verificação
- Opção de senha administrativa de backup
- Processo seguro de redefinição
- Senhas temporárias automáticas

### 📤 Importação/Exportação
- Suporte para arquivos CSV
- Suporte para arquivos JSON
- Backup criptografado
- Migração facilitada

### 🛡️ Segurança
- Criptografia AES para senhas
- Proteção por senha mestra
- Timeout de sessão
- Logs de segurança
- Configurações criptografadas
- Salt e hash para senhas de usuários

## 🚀 Instalação

### Via Instalador
1. Baixe o instalador mais recente da [página de releases](https://github.com/JoaoSantosCodes/SecureVault/releases)
2. Execute o instalador
3. Inicie o SecureVault
4. Crie sua senha mestra na primeira execução

### Via Código Fonte
```bash
# Clone o repositório
git clone https://github.com/JoaoSantosCodes/SecureVault.git

# Entre no diretório
cd SecureVault

# Instale as dependências
pip install -r requirements.txt

# Execute o aplicativo
python main.py
```

## 💻 Desenvolvimento

### Pré-requisitos
- Python 3.11+
- PyQt5 5.15+
- cryptography 41.0+
- Outras dependências listadas em requirements.txt

### Configuração do Ambiente
1. Configure um ambiente virtual (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute os testes:
   ```bash
   pytest
   ```

## 📝 Configuração

### Email de Recuperação
Para configurar o sistema de recuperação por email:

1. Abra o arquivo `config.enc`
2. Configure as informações do servidor SMTP:
   ```json
   {
     "email": {
       "smtp_server": "smtp.gmail.com",
       "smtp_port": 587,
       "email": "seu_email@gmail.com",
       "password": "sua_senha_de_app"
     }
   }
   ```
3. Para Gmail, use uma [senha de aplicativo](https://support.google.com/accounts/answer/185833)

### Senha Administrativa
Para configurar a senha administrativa:

1. Abra o arquivo `config.enc`
2. Defina a senha de administrador:
   ```json
   {
     "admin_password": "sua_senha_admin"
   }
   ```

## 🎯 Próximos Passos

- [ ] Categorização de senhas
- [ ] Análise de força de senhas
- [ ] Sincronização em nuvem
- [ ] Autenticação em dois fatores
- [ ] Temas personalizados
- [ ] Backup automático
- [ ] Histórico de senhas
- [ ] Compartilhamento seguro

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/AmazingFeature`)
3. Faça o Commit de suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Faça o Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.
