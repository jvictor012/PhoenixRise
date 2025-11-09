-- =====================================================
-- SCHEMA
-- =====================================================
CREATE SCHEMA IF NOT EXISTS phoenixrise;
USE phoenixrise;

-- =====================================================
-- TABELA: ESPORTES
-- =====================================================
CREATE TABLE esportes (
    id_esporte INT AUTO_INCREMENT PRIMARY KEY,
    nome_esporte VARCHAR(120) NOT NULL
);

INSERT INTO esportes (nome_esporte) VALUES
('Artes Marciais'),
('Basquete'),
('Corrida'),
('Futsal'),
('Futebol'),
('Ginástica'),
('Hidroginástica'),
('Handebol'),
('Natação');

-- =====================================================
-- TABELA: USUÁRIOS
-- =====================================================
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    nome_usuario VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(80) NOT NULL UNIQUE,
    senha_hash VARCHAR(300) NOT NULL,
    data_nascimento DATE,
    foto_url VARCHAR(255)
);

-- =====================================================
-- TABELA: USUARIO_ESPORTE (TABELA RELACIONAL)
-- =====================================================
CREATE TABLE usuario_esporte (
    id_usuario INT,
    id_esporte INT,
    PRIMARY KEY (id_usuario, id_esporte),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (id_esporte) REFERENCES esportes(id_esporte)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- =====================================================
-- TABELA: POSTS
-- =====================================================
CREATE TABLE posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descricao TEXT NOT NULL,
    url_image VARCHAR(255),
    data_publicacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_id INT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- =====================================================
-- TABELA: ACADEMIAS
-- =====================================================
CREATE TABLE academias (
    id_academia INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    mensalidade DECIMAL(10,2),
    descricao TEXT,
    latitude DOUBLE,
    longitude DOUBLE,
    cidade VARCHAR(100),
    rua VARCHAR(100),
    complemento VARCHAR(100),
    dias_funcionamento VARCHAR(100),
    contato_principal VARCHAR(100),
    imagem_url VARCHAR(255)
);

INSERT INTO academias 
(nome, mensalidade, descricao, latitude, longitude, cidade, rua, complemento, dias_funcionamento, contato_principal, imagem_url)
VALUES
("Academia Top Fitness", 90.00, "A Top Fitness proporciona um ambiente climatizado com máquinas bem preservadas.", -5.663812521428317, -37.80741868034249, "Apodi", "R. Moésio Holanda", "Esquina", "Seg-Sex(5h-20h) Sab-Dom(7h-14h)", "topfitnessapodi", "https://www.akademias.com.br/imgempresas/academia-top-fitness-19767-VSJk.jpg"),
("Foco Academia", 80.00, "A Foco Academia é ideal para quem busca resultados rápidos, com treinos personalizados e acompanhamento profissional.", -5.658043198588798, -37.79612277145106, "Apodi", "Av. Marechal Floriano Peixoto", "Próximo à panificadora Requinte da Massa", "Seg-Sex(6h-22h) Sab-Dom(15h-19h)", "focoacademiaapodi", "https://lh3.googleusercontent.com/p/AF1QipNo7DyX8A5WRRuw3aFoR394ca74GbutfW8ZOYOW=s1360-w1360-h1020-rw"),
("Academia Prime Core", 85.00, "A Prime Core oferece treinos funcionais e musculação de alta performance em ambiente moderno.", -5.650346879472210, -37.79995285916965, "Apodi", "R. Joaquim de Moura", "Ao lado da Facis", "Seg-Sex(3:50h-21h) Sab-Dom(15h-19h)", "primecoreofc", "https://res.cloudinary.com/drdezhuko/image/upload/v1762632472/rv0jxpvzfxy0arv33vb9.png"),
("Soufit", 80.00, "A Soufit combina tecnologia e conforto para tornar os treinos mais eficientes e agradáveis.", -5.648767002876063, -37.79925649914765, "Apodi", "R. Manoel Nogueira", "Próximo a Oficina Nunes", "Seg-Sex(5h-22h) Sab-Dom(7h-18h)", "soufit_apodi", "https://res.cloudinary.com/drdezhuko/image/upload/v1762632793/l1vgb9hw22hrhamyqxng.png"),
("Academia Performance", 85.00, "A Academia Performance é ideal para quem busca força e resistência com acompanhamento profissional.", -5.665555680785641, -37.79491094724948, "Apodi", "Av. Moésio Holanda", "Em frente à Escola Estadual", "Seg-Sex(5h-21h) Sab(6h-12h)", "performanceapodi", "https://res.cloudinary.com/drdezhuko/image/upload/v1762632793/l1vgb9hw22hrhamyqxng.png");

-- =====================================================
-- TABELA: ACADEMIAS LIVRES
-- =====================================================
CREATE TABLE academias_livres (
    id_academia_livre INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    latitude DOUBLE,
    longitude DOUBLE,
    cidade VARCHAR(100),
    rua VARCHAR(100),
    complemento VARCHAR(100),
    imagem_url VARCHAR(255)
);

INSERT INTO academias_livres (nome, latitude, longitude, cidade, rua, complemento, imagem_url) VALUES
('Academia do Calçadão', -5.669354646518213, -37.79919838643754, 'Apodi', 'Raimundo Cristino da Silva', 'Próximo ao Kurrupius', 'https://res.cloudinary.com/drdezhuko/image/upload/v1762645293/ujm1u3wmdsj01uxnyops.png'),
('Academia Antonio Dantas', -5.652562205176904, -37.799625568567876, 'Apodi', 'R. Joaquim de Moura', 'Próximo ao Antonio Dantas', 'https://res.cloudinary.com/drdezhuko/image/upload/v1762645727/o7v7poqu4foccqjtzf75.png'),
('Academia do IPE', -5.644143616635816, -37.7997507246134, 'Apodi', 'R. Joaquim Teixeira de Moura', 'Próximo ao Célio Auto Mecânica', 'https://res.cloudinary.com/drdezhuko/image/upload/v1762646141/ezx3kxwx92mxxrxbhzfy.png'),
('Academia do Bacural 1', -5.662501638500952, -37.812093091792796, 'Apodi', 'R. Luís Nogueira de Oliveira', 'Próximo a Panificadora Cristal', 'https://res.cloudinary.com/drdezhuko/image/upload/v1762646438/hczqbql5vejpuvjgqzfy.png');

-- =====================================================
-- TABELA: QUADRAS
-- =====================================================
CREATE TABLE quadras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    latitude DOUBLE,
    longitude DOUBLE,
    cidade VARCHAR(100),
    rua VARCHAR(100),
    complemento VARCHAR(100),
    dias_funcionamento VARCHAR(100),
    imagem_url VARCHAR(255)
);

