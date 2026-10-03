# EAD Católica

O **EAD Católica** é um projeto acadêmico desenvolvido para a disciplina de **Desenvolvimento Back-end**, ministrada pelo professor Renê Gadelha, com o objetivo de criar uma plataforma de Educação a Distância (EAD) para a faculdade, de maneira prototipada.

## Tecnologias utilizadas

- **Flask** — framework utilizado no desenvolvimento do back-end da aplicação.
- **Jinja2** — utilizado para a renderização das páginas e integração entre o back-end e o front-end.
- **SQLAlchemy** — utilizado para a modelagem e comunicação com o banco de dados.
- **HTML, CSS e JavaScript** — utilizados na construção da interface da aplicação.

## Armazenamento de arquivos

O projeto possui um sistema de armazenamento local para arquivos estáticos, como imagens e outros recursos utilizados pela aplicação.

Esses arquivos são armazenados em uma pasta chamada `bucket`, localizada na raiz do projeto:

EAD-Catolica/
├── bucket/
│   ├── imagem/
│   ├── video/
│   └── ...
├── app/
├── templates/
└── ...

A pasta `bucket` funciona como o armazenamento dos arquivos utilizados pela plataforma, mantendo esses recursos separados da estrutura principal da aplicação.

> Este projeto possui finalidade acadêmica e foi desenvolvido como parte das atividades da disciplina de **Desenvolvimento Back-end**.