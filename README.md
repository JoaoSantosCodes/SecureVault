# Gerenciador de Senhas

Um aplicativo seguro para gerenciar senhas e sites, desenvolvido com PyQt5 e criptografia moderna.

## Características

- Interface gráfica moderna e intuitiva
- Criptografia segura de senhas
- Armazenamento local criptografado
- Gerenciamento de múltiplas senhas
- Proteção com senha mestra

## Requisitos

- Python 3.7+
- PyQt5
- cryptography

## Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITORIO]
cd gerenciador-senhas
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

1. Execute o programa:
```bash
python main.py
```

2. Na primeira execução, defina uma senha mestra. Esta senha será necessária para acessar suas senhas armazenadas.

3. Após fazer login com a senha mestra, você pode:
   - Adicionar novas senhas
   - Visualizar senhas existentes
   - Excluir senhas
   - Todas as senhas são armazenadas localmente no arquivo `passwords.enc`

## Segurança

- As senhas são criptografadas usando o algoritmo Fernet da biblioteca cryptography
- A senha mestra nunca é armazenada diretamente
- Os dados são armazenados localmente em um arquivo criptografado
- Proteção contra acesso não autorizado através de senha mestra

## Desenvolvimento

O projeto segue uma estrutura modular:

```
gerenciador-senhas/
├── core/
│   ├── __init__.py
│   └── password_manager.py
├── ui/
│   ├── __init__.py
│   └── password_widget.py
├── main.py
├── requirements.txt
└── README.md
```

## Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Crie um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes. 