INSERT INTO quadras (nome, latitude, longitude, cidade, rua, complemento, dias_funcionamento, imagem_url) VALUES
("Quadra Poliesportiva", -5.632274690348239, -37.80171350910772, "Apodi", "BR-405", "Na descida da chapada do Apodi", "Não informado", 'https://i.pinimg.com/736x/51/9e/86/519e865861584737324da96fadaa621a.jpg'),
("Quadra COHAB", -5.657647986318352, -37.801125375869645, "Apodi", "R. Araçá", "Próximo ao Consultório Rebeca Silveira", "Não informado", 'https://res.cloudinary.com/drdezhuko/image/upload/v1762638383/dkl91e5v2wt2onxqekmy.png'),
("Quadra IFRN Apodi", -5.62718845440121, -37.80725109801273, "Apodi", "Chapada do Apodi RN-233", "Ao lado do Cactus Restaurante", "Seg-Sex(7h-22:10h)", 'https://res.cloudinary.com/drdezhuko/image/upload/v1762639111/ykp174rqqj1iu3xzmre4.png');

-- =====================================================
-- TABELA: LOJAS
-- =====================================================
CREATE TABLE lojas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    latitude DOUBLE,
    longitude DOUBLE,
    cidade VARCHAR(100),
    rua VARCHAR(100),
    complemento VARCHAR(100),
    dias_funcionamento VARCHAR(100),
    contato_principal VARCHAR(100),
    imagem_url VARCHAR(255)
);

