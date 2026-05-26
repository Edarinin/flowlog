import json
import os
import PySimpleGUI as sg

# =========================
# CONFIGURAÇÃO VISUAL
# =========================
# Tema global do PySimpleGUI para manter cores coerentes em toda a UI.
sg.theme("DarkBlue14")

# Caminhos absolutos da pasta do projeto para localizar assets.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Imagens usadas nas telas (logo e banner no dashboard).
LOGO_PATH = os.path.join(BASE_DIR, "logo.png")
BANNER_PATH = os.path.join(BASE_DIR, "banner.png")

# Arquivo local para persistir cadastros (somente local, sem banco).
DATA_PATH = os.path.join(BASE_DIR, "flowlog_data.json")


# Helper para renderizar uma imagem somente se o arquivo existir.
def image_if_exists(path, size=None):
    if os.path.exists(path):
        return sg.Image(filename=path, size=size)
    return sg.Text("")


# =========================
# TELA DE LOGIN
# =========================
# Monta e retorna a janela de login com branding e formulario.
def login_window():
    # Layout dividido em 2 colunas: branding e formulario de acesso.
    layout = [
        [
            # Coluna Esquerda (Branding)
            sg.Column(
                [
                    [sg.VPush()],
                    [sg.Text("FLOW LOG", font=("Arial", 40, "bold"), text_color="white")],
                    [sg.Text("Sistema de gestão e estoque", font=("Arial", 14), text_color="#B0B8C1")],
                    [sg.VPush()],
                    [image_if_exists(LOGO_PATH, size=(250, 250))],
                    [sg.VPush()],
                ],
                expand_x=True,
                expand_y=True,
                element_justification="center",
                background_color="#111827"
            ),
            
            sg.VerticalSeparator(color="#2A3546"),
            
            # Coluna Direita (Formulário)
            sg.Column(
                [
                    [sg.VPush()],
                    [sg.Text("Acesse o sistema", font=("Arial", 24, "bold"), text_color="white")],
                    [sg.Text("Usuário", font=("Arial", 12), text_color="#E5E7EB")],
                    [sg.Input(key="-USER-", size=(35, 1), border_width=0, background_color="#1E2633", text_color="white", font=("Arial", 12))],
                    [sg.Text("Senha", font=("Arial", 12), text_color="#E5E7EB")],
                    [sg.Input(password_char="*", key="-PASS-", size=(35, 1), border_width=0, background_color="#1E2633", text_color="white", font=("Arial", 12))],
                    [sg.Text("", key="-MSG-", size=(35, 1), text_color="#FF8A8A")],
                    
                    [
                        sg.Button("Entrar", key="-ENTER-", size=(15, 1), button_color=("white", "#2D6CDF"), border_width=0, font=("Arial", 12, "bold"), bind_return_key=True),
                        sg.Button("Sair", key="-EXIT-", size=(15, 1), button_color=("white", "#3A4656"), border_width=0, font=("Arial", 12))
                    ],
                    
                    [sg.Text("Login de teste: admin / 123", font=("Arial", 10), text_color="#9AA7B3")],
                    [sg.VPush()],
                ],
                expand_x=True,
                expand_y=True,
                element_justification="left",
                pad=(50, 0),
                background_color="#111827"
            ),
        ]
    ]

    # Criamos a janela com finalize=True para poder maximizar logo em seguida
    window = sg.Window(
        "Login - Flow Log",
        layout,
        size=(1366, 720),
        finalize=True,
        resizable=True, # Permitir redimensionamento ajuda o maximize() a funcionar melhor
        background_color="#111827",
        margins=(0, 0),
        no_titlebar=False # Se quiser esconder a barra superior, mude para True
    )

    # Este é o comando que faz a mágica da tela cheia
    window.maximize()
    
    return window


# --- LÓGICA DE PRODUTOS ---
def atualizar_produto(sku, nome, categoria, estoque):
    # Aqui usamos o SKU como chave única
    for p in products: # Certifique-se que a lista de produtos se chama 'products' globalmente
        if p[0] == sku:
            p[1], p[2], p[3] = nome, categoria, estoque
            save_local_data()
            return True
    return False

def remover_produto(sku):
    global products
    products = [p for p in products if p[0] != sku]
    save_local_data()

# --- LÓGICA DE USUÁRIOS ---
def atualizar_usuario(codigo, nome, perfil):
    for u in users_data:
        if u["codigo"] == codigo:
            u["nome"], u["perfil"] = nome, perfil
            save_local_data()
            return True
    return False

def remover_usuario(codigo):
    global users_data
    users_data = [u for u in users_data if u["codigo"] != codigo]
    save_local_data()


# =========================
# COMPONENTES DO DASHBOARD
# =========================
# Dados (carregados do JSON local quando existir).
agenda = []
clients_data = []
suppliers_data = []
users_data = []


