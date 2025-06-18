# SecureVault - Gerenciador de Senhas Seguro

```
  _____     _____ 
 / ____|   |  __ \
| (___     | |  | |
 \___ \    | |  | |
 ____) |   | |__| |
|_____/    |_____/
  
  🛡️ SecureVault: Proteção Moderna para Suas Senhas 🔒
```

<div align="center">
  <img src="resources/images/securevault.png" alt="SecureVault Logo" width="128" height="128">
</div>

SecureVault é um gerenciador de senhas moderno e seguro desenvolvido em Python, oferecendo uma interface gráfica intuitiva e recursos avançados de segurança.

![SecureVault Screenshot](screenshot.png)

## 🔐 Características Principais

- Interface gráfica moderna com tema escuro
- Criptografia forte usando a biblioteca cryptography
- Sistema de senha mestra para proteção
- Armazenamento local seguro
- Log detalhado de atividades
- Design responsivo e intuitivo

## 🛡️ Segurança

O SecureVault implementa as seguintes medidas de segurança:

- Criptografia AES-256 para senhas armazenadas
- Hash bcrypt para senha mestra
- Proteção contra ataques de força bruta
- Dados armazenados localmente (sem transmissão pela internet)
- Limpeza automática da memória após uso
- Timeout de sessão por inatividade

## 📖 Manual de Uso

1. **Primeira Execução**
   - Execute o programa
   - Crie sua senha mestra
   - Configure as preferências iniciais

2. **Gerenciando Senhas**
   - Adicionar nova senha: Clique no botão "+" e preencha os detalhes
   - Visualizar senha: Selecione a entrada desejada
   - Editar senha: Clique duas vezes na entrada
   - Excluir senha: Selecione e use o botão "Excluir"

3. **Recursos Adicionais**
   - Gerador de senhas fortes
   - Backup automático
   - Exportação segura
   - Log de atividades

## 🛠️ Instalação

```bash
# Clone o repositório
git clone https://github.com/JoaoSantosCodes/SecureVault.git

# Entre no diretório
cd SecureVault

# Instale as dependências
pip install -r requirements.txt

# Execute o programa
python main.py
```

## 🗺️ RoadMap

### Versão 1.1 (Próxima)
- [ ] Sincronização com nuvem
- [ ] Autenticação biométrica
- [ ] Importação de senhas de outros gerenciadores
- [ ] Modo offline

### Versão 1.2
- [ ] Apps mobile (iOS/Android)
- [ ] Extensões para navegadores
- [ ] Compartilhamento seguro de senhas
- [ ] Autenticação 2FA

### Versão 1.3
- [ ] Análise de força de senhas
- [ ] Alertas de vazamentos
- [ ] Backup em múltiplos locais
- [ ] Integração com serviços populares

## 📝 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

```
MIT License

Copyright (c) 2024 João Santos

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Suporte

- Email: joao.santos@example.com
- Issues: https://github.com/JoaoSantosCodes/SecureVault/issues
- Wiki: https://github.com/JoaoSantosCodes/SecureVault/wiki

## ✨ Agradecimentos

- Comunidade Python
- Contribuidores do projeto
- Usuários que forneceram feedback

---
Desenvolvido com ❤️ por João Santos 