INSERT INTO lojas (nome, latitude, longitude, cidade, rua, complemento, dias_funcionamento, contato_principal, imagem_url)
VALUES
('Fit Closet Apodi', -5.664434892555351, -37.79916604047842, 'Apodi', 'R. Nossa Senhora de Conceição', 'Ao lado do banco Bradesco', 'Seg-Sex(8h-17h30) Sab(8h-12h)', 'fit.closetapodi', 'https://res.cloudinary.com/drdezhuko/image/upload/v1762635146/zrz3kxllzsq7n5btnau5.png'),
('Sport Center', -5.6638995267040935, -37.798567762811786, 'Apodi', 'R. São João Batista', 'Ao lado da farmácia Menor Preço', 'Seg-Sex(7h-18h) Sab(7h-13h)', '08433332879', 'https://res.cloudinary.com/drdezhuko/image/upload/v1762635291/tievwun0g4qgcclipyck.png'),
('Meu Suplemento', -5.665122, -37.799332, 'Apodi', 'R. Gov. Dix-Sept Rosado', 'Ao lado do Açaí da Praça', 'Seg-Sex(8h-18h) Sab(8h-12h)', 'meu.suplemento', 'https://res.cloudinary.com/drdezhuko/image/upload/v1762635410/jjrwfev6micvftkjejlp.png'),
('Prosup', -5.653765, -37.799501, 'Apodi', 'R. Joaquim Moura', 'Próximo ao Hot Dog do Pedro', 'Seg-Sex(8h-19h) Sab(8h-11h)', '084999309173', 'https://res.cloudinary.com/drdezhuko/image/upload/v1762635499/rspmny4hda380g07btpz.png');

-- =====================================================
-- TABELA: PRODUTOS
-- =====================================================
CREATE TABLE produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    loja_id INT,
    nome_produto VARCHAR(100) NOT NULL,
    descricao_produto TEXT,
    preco DECIMAL(10,2) NOT NULL,
    categoria VARCHAR(100),
    imagem_url VARCHAR(255),
    FOREIGN KEY (loja_id) REFERENCES lojas(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

INSERT INTO produtos (loja_id, nome_produto, descricao_produto, preco, categoria, imagem_url)
VALUES
(3, "T_SEK", "Ideal para preparar e consumir suplementos líquidos durante o treino.", 84.90, "Suplementos", "https://res.cloudinary.com/drdezhuko/image/upload/v1762642057/qdtk6q5qovsnwuur7dhm.png"),
(1, "Short FILA FLOW", "Tecido leve e respirável, ideal para treinos de musculação e corrida.", 39.90, "Vestuário", "https://res.cloudinary.com/drdezhuko/image/upload/v1762639661/d5gmo5xqjwq2mxcthpoe.png"),
(1, "Short esportivo Bs Cross", "Conforto, mobilidade e resistência para qualquer desafio.", 39.90, "Vestuário", "https://res.cloudinary.com/drdezhuko/image/upload/v1762639843/r3v0n4itqj4kc8jbihnl.png"),
(2, "Tenis de Corrida Azul", "Aumenta força, resistência e performance durante os treinos intensos.", 104.90, "Vestuário", "https://res.cloudinary.com/drdezhuko/image/upload/v1762640545/idhpynltzqm6r6cmhg3t.png"),
(3, "INSANE", "Ideal para preparar e consumir suplementos líquidos durante o treino.", 74.90, "Suplementos", "https://res.cloudinary.com/drdezhuko/image/upload/v1762640774/xndmclnpojze25ltvgy7.png"),
(4, "Kit Max Titanium Creatina 500g", "Perfeito para treinos e força.", 150.00, "Suplementos", "https://static.wixstatic.com/media/781ba9_dde53de4d72d4c41a0d51ac5a7e752ec~mv2.webp"),
(4, "Whey Grego 3W 900g", "Sabor iogurte natural, 3 tipos de proteína.", 199.90, "Suplementos", "https://static.wixstatic.com/media/781ba9_db3686b7467048fb9ab8b73cf2360677~mv2.png");