def default_data():
    return {
        "agenda": [
            {"nome": "Bruno", "celular": "1199999999999"},
            {"nome": "Daniela", "celular": "1199999999998"},
            {"nome": "Maria", "celular": "1199999999997"},
            {"nome": "Joao", "celular": "1199999999996"},
        ],
        "clients": [
            {"codigo": "CL-104", "cliente": "Loja Central", "status": "Ativo"},
            {"codigo": "CL-117", "cliente": "TechVille", "status": "Ativo"},
            {"codigo": "CL-128", "cliente": "Digital House", "status": "Ativo"},
            {"codigo": "CL-132", "cliente": "Mercado Sul", "status": "Inativo"},
        ],
        "suppliers": [
            {"codigo": "FO-21", "fornecedor": "Mega Distribuidora", "prazo": "Entregas semanais"},
            {"codigo": "FO-28", "fornecedor": "Alpha Tech", "prazo": "Ate 48h"},
            {"codigo": "FO-35", "fornecedor": "Prime Components", "prazo": "Ate 72h"},
        ],
        "users": [
            {"codigo": "USR-01", "nome": "Renata Lima", "perfil": "Admin"},
            {"codigo": "USR-02", "nome": "Joao Prado", "perfil": "Operador"},
            {"codigo": "USR-03", "nome": "Larissa Melo", "perfil": "Compras"},
        ],
    }


def load_local_data():
    global agenda, clients_data, suppliers_data, users_data

    data = default_data()
    if os.path.exists(DATA_PATH):
        try:
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            if isinstance(loaded, dict):
                data["agenda"] = loaded.get("agenda", data["agenda"])
                data["clients"] = loaded.get("clients", data["clients"])
                data["suppliers"] = loaded.get("suppliers", data["suppliers"])
                data["users"] = loaded.get("users", data["users"])
        except (OSError, json.JSONDecodeError):
            data = default_data()

    agenda = list(data["agenda"])
    clients_data = list(data["clients"])
    suppliers_data = list(data["suppliers"])
    users_data = list(data["users"])


def save_local_data():
    data = {
        "agenda": agenda,
        "clients": clients_data,
        "suppliers": suppliers_data,
        "users": users_data,
    }
    try:
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


def next_code(prefix, items, code_key="codigo"):
    max_num = 0
    for item in items:
        code = str(item.get(code_key, ""))
        if code.startswith(prefix):
            suffix = code[len(prefix) :]
            try:
                max_num = max(max_num, int(suffix))
            except ValueError:
                continue
    return f"{prefix}{max_num + 1:02d}" if prefix == "USR-" else f"{prefix}{max_num + 1}"


def clients_rows():
    return [[c.get("codigo", ""), c.get("cliente", ""), c.get("status", "")] for c in clients_data]


def suppliers_rows():
    return [[s.get("codigo", ""), s.get("fornecedor", ""), s.get("prazo", "")] for s in suppliers_data]


def users_rows():
    return [[u.get("codigo", ""), u.get("nome", ""), u.get("perfil", "")] for u in users_data]


def criar_amigo(nome, celular):
    agenda.append({"nome": nome, "celular": celular})
    save_local_data()


def consultar_amigo(nome):
    for item in agenda:
        if item["nome"].lower() == nome.lower():
            return item
    return None


def atualizar_amigo(nome, celular):
    global agenda
    for item in agenda:
        if item["nome"].lower() == nome.lower():
            item["celular"] = celular
            save_local_data()
            return True
    return False

def remover_amigo(nome):
    global agenda
    for idx, item in enumerate(agenda):
        if item["nome"].lower() == nome.lower():
            del agenda[idx]
            save_local_data()
            return True
    return False

def agenda_rows():
    return [[item["nome"], item["celular"]] for item in agenda]


# Card padrao para KPIs com titulo, valor principal e legenda.
def card(title, value, subtitle):
    return sg.Frame(
        "",
        [
            [sg.Text(title, font=("Arial", 10), text_color="#AAB4C3")],
            [sg.Text(value, font=("Arial", 22, "bold"), text_color="white")],
            [sg.Text(subtitle, font=("Arial", 9), text_color="#7F8A99")],
        ],
        relief=sg.RELIEF_FLAT,
        border_width=0,
        background_color="#18212E",
        pad=(12, 12),
        expand_x=True,
    )


# Botao do menu lateral com cores e hover padronizados.
def sidebar_button(text, key):
    return sg.Button(
        text,
        key=key,
        size=(20, 1),
        button_color=("white", "#1E2633"),
        border_width=0,
        pad=(0, 6),
        mouseover_colors=("white", "#2D6CDF"),
    )


