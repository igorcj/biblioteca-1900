-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2021-03-14 17:52:19.901

-- tables
-- Table: alunos
CREATE TABLE alunos (
    ID serial NOT NULL,
    nome varchar(50) NOT NULL,
    quarto int NOT NULL,
    telefone char(11) NULL,
    CONSTRAINT alunos_pk PRIMARY KEY (ID)
) COMMENT 'Tabela com as informações dos alunos';

-- Table: emprestimos
CREATE TABLE emprestimos (
    ID serial NOT NULL,
    data_emp date NOT NULL,
    data_dev date NULL,
    alunos_ID bigint UNSIGNED NOT NULL,
    livros_academico bool NOT NULL,
    livros_letra char(1) NOT NULL,
    livros_indice MEDIUMINT NOT NULL,
    CONSTRAINT emprestimos_pk PRIMARY KEY (ID)
) COMMENT 'Histórico de empréstimos';

-- Table: livros
CREATE TABLE livros (
    academico bool NOT NULL,
    letra char(1) NOT NULL,
    indice MEDIUMINT NOT NULL,
    titulo varchar(100) NOT NULL,
    autor varchar(50) NOT NULL,
    editora varchar(30) NOT NULL,
    ano int NULL,
    alunos_ID bigint UNSIGNED NOT NULL,
    CONSTRAINT livros_pk PRIMARY KEY (academico,letra,indice)
);

-- foreign keys
-- Reference: emprestimos_alunos (table: emprestimos)
ALTER TABLE emprestimos ADD CONSTRAINT emprestimos_alunos FOREIGN KEY emprestimos_alunos (alunos_ID)
    REFERENCES alunos (ID);

-- Reference: emprestimos_livros (table: emprestimos)
ALTER TABLE emprestimos ADD CONSTRAINT emprestimos_livros FOREIGN KEY emprestimos_livros (livros_academico,livros_letra,livros_indice)
    REFERENCES livros (academico,letra,indice);

-- Reference: livros_alunos (table: livros)
ALTER TABLE livros ADD CONSTRAINT livros_alunos FOREIGN KEY livros_alunos (alunos_ID)
    REFERENCES alunos (ID);

-- End of file.

