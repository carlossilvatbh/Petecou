# 🏓 Peteca Scout

Sistema de acompanhamento de partidas de peteca com rankings individuais e de duplas.

## 🚀 Funcionalidades

- **Rankings Dinâmicos**: Classificação de jogadores individuais e duplas
- **Filtros Avançados**: Por trimestre e número mínimo de partidas
- **Estatísticas Completas**: Pontos, vitórias, média e eficiência
- **Interface Administrativa**: Gerenciamento completo via Django Admin
- **Interface Web Moderna**: Templates responsivos e intuitivos

## 📊 Métricas Calculadas

### Ranking Individual
- **Partidas**: Número total de jogos
- **Pontos**: Soma de todos os pontos marcados
- **Vitórias**: Número de partidas vencidas
- **Média de Pontos**: Pontos totais ÷ número de partidas
- **Eficiência**: (Vitórias ÷ partidas) × 100

### Ranking de Duplas
- **Partidas**: Número total de jogos da dupla
- **Vitórias**: Número de partidas vencidas pela dupla
- **Eficiência**: (Vitórias ÷ partidas) × 100

## 🛠️ Instalação e Configuração

### Pré-requisitos
- Python 3.11+
- pip
- virtualenv (recomendado)

### Passos

1. **Clone o repositório**
   ```bash
   git clone <url-do-repositorio>
   cd petecou
   ```

2. **Crie e ative o ambiente virtual**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # No Windows: .venv\Scripts\activate
   ```

3. **Instale as dependências**
   ```bash
   pip install django
   ```

4. **Execute as migrações**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Crie um superusuário**
   ```bash
   python manage.py createsuperuser
   ```

6. **Inicie o servidor**
   ```bash
   python manage.py runserver
   ```

7. **Acesse a aplicação**
   - Interface web: http://localhost:8000
   - Admin: http://localhost:8000/admin

## 🎯 Como Usar

### 1. Cadastro de Dados (via Admin)
1. Acesse `/admin/` e faça login
2. Cadastre jogadores em "Jogadores"
3. Crie duplas em "Duplas" (selecione 2 jogadores)
4. Registre partidas em "Partidas"

### 2. Visualização de Rankings
- **Ranking Individual**: `/ranking/individual/`
- **Ranking de Duplas**: `/ranking/duplas/`

### 3. Filtros Disponíveis
- **Trimestre**: 1º, 2º, 3º ou 4º trimestre
- **Partidas Mínimas**: Número mínimo de jogos para aparecer no ranking

## 📁 Estrutura do Projeto

```
petecou/
├── jogos/                  # App principal
│   ├── models.py          # Modelos (Jogador, Dupla, Partida)
│   ├── views.py           # Views dos rankings
│   ├── admin.py           # Interface administrativa
│   ├── utils.py           # Funções de cálculo
│   ├── urls.py            # URLs do app
│   └── templates/         # Templates HTML
├── peteca_scout/          # Configuração do projeto
│   ├── settings.py        # Configurações Django
│   └── urls.py            # URLs principais
├── manage.py              # Script de gerenciamento Django
└── requirements.txt       # Dependências do projeto
```

## 🔧 Configuração para Desenvolvimento

### Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:
```env
DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui
```

### Executar Testes
```bash
python manage.py test
```

### Verificar Estilo de Código
```bash
flake8 jogos/
```

## 📈 Funcionalidades Futuras

- [ ] Gráficos de performance
- [ ] Histórico de partidas por jogador
- [ ] Exportação de relatórios
- [ ] API REST
- [ ] Autenticação de usuários
- [ ] Comentários e observações nas partidas

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🏆 Créditos

Desenvolvido para acompanhar e melhorar o desempenho dos jogadores de peteca, promovendo a competição saudável e o desenvolvimento do esporte.