# =========================
# TELAS INTERNAS
# =========================
# Tela inicial do dashboard com KPIs, banner, atividades e acoes rapidas.
def home_page():
    # Dados de exemplo para a tabela de atividades recentes.
    activities = [
        ["08:10", "Entrada", "Monitor 27\"", "+6"],
        ["09:05", "Saida", "Teclado mecanico", "-2"],
        ["10:20", "Entrada", "Mouse ergonomico", "+8"],
        ["11:40", "Saida", "Headset Pro", "-1"],
    ]

    return sg.Column(
        [
            # Cabecalho e subtitulo do dashboard.
            [
                sg.Text("Dashboard", font=("Arial", 24, "bold"), text_color="white"),
                sg.Push(),
                sg.Text("Painel do projeto", font=("Arial", 10), text_color="#AAB4C3"),
            ],
            [sg.HorizontalSeparator(color="#2A3546")],
            # KPIs do topo.
            [
                card("Produtos", "128", "Itens cadastrados"),
                card("Baixo estoque", "12", "Precisam reposicao"),
                card("Entradas hoje", "18", "Movimentacoes recentes"),
            ],
            [
                # Banner visual com imagem opcional.
                sg.Frame(
                    "",
                    [
                        [sg.Text("Visao geral", font=("Arial", 14, "bold"), text_color="white")],
                        [sg.Text("", text_color="#B8C2CE")],
                        [sg.Push()],
                        [image_if_exists(BANNER_PATH)],
                    ],
                    background_color="#18212E",
                    border_width=0,
                    relief=sg.RELIEF_FLAT,
                    expand_x=True,
                    expand_y=True,
                    pad=(0, 12),
                )
            ],
            [
                # Tabela de atividades recentes.
                sg.Frame(
                    "",
                    [
                        [sg.Text("Atividades recentes", font=("Arial", 14, "bold"), text_color="white")],
                        [
                            sg.Table(
                                values=activities,
                                headings=["Hora", "Tipo", "Item", "Qtd"],
                                auto_size_columns=True,
                                num_rows=4,
                                background_color="#0F172A",
                                text_color="#E5E7EB",
                                header_background_color="#1F2937",
                                header_text_color="#E5E7EB",
                                row_height=26,
                                justification="left",
                                border_width=0,
                            )
                        ],
                    ],
                    background_color="#18212E",
                    border_width=0,
                    relief=sg.RELIEF_FLAT,
                    expand_x=True,
                    pad=(0, 12),
                )
            ],
            [
                # Acoes rapidas do dashboard.
                sg.Frame(
                    "",
                    [
                        [sg.Text("Acoes rapidas", font=("Arial", 14, "bold"), text_color="white")],
                        [
                            sg.Button("Novo produto", button_color=("white", "#2D6CDF"), border_width=0, size=(15, 1)),
                            sg.Button("Novo fornecedor", button_color=("white", "#3A4656"), border_width=0, size=(18, 1)),
                            sg.Button("Relatorios", button_color=("white", "#3A4656"), border_width=0, size=(12, 1)),
                        ],
                    ],
                    background_color="#18212E",
                    border_width=0,
                    relief=sg.RELIEF_FLAT,
                    expand_x=True,
                    pad=(0, 0),
                )
            ],
        ],
        background_color="#111827",
        expand_x=True,
        expand_y=True,
        key="-PAGE-HOME-",
        visible=True,
    )


