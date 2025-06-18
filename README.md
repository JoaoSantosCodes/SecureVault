# SecureVault

<div align="center">
  <img src="docs/images/logo.png" alt="SecureVault Logo" width="150">
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
  [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
  [![PyQt5](https://img.shields.io/badge/PyQt-5.15+-green.svg)](https://pypi.org/project/PyQt5/)
  [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

  <h3>Um gerenciador de senhas moderno e seguro desenvolvido em Python</h3>
</div>

SecureVault é um gerenciador de senhas que combina segurança robusta com uma interface elegante, oferecendo uma solução completa para o gerenciamento de suas credenciais digitais.

<div align="center">
  <img src="docs/images/main_screen.png" alt="Tela Principal" width="600">
</div>

## 🌟 Destaques

- 🔒 **Segurança Robusta**: Criptografia AES-256 e hash SHA-256
- 🎨 **Interface Moderna**: Tema escuro elegante com PyQt5
- 💾 **Armazenamento Local**: Seus dados nunca saem do seu computador
- 🔑 **Senha Mestra**: Proteção adicional para seus dados
- 🔄 **Backup Automático**: Nunca perca suas senhas
- 🎯 **Fácil de Usar**: Interface intuitiva e amigável

## 📸 Screenshots

<div align="center">
  <img src="docs/images/login_screen.png" alt="Tela de Login" width="300">
  <img src="docs/images/add_password.png" alt="Adicionar Senha" width="300">
  <br>
  <img src="docs/images/settings_screen.png" alt="Configurações" width="300">
  <img src="docs/images/generator_screen.png" alt="Gerador de Senhas" width="300">
</div>

## 🚀 Instalação

### Usando o Executável

1. Baixe a [última versão](https://github.com/seu-usuario/securevault/releases/latest) do SecureVault
2. Extraia o arquivo ZIP
3. Execute `SecureVault.exe` na pasta extraída

### Instalando do Código Fonte

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/securevault.git

# Entre no diretório
cd securevault

# Instale as dependências
pip install -r requirements.txt

# Execute o programa
python main.py
```

## 📦 Dependências

| Pacote | Versão | Descrição |
|--------|---------|------------|
| PyQt5 | >=5.15.0 | Framework GUI |
| cryptography | >=3.4.7 | Criptografia |
| python-dotenv | ==1.0.0 | Variáveis de ambiente |
| Pillow | >=9.0.0 | Processamento de imagens |
| pytest | ==7.4.0 | Testes unitários |
| black | ==23.3.0 | Formatação de código |
| flake8 | ==6.0.0 | Linting |
| mypy | ==1.3.0 | Verificação de tipos |

## 🎨 Interface

### Tema e Cores
- **Principal**: Verde Esmeralda (#2ecc71)
- **Fundo**: Cinza Escuro (#232323)
- **Texto**: Branco Suave (#e0e0e0)
- **Destaque**: Verde Claro (#44ff44)
- **Bordas**: Cinza Médio (#333333)

### Componentes
- Fonte principal: Segoe UI (10pt)
- Fonte de logs: Consolas
- Ícones personalizados
- Animações suaves
- Design responsivo

<div align="center">
  <img src="docs/images/theme_preview.png" alt="Preview do Tema" width="800">
</div>

## 🔒 Segurança

### Criptografia
- AES-256-GCM para dados sensíveis
- SHA-256 para hash da senha mestra
- Salt único por usuário
- Chaves derivadas com PBKDF2

### Proteção
- Timeout de sessão
- Limpeza de memória
- Proteção contra força bruta
- Backup criptografado

## 🛠️ Desenvolvimento

### Estrutura do Projeto
```
securevault/
├── core/                   # Lógica principal
│   ├── __init__.py
│   ├── crypto.py          # Funções de criptografia
│   ├── database.py        # Gerenciamento de dados
│   └── password_manager.py # Gerenciador de senhas
├── ui/                     # Interface gráfica
│   ├── __init__.py
│   ├── styles/            # Estilos e temas
│   ├── dialogs/           # Janelas de diálogo
│   └── password_widget.py # Widget principal
├── resources/             # Recursos
│   ├── images/           # Imagens e ícones
│   └── generate_icon.py  # Gerador de ícones
├── tests/                # Testes
│   ├── __init__.py
│   └── test_*.py        # Arquivos de teste
├── docs/                 # Documentação
├── main.py              # Ponto de entrada
├── requirements.txt     # Dependências
└── README.md           # Este arquivo
```

### Métricas de Código
- Cobertura de testes: >90%
- Conformidade com PEP 8
- Tipagem estática com mypy
- Documentação completa

## 📊 Status do Projeto

- ✅ **Versão**: 1.0.0
- 🏗️ **Status**: Ativo
- 📈 **Cobertura de Testes**: 92%
- 🐛 **Issues Abertas**: [Ver no GitHub](https://github.com/seu-usuario/securevault/issues)

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Guia de Contribuição
- Siga o estilo de código existente
- Adicione testes para novas funcionalidades
- Atualize a documentação
- Verifique se todos os testes passam

## ✨ Agradecimentos

- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) pela excelente framework GUI
- [cryptography](https://cryptography.io/) pela robusta biblioteca de criptografia
- Todos os contribuidores e usuários do projeto

---
<div align="center">
  <sub>Construído com ❤️ pela comunidade</sub>
</div>