def products_page():
    # Dados de exemplo para tabelas da tela de produtos.
    products = [
        ["P-103", "Monitor 27\"", "Eletronicos", "34"],
        ["P-118", "Teclado mecanico", "Perifericos", "58"],
        ["P-121", "Mouse ergonomico", "Perifericos", "22"],
        ["P-142", "Headset Pro", "Audio", "9"],
        ["P-177", "Dock USB-C", "Acessorios", "15"],
    ]
    low_stock = [
        ["P-142", "Headset Pro", "9", "Min. 15"],
        ["P-177", "Dock USB-C", "15", "Min. 25"],
        ["P-199", "Cabo HDMI", "12", "Min. 30"],
    ]
    categories = [
        ["Eletronicos", "42"],
        ["Perifericos", "31"],
        ["Audio", "14"],
        ["Acessorios", "9"],
    ]

    return sg.Column(
        [
            # Titulo e subtitulo da pagina.
            [sg.Text("Produtos", font=("Arial", 24, "bold"), text_color="white")],
            [sg.Text("Resumo de estoque e cadastro", font=("Arial", 10), text_color="#AAB4C3")],
            [sg.HorizontalSeparator(color="#2A3546")],
            # KPIs de produtos.
            [
                card("Ativos", "96", "Produtos em uso"),
                card("Inativos", "32", "Fora de linha"),
                card("Fornecedores", "14", "Parceiros"),
            ],
            [
                # Tabela principal de produtos.
                sg.Frame(
                    "",
                    [
                        [sg.Text("Produtos cadastrados", font=("Arial", 14, "bold"), text_color="white")],
                        [
                            sg.Table(
                                values=products,
                                headings=["SKU", "Produto", "Categoria", "Estoque"],
                                auto_size_columns=True,
                                num_rows=6,
                                background_color="#0F172A",
                                text_color="#E5E7EB",
                                header_background_color="#1F2937",
                                header_text_color="#E5E7EB",
                                row_height=26,
                                justification="left",
                                border_width=0,
                                size=(48, 8),
                            )
                        ],
                    ],
                    background_color="#18212E",
                    border_width=0,
                    relief=sg.RELIEF_FLAT,
                    expand_x=True,
                    pad=(0, 12),
                )
            ],
            [
                # Bloco duplo: estoque critico e categorias.
                sg.Frame(
                    "",
                    [
                        [sg.Text("Estoque critico", font=("Arial", 14, "bold"), text_color="white")],
                        [
                            sg.Table(
                                values=low_stock,
                                headings=["SKU", "Produto", "Atual", "Meta"],
                                auto_size_columns=True,
                                num_rows=4,
                                background_color="#0F172A",
                                text_color="#E5E7EB",
                                header_background_color="#1F2937",
                                header_text_color="#E5E7EB",
                                row_height=26,
                                justification="left",
                                border_width=0,
                                size=(44, 5),
                            )
                        ],
                    ],
                    background_color="#18212E",
                    border_width=0,
                    relief=sg.RELIEF_FLAT,
                    expand_x=True,
                    pad=(0, 12),
                ),
                sg.Frame(
                    "",
                    [
                        [sg.Text("Categorias", font=("Arial", 14, "bold"), text_color="white")],
                        [
                            sg.Table(
                                values=categories,
                                headings=["Categoria", "Itens"],
                                auto_size_columns=True,
                                num_rows=4,
                                background_color="#0F172A",
                                text_color="#E5E7EB",
                                header_background_color="#1F2937",
                                header_text_color="#E5E7EB",
                                row_height=26,
                                justification="left",
                                border_width=0,
                                size=(24, 5),
                            )
                        ],
                    ],
                    background_color="#18212E",
                    border_width=0,
                    relief=sg.RELIEF_FLAT,
                    expand_x=True,
                    pad=(0, 12),
                ),
            ],
            [
                # Acoes relacionadas a produtos.
                sg.Frame(
                    "",
                    [
                        [sg.Text("Acoes", font=("Arial", 14, "bold"), text_color="white")],
                        [
                         [
                            sg.Button("Adicionar", key="-PROD-ADD-", button_color=("white", "#2D6CDF"), size=(12, 1)),
                            sg.Button("Atualizar", key="-PROD-UPDATE-", button_color=("white", "#3A4656"), size=(12, 1)),
                            sg.Button("Excluir", key="-PROD-DELETE-", button_color=("white", "#E53E3E"), size=(12, 1)),
                        ]
                        ],
                    ],
                    background_color="#18212E",
                    border_width=0,
                    relief=sg.RELIEF_FLAT,
                    expand_x=True,
                    pad=(0, 0),
                )
            ],
        ],
        background_color="#111827",
        expand_x=True,
        expand_y=True,
        key="-PAGE-PRODUTO-",
        visible=False,
    )


def reports_page():
    # Dados de exemplo para os relatorios.
    monthly = [
        ["Jan", "R$ 28.120", "212", "17%"],
        ["Fev", "R$ 31.780", "236", "18%"],
        ["Mar", "R$ 33.540", "244", "19%"],
        ["Abr", "R$ 32.450", "248", "18%"],
    ]
    highlights = [
        ["Campanha Q1", "R$ 9.420", "+12%"],
        ["Canal online", "R$ 14.880", "+18%"],
        ["Vendas B2B", "R$ 7.350", "+9%"],
    ]

    return sg.Column(
        [
            # Titulo e subtitulo da pagina.
            [sg.Text("Relatorios", font=("Arial", 24, "bold"), text_color="white")],
            [sg.Text("Visao de desempenho e indicadores", font=("Arial", 10), text_color="#AAB4C3")],
            [sg.HorizontalSeparator(color="#2A3546")],
            # KPIs da area de relatorios.
            [
                card("Vendas", "R$ 32.450", "Mes atual"),
                card("Pedidos", "248", "Mes atual"),
                card("Margem", "18%", "Media"),
            ],
            [
                # Tabela com resumo mensal.
                sg.Frame(
                    "",
                    [
                        [sg.Text("Resumo mensal", font=("Arial", 14, "bold"), text_color="white")],
                        [
                            sg.Table(
                                values=monthly,
                                headings=["Mes", "Vendas", "Pedidos", "Margem"],
                                auto_size_columns=True,
                                num_rows=5,
                                background_color="#0F172A",
                                text_color="#E5E7EB",
                                header_background_color="#1F2937",
                                header_text_color="#E5E7EB",
                                row_height=26,
                                justification="left",
                                border_width=0,
                                size=(44, 6),
                            )
                        ],
                    ],
                    background_color="#18212E",
                    border_width=0,
                    relief=sg.RELIEF_FLAT,
                    expand_x=True,
                    pad=(0, 12),
                )
            ],
            [
                # Destaques por origem ou canal.
                sg.Frame(
                    "",
                    [
                        [sg.Text("Destaques", font=("Arial", 14, "bold"), text_color="white")],
                        [
                            sg.Table(
                                values=highlights,
                                headings=["Origem", "Receita", "Crescimento"],
                                auto_size_columns=True,
                                num_rows=4,
                                background_color="#0F172A",
                                text_color="#E5E7EB",
                                header_background_color="#1F2937",
                                header_text_color="#E5E7EB",
                                row_height=26,
                                justification="left",
                                border_width=0,
                                size=(36, 5),
                            )
                        ],
                    ],
                    background_color="#18212E",
                    border_width=0,
                    relief=sg.RELIEF_FLAT,
                    expand_x=True,
                    pad=(0, 12),
                )
            ],
            [
                # Botoes de exportacao.
                sg.Frame(
                    "",
                    [
                        [sg.Text("Exportar", font=("Arial", 14, "bold"), text_color="white")],
                        [
                            sg.Button("PDF", button_color=("white", "#2D6CDF"), border_width=0, size=(10, 1)),
                            sg.Button("Excel", button_color=("white", "#3A4656"), border_width=0, size=(10, 1)),
                        ],
                    ],
                    background_color="#18212E",
                    border_width=0,
                    relief=sg.RELIEF_FLAT,
                    expand_x=True,
                    pad=(0, 0),
                )
            ],
        ],
        background_color="#111827",
        expand_x=True,
        expand_y=True,
        key="-PAGE-RELATO-",
        visible=False,
    )


def registrations_page():
    return sg.Column(
        [
            # Titulo e subtitulo da pagina.
            [sg.Text("Cadastros", font=("Arial", 24, "bold"), text_color="white")],
            [sg.Text("Gerencie clientes, fornecedores e usuarios", font=("Arial", 10), text_color="#AAB4C3")],
            [sg.HorizontalSeparator(color="#2A3546")],
            [
                # Acoes rapidas para adicionar cadastros.
                sg.Frame(
                    "",
                    [
                        [sg.Text("Acoes de cadastro", font=("Arial", 14, "bold"), text_color="white")],
                        [
                            sg.Button("Adicionar cliente", key="-ADD-CLIENT-", button_color=("white", "#2D6CDF"), border_width=0, size=(18, 1)),
                            sg.Button("Adicionar fornecedor", key="-ADD-SUPPLIER-", button_color=("white", "#3A4656"), border_width=0, size=(20, 1)),
                            sg.Button("Adicionar usuario", key="-ADD-USER-", button_color=("white", "#3A4656"), border_width=0, size=(18, 1)),
                        ],
                    ],
                    background_color="#18212E",
                    border_width=0,
                    relief=sg.RELIEF_FLAT,
                    expand_x=True,
                    pad=(0, 12),
                )
            ],
            # KPIs da area de cadastros.
            [
                card("Clientes", "420", "Ativos"),
                card("Fornecedores", "18", "Ativos"),
                card("Usuarios", "7", "Com acesso"),
            ],
            [
                # Tabela de clientes.
                sg.Frame(
                    "",
                    [
                        [sg.Text("Clientes", font=("Arial", 14, "bold"), text_color="white")],
                        [
                            sg.Table(
                                values=clients_rows(),
                                headings=["Codigo", "Cliente", "Status"],
                                auto_size_columns=True,
                                num_rows=4,
                                background_color="#0F172A",
                                text_color="#E5E7EB",
                                header_background_color="#1F2937",
                                header_text_color="#E5E7EB",
                                row_height=26,
                                justification="left",
                                border_width=0,
                                size=(40, 5),
                                key="-CLIENTS-TABLE-",
                            )
                        ],
                    ],
                    background_color="#18212E",
                    border_width=0,
                    relief=sg.RELIEF_FLAT,
                    expand_x=True,
                    pad=(0, 12),
                )
            ],
            [
                # Tabela de fornecedores e acoes.
                sg.Frame(
                    "",
                    [
                        [sg.Text("Fornecedores", font=("Arial", 14, "bold"), text_color="white")],
                        [
                            sg.Table(
                                values=suppliers_rows(),
                                headings=["Codigo", "Fornecedor", "Prazo"],
                                auto_size_columns=True,
                                num_rows=3,
                                background_color="#0F172A",
                                text_color="#E5E7EB",
                                header_background_color="#1F2937",
                                header_text_color="#E5E7EB",
                                row_height=26,
                                justification="left",
                                border_width=0,
                                size=(40, 4),
                                key="-SUPPLIERS-TABLE-",
                            )
                        ],
                        [
                            sg.Button("Novo cliente", key="-ADD-CLIENT-", button_color=("white", "#2D6CDF"), border_width=0, size=(14, 1)),
                            sg.Button("Novo fornecedor", key="-ADD-SUPPLIER-", button_color=("white", "#3A4656"), border_width=0, size=(16, 1)),
                            sg.Button("Novo usuario", key="-ADD-USER-", button_color=("white", "#3A4656"), border_width=0, size=(14, 1)),
                        ],
                    ],
                    background_color="#18212E",
                    border_width=0,
                    relief=sg.RELIEF_FLAT,
                    expand_x=True,
                    pad=(0, 12),
                )
            ],
            [
                # Tabela de usuarios e acoes de acesso.
                sg.Frame(
                    "",
                    [
                        [sg.Text("Usuarios", font=("Arial", 14, "bold"), text_color="white")],
                        [
                            sg.Table(
                                values=users_rows(),
                                headings=["Codigo", "Nome", "Perfil"],
                                auto_size_columns=True,
                                num_rows=3,
                                background_color="#0F172A",
                                text_color="#E5E7EB",
                                header_background_color="#1F2937",
                                header_text_color="#E5E7EB",
                                row_height=26,
                                justification="left",
                                border_width=0,
                                size=(40, 4),
                                key="-USERS-TABLE-",
                            )
                        ],
                        [
                            sg.Button("Convidar", key="-ADD-USER-", button_color=("white", "#2D6CDF"), border_width=0, size=(12, 1)),
                            sg.Button("Permissoes", button_color=("white", "#3A4656"), border_width=0, size=(12, 1)),
                        ],
                    ],
                    background_color="#18212E",
                    border_width=0,
                    relief=sg.RELIEF_FLAT,
                    expand_x=True,
                    pad=(0, 12),
                )
            ],
            [
                # CRUD da agenda de amigos.
                sg.Frame(
                    "",
                    [
                        [sg.Text("Agenda de amigos", font=("Arial", 14, "bold"), text_color="white")],
                        [
                            sg.Text("Nome", size=(6, 1)),
                            sg.Input(key="-AGENDA-NOME-", size=(18, 1), background_color="#0F172A"),
                            sg.Text("Celular", size=(7, 1)),
                            sg.Input(key="-AGENDA-CELULAR-", size=(18, 1), background_color="#0F172A"),
                        ],
                        [
                            sg.Button("Adicionar", key="-AGENDA-ADD-", button_color=("white", "#2D6CDF"), border_width=0, size=(11, 1)),
                            sg.Button("Pesquisar", key="-AGENDA-SEARCH-", button_color=("white", "#3A4656"), border_width=0, size=(11, 1)),
                            sg.Button("Atualizar", key="-AGENDA-UPDATE-", button_color=("white", "#3A4656"), border_width=0, size=(11, 1)),
                            sg.Button("Remover", key="-AGENDA-DELETE-", button_color=("white", "#3A4656"), border_width=0, size=(11, 1)),
                        ],
                        [
                            sg.Table(
                                values=agenda_rows(),
                                headings=["Nome", "Celular"],
                                auto_size_columns=True,
                                num_rows=5,
                                background_color="#0F172A",
                                text_color="#E5E7EB",
                                header_background_color="#1F2937",
                                header_text_color="#E5E7EB",
                                row_height=26,
                                justification="left",
                                border_width=0,
                                size=(44, 6),
                                key="-AGENDA-TABLE-",
                                enable_events=True,
                            )
                        ],
                    ],
                    background_color="#18212E",
                    border_width=0,
                    relief=sg.RELIEF_FLAT,
                    expand_x=True,
                    pad=(0, 0),
                )
            ],
        ],
        background_color="#111827",
        expand_x=True,
        expand_y=True,
        key="-PAGE-CAD-",
        visible=False,
    )


def settings_page():
    # Dados de exemplo das configuracoes.
    options = [
        ["Notificacoes", "Ativas"],
        ["Backup automatico", "Diario"],
        ["Idioma", "PT-BR"],
        ["Fuso horario", "America/Sao_Paulo"],
    ]
    integrations = [
        ["Email", "Conectado"],
        ["ERP", "Pendente"],
        ["Planilhas", "Conectado"],
    ]

    return sg.Column(
        [
            # Titulo e subtitulo da pagina.
            [sg.Text("Configuracoes", font=("Arial", 24, "bold"), text_color="white")],
            [sg.Text("Preferencias do sistema", font=("Arial", 10), text_color="#AAB4C3")],
            [sg.HorizontalSeparator(color="#2A3546")],
            [
                # Tabela de preferencias gerais.
                sg.Frame(
                    "",
                    [
                        [sg.Text("Perfil", font=("Arial", 14, "bold"), text_color="white")],
                        [
                            sg.Table(
                                values=options,
                                headings=["Opcao", "Status"],
                                auto_size_columns=True,
                                num_rows=4,
                                background_color="#0F172A",
                                text_color="#E5E7EB",
                                header_background_color="#1F2937",
                                header_text_color="#E5E7EB",
                                row_height=26,
                                justification="left",
                                border_width=0,
                                size=(36, 5),
                            )
                        ],
                    ],
                    background_color="#18212E",
                    border_width=0,
                    relief=sg.RELIEF_FLAT,
                    expand_x=True,
                    pad=(0, 12),
                )
            ],
            [
                # Acoes de seguranca.
                sg.Frame(
                    "",
                    [
                        [sg.Text("Seguranca", font=("Arial", 14, "bold"), text_color="white")],
                        [sg.Text("Senha expira em 25 dias", text_color="#B8C2CE")],
                        [
                            sg.Button("Trocar senha", button_color=("white", "#2D6CDF"), border_width=0, size=(14, 1)),
                            sg.Button("Sair de todos", button_color=("white", "#3A4656"), border_width=0, size=(14, 1)),
                        ],
                    ],
                    background_color="#18212E",
                    border_width=0,
                    relief=sg.RELIEF_FLAT,
                    expand_x=True,
                    pad=(0, 0),
                )
            ],
            [
                # Integracoes externas e botoes de gestao.
                sg.Frame(
                    "",
                    [
                        [sg.Text("Integracoes", font=("Arial", 14, "bold"), text_color="white")],
                        [
                            sg.Table(
                                values=integrations,
                                headings=["Servico", "Status"],
                                auto_size_columns=True,
                                num_rows=3,
                                background_color="#0F172A",
                                text_color="#E5E7EB",
                                header_background_color="#1F2937",
                                header_text_color="#E5E7EB",
                                row_height=26,
                                justification="left",
                                border_width=0,
                                size=(32, 4),
                            )
                        ],
                        [
                            sg.Button("Conectar", button_color=("white", "#2D6CDF"), border_width=0, size=(12, 1)),
                            sg.Button("Gerenciar", button_color=("white", "#3A4656"), border_width=0, size=(12, 1)),
                        ],
                    ],
                    background_color="#18212E",
                    border_width=0,
                    relief=sg.RELIEF_FLAT,
                    expand_x=True,
                    pad=(0, 12),
                )
            ],
        ],
        background_color="#111827",
        expand_x=True,
        expand_y=True,
        key="-PAGE-SCHEDULE-",
        visible=False,
    )


# Usa pin para permitir alternar visibilidade sem perder o tamanho do layout.
def pin_page(page):
    return sg.pin(page)


# =========================
# DASHBOARD
# =========================
# Janela principal com menu lateral e area de conteudo.
def dashboard_window(usuario):
    layout = [
        [
            # Coluna 1: Menu Lateral (Largura fixa, altura total)
            sg.Column(
                [
                    # Cabeçalho do menu lateral.
                    [sg.Text("FLOW LOG", font=("Arial", 24, "bold"), text_color="white")],
                    [sg.Text(f"Olá, {usuario}", font=("Arial", 11), text_color="#AAB4C3")],
                    
                    [sg.HorizontalSeparator(color="#2A3546")],
                    
                    # Botoes do menu.
                    [sidebar_button("Início", "-HOME-")],
                    [sidebar_button("Produtos", "-PRODUTO-")],
                    [sidebar_button("Relatórios", "-RELATO-")],
                    [sidebar_button("Cadastros", "-CAD-")],
                    [sidebar_button("Configurações", "-SCHEDULE-")],
                    [sg.VPush()],
                    [sidebar_button("Sair", "-LOGOUT-")],
                ],
                background_color="#111827",
                pad=((20, 20), (20, 20)),
                element_justification="left",
                vertical_alignment="top",
                expand_y=True,
                size=(250, None), # Aumentei um pouco a largura para telas maiores
            ),
            
            # Coluna 2: Área de Conteúdo (Expande para preencher a tela)
            sg.Column(
                [
                    [pin_page(home_page())],
                    [pin_page(products_page())],
                    [pin_page(reports_page())],
                    [pin_page(registrations_page())],
                    [pin_page(settings_page())],
                ],
                background_color="#111827",
                pad=((10, 20), (20, 20)),
                expand_x=True, # IMPORTANTE: Preenche a largura horizontal
                expand_y=True, # IMPORTANTE: Preenche a altura vertical
                vertical_alignment="top",
                key="-MAIN-CONTENT-"
            ),
        ]
    ]

    window = sg.Window(
        "Flow Log - Dashboard",
        layout,
        size=(1920, 1080), # Resolução alvo
        finalize=True,
        resizable=True,
        background_color="#111827",
        margins=(0, 0),
        element_padding=(0, 0) # Removi o padding padrão para um visual mais limpo
    )

    # Força o modo tela cheia maximizado
    window.maximize()
    
    return window


# =========================
# PROGRAMA PRINCIPAL
# =========================
# Valida as credenciais informadas e retorna status e usuario autenticado.
def attempt_login(window, values):
    # Centraliza a validacao do login para reutilizar em clique e Enter.
    user = values["-USER-"].strip()
    password = values["-PASS-"].strip()

    if user == "admin" and password == "123":
        return True, user

    window["-MSG-"].update("Usuario ou senha invalidos.")
    return False, None


def main():
    load_local_data()

    # Inicia pela janela de login e cria a do dashboard apos autenticacao.
    win_login = login_window()
    win_dash = None

    # Mapeia eventos do menu para as telas internas.
    page_map = {
        "-HOME-": "-PAGE-HOME-",
        "-PRODUTO-": "-PAGE-PRODUTO-",
        "-RELATO-": "-PAGE-RELATO-",
        "-CAD-": "-PAGE-CAD-",
        "-SCHEDULE-": "-PAGE-SCHEDULE-",
    }

    while True:
        # Le eventos de todas as janelas abertas (login e dashboard).
        window, event, values = sg.read_all_windows()

        # Fecha o app se o usuario fechar qualquer janela principal.
        if window == sg.WIN_CLOSED:
            break

        if window == win_login:
            # Eventos da tela de login.
            if event == "-EXIT-":
                break

            if event == "-ENTER-":
                logged_in, user = attempt_login(win_login, values)
                if logged_in:
                    # Fecha login e abre o dashboard.
                    win_login.close()
                    win_dash = dashboard_window(user)

        elif win_dash and window == win_dash:
            # Eventos da tela principal.
            if event == "-LOGOUT-":
                # Volta para o login.
                win_dash.close()
                win_dash = None
                win_login = login_window()

            # Alterna a visibilidade das colunas para simular navegacao entre telas.
            elif event in page_map:
                for key in page_map.values():
                    win_dash[key].update(visible=False)
                win_dash[page_map[event]].update(visible=True)
            elif event == "-ADD-CLIENT-":
                nome = sg.popup_get_text("Nome do cliente:", title="Adicionar cliente")
                if nome is not None:
                    nome = nome.strip()
                if not nome:
                    continue
                status = sg.popup_get_text("Status (Ativo/Inativo):", default_text="Ativo", title="Adicionar cliente")
                if status is None:
                    continue
                status = status.strip() or "Ativo"
                codigo = next_code("CL-", clients_data)
                clients_data.append({"codigo": codigo, "cliente": nome, "status": status})
                save_local_data()
                win_dash["-CLIENTS-TABLE-"].update(values=clients_rows())
                sg.popup("Cliente adicionado!", location=(100, 100))
            elif event == "-ADD-SUPPLIER-":
                fornecedor = sg.popup_get_text("Nome do fornecedor:", title="Adicionar fornecedor")
                if fornecedor is not None:
                    fornecedor = fornecedor.strip()
                if not fornecedor:
                    continue
                prazo = sg.popup_get_text("Prazo/Observacao:", default_text="Ate 48h", title="Adicionar fornecedor")
                if prazo is None:
                    continue
                prazo = prazo.strip() or "Ate 48h"
                codigo = next_code("FO-", suppliers_data)
                suppliers_data.append({"codigo": codigo, "fornecedor": fornecedor, "prazo": prazo})
                save_local_data()
                win_dash["-SUPPLIERS-TABLE-"].update(values=suppliers_rows())
                sg.popup("Fornecedor adicionado!", location=(100, 100))
            elif event == "-ADD-USER-":
                nome = sg.popup_get_text("Nome do usuario:", title="Adicionar usuario")
                if nome is not None:
                    nome = nome.strip()
                if not nome:
                    continue
                perfil = sg.popup_get_text("Perfil:", default_text="Operador", title="Adicionar usuario")
                if perfil is None:
                    continue
                perfil = perfil.strip() or "Operador"
                codigo = next_code("USR-", users_data)
                users_data.append({"codigo": codigo, "nome": nome, "perfil": perfil})
                save_local_data()
                win_dash["-USERS-TABLE-"].update(values=users_rows())
                sg.popup("Usuario adicionado!", location=(100, 100))
            elif event == "-AGENDA-ADD-":
                nome = values["-AGENDA-NOME-"].strip()
                celular = values["-AGENDA-CELULAR-"].strip()
                if nome and celular:
                    criar_amigo(nome, celular)
                    win_dash["-AGENDA-TABLE-"].update(values=agenda_rows())
                    sg.popup("Amigo cadastrado!", location=(100, 100))
                else:
                    sg.popup("Informe nome e celular.", location=(100, 100))
            elif event == "-AGENDA-SEARCH-":
                nome = values["-AGENDA-NOME-"].strip()
                if not nome:
                    sg.popup("Informe o nome para pesquisar.", location=(100, 100))
                else:
                    item = consultar_amigo(nome)
                    if item:
                        sg.popup(f"Achei o celular do(a) {item['nome']}, e {item['celular']}.", location=(100, 100))
                    else:
                        sg.popup("Nao encontrado.", location=(100, 100))
            elif event == "-AGENDA-UPDATE-":
                nome = values["-AGENDA-NOME-"].strip()
                celular = values["-AGENDA-CELULAR-"].strip()
                if nome and celular:
                    if atualizar_amigo(nome, celular):
                        win_dash["-AGENDA-TABLE-"].update(values=agenda_rows())
                        sg.popup("Contato atualizado!", location=(100, 100))
                    else:
                        sg.popup("Nome nao encontrado.", location=(100, 100))
                else:
                    sg.popup("Informe nome e novo celular.", location=(100, 100))
            elif event == "-AGENDA-DELETE-":
                nome = values["-AGENDA-NOME-"].strip()
                if nome:
                    if remover_amigo(nome):
                        win_dash["-AGENDA-TABLE-"].update(values=agenda_rows())
                        sg.popup("Contato removido!", location=(100, 100))
                    else:
                        sg.popup("Nome nao encontrado.", location=(100, 100))
                else:
                    sg.popup("Informe o nome para remover.", location=(100, 100))
            elif event == "-AGENDA-TABLE-":
                selected = values["-AGENDA-TABLE-"]
                if selected:
                    row = agenda_rows()[selected[0]]
                    win_dash["-AGENDA-NOME-"].update(row[0])
                    win_dash["-AGENDA-CELULAR-"].update(row[1])

    # Garante fechamento de todas as janelas remanescentes.
    for w in sg.get_open_windows():
        w.close()


if __name__ == "__main__":
    main()

#  Mantive este pois sei q funciona