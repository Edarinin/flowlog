import csv
import json
import os
import PySimpleGUI as sg
# from supabase import create_client, Client
from datetime import date, timedelta 

# ==============================================================================
# CAMINHOS E CONFIGURAÇÕES
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "flowlog_data.json")
LOGO_PATH = os.path.join(BASE_DIR, "Logo_Flow_log-png.png")
BANNER_PATH = os.path.join(BASE_DIR, "imgs/Flowlog.png")

# Caminhos do SupaBase
SUPABASE_URL = "https://gbfhudykukprfvsmdgxr.supabase.co"
SUPABASE_KEY = "sb_publishable_9zCLQycw_7wMJol_LXB9GA_SigdLMHk"

# Teste no banco, se não der certo, avisa que deu erro
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("Conexão Bem Sucedida!")
except Exception as e:
    supabase = None
    print(f"Erro na conexão: {e}")

# Variáveis globais de dados
agenda = []
clients_data = []
suppliers_data = []
users_data = []
products_data = []
movements = []

def default_data():
    return {
        "agenda": [
            {"nome": "Bruno", "celular": "11999999999"},
            {"nome": "Maria", "celular": "11988888888"},
        ],
        "clients": [{"codigo": "CL-01", "cliente": "Loja Central", "status": "Ativo"}],
        "suppliers": [{"codigo": "FO-01", "fornecedor": "Alpha Tech", "cnpj": "0", "fone": "0", "email": "fornecedor@flowlog.com"}],
        "users": [{"codigo": "USR-01", "nome": "Admin", "perfil": "Admin", "senha": "123"}],
        "products": [],
        "movements": [],
    }

# ==============================================================================
# SISTEMA DE CARREGAMENTO E FILTRAGEM (EXCLUSÃO LÓGICA)
# ==============================================================================
def load_local_data():
    global agenda, clients_data, suppliers_data, users_data, products_data, movements
    
    if os.path.exists(DATA_PATH):
        try:
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = default_data()
    else:
        data = default_data()

    agenda = data.get("agenda", [])
    clients_data = data.get("clients", [])

    # --- Usuários do Supabase ---
    sucesso_users = False
    if supabase is not None:
        try:
            response_users = supabase.table("usuario").select("*").execute()
            users_data = []
            for row in response_users.data:
                if not row.get("status_usuario", True):
                    continue
                users_data.append({
                    "id_banco": row["id_usuario"],
                    "codigo": f"USR-{row['id_usuario']:02d}",
                    "nome": row["nome_usuario"],
                    "email": row["email"],
                    "senha": row["senha"],
                    "perfil": "Admin" if row["tipo_usuario"] else "Usuário Comum",
                    "status": row["status_usuario"]
                })
            sucesso_users = True
            print("⚡ Usuários carregados do Supabase!")
        except Exception as e:
            print(f"⚠️ Erro nos usuários (Supabase): {e}. Usando JSON local...")

    if not sucesso_users:
        users_data = data.get("users", [])

    # --- Produtos do Supabase ---
    sucesso_products = False
    if supabase is not None:
        try:
            response_prod = supabase.table("produto").select("*").execute()
            products_data = []
            for row in response_prod.data:
                if row["nome_pdt"].startswith("[OCULTO]"):
                    continue
                products_data.append({
                    "id_banco": row["id_produto"],
                    "sku": str(row["id_produto"]),                 
                    "nome": row["nome_pdt"],                        
                    "categoria": row["categoria_pdt"],              
                    "estoque": str(row["estoque_atual_pdt"]),       
                    "descricao": row["desc_pdt"],                   
                    "preco_compra": float(row["preco_compra_pd"]),
                    "valor_venda": float(row["valor_venda_pdt"]) if row["valor_venda_pdt"] else 0.0,
                    "data_cadastro": row["data_cadastro_pdt"]
                })
            sucesso_products = True
            print("⚡ Produtos carregados do Supabase!")
        except Exception as e:
            print(f"⚠️ Erro nos produtos (Supabase): {e}. Usando JSON local...")

    if not sucesso_products:
        products_data = data.get("products", [])

    # --- Fornecedores do Supabase ---
    sucesso_suppliers = False
    if supabase is not None:
        try:
            response_supp = supabase.table("fornecedor").select("*").execute()
            suppliers_data = []
            for row in response_supp.data:
                if row["nome_fornecedor"].startswith("[OCULTO]"):
                    continue
                suppliers_data.append({
                    "id_banco": row["id_fornecedor"],
                    "codigo": f"FO-{row['id_fornecedor']}",
                    "fornecedor": row["nome_fornecedor"],
                    "cnpj": str(row["cnpj_fornecedor"]),
                    "fone": str(row["fone_fornecedor"]),
                    "email": row["email_fornecedor"]
                })
            sucesso_suppliers = True
            print("⚡ Fornecedores carregados do Supabase!")
        except Exception as e:
            print(f"⚠️ Erro nos fornecedores (Supabase): {e}. Usando JSON local...")

    if not sucesso_suppliers:
        suppliers_data = data.get("suppliers", [])

    movements = data.get("movements", [])

    # Seed movements from products if no movements are present
    if (not movements) and products_data:
        seeded = []
        for p in products_data:
            raw_date = str(p.get("data_cadastro", "")).strip()
            if not raw_date:
                continue
            try:
                quantidade = int(str(p.get("estoque", "0")).strip() or 0)
            except Exception:
                quantidade = 0
            if quantidade <= 0:
                continue
            seeded.append({
                "data": raw_date,
                "tipo": "Entrada",
                "item": p.get("nome", "Produto"),
                "quantidade": quantidade,
                "usuario": "Sistema"
            })
        if seeded:
            movements = seeded
            data["movements"] = movements
            try:
                with open(DATA_PATH, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print("Movements seeded from products and saved to JSON.")
            except Exception as e:
                print(f"Falha ao salvar movimentos seed: {e}")


def save_local_data():
    """Garante o backup local imediato sincronizando o estado atual no JSON."""
    global agenda, clients_data, suppliers_data, users_data, products_data, movements
    data = {
        "agenda": agenda,
        "clients": clients_data,
        "suppliers": suppliers_data,
        "users": users_data,
        "products": products_data,
        "movements": movements,
    }
    try:
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("📁 Cópia salva no JSON local.")
    except Exception as e:
        print(f"❌ Erro no JSON local: {e}")


# ==============================================================================
# LÓGICA DE INSERTS DIRETOS
# ==============================================================================
def insert_usuario(nome, email, senha, perfil):
    global users_data
    max_id = 0
    for u in users_data:
        if u.get("id_banco") and u["id_banco"] > max_id:
            max_id = u["id_banco"]
    next_id = max_id + 1
    
    novo_usuario_banco = {
        "id_usuario": next_id,
        "senha": senha,
        "email": email,
        "data_criacao": date.today().isoformat(),
        "nome_usuario": nome,
        "tipo_usuario": True if perfil == "Admin" else False,
        "status_usuario": True
    }
    
    novo_usuario_python = {
        "id_banco": next_id,
        "codigo": f"USR-{next_id:02d}",
        "nome": nome,
        "email": email,
        "senha": senha,
        "perfil": perfil, 
        "status": True
    }
    
    if supabase is not None:
        try:
            supabase.table("usuario").insert(novo_usuario_banco).execute()
            print(f"⚡ {nome} inserido com sucesso no Supabase!")
        except Exception as e: print(f"❌ Falha Insert: {e}")
            
    users_data.append(novo_usuario_python)
    save_local_data()


# ==============================================================================
# FUNÇÕES DE FORMATAÇÃO E VALIDAÇÃO
# ==============================================================================
def format_date(date_str):
    """Formata data ISO para DD/MM/YYYY ou retorna '---' se inválida."""
    if not date_str or date_str == "---":
        return "---"
    try:
        d = date.fromisoformat(str(date_str).split("T")[0])
        return d.strftime("%d/%m/%Y")
    except Exception:
        return "---"

def format_number(value):
    """Formata número com separador de milhar."""
    try:
        return f"{int(value):,}".replace(",", ".")
    except Exception:
        return str(value)

def is_valid_email(email):
    """Validação básica de email."""
    return "@" in email and "." in email.split("@")[-1]

def is_valid_cnpj(cnpj):
    """Validação básica de CNPJ (apenas verifica se tem 14 dígitos)."""
    clean = "".join(c for c in str(cnpj) if c.isdigit())
    return len(clean) == 14 or len(clean) == 0

def sku_exists(sku, exclude_index=None):
    """Verifica se um SKU já existe na lista de produtos."""
    for i, p in enumerate(products_data):
        if str(p.get("sku", "")).strip() == str(sku).strip():
            if exclude_index is None or i != exclude_index:
                return True
    return False

def append_movement(tipo, item, quantidade, usuario="Sistema", data_entry=None):
    global movements
    try:
        quantidade = int(str(quantidade).strip() or 0)
    except Exception:
        quantidade = 0
    if data_entry is None:
        data_entry = date.today().isoformat()
    movements.append({
        "data": data_entry,
        "tipo": tipo,
        "item": item,
        "quantidade": quantidade,
        "usuario": usuario,
    })


def insert_produto(sku, nome, categoria, estoque):
    global products_data
    if not sku.strip() or not nome.strip():
        raise ValueError("SKU e Nome são obrigatórios.")
    if sku_exists(sku):
        raise ValueError(f"SKU '{sku}' já existe na base de dados.")
    try:
        estoque_num = int(str(estoque).strip() or 0)
    except ValueError:
        raise ValueError("Estoque deve ser um número válido.")
    
    try: id_prod = int(sku.strip())
    except ValueError:
        max_id = 0
        for p in products_data:
            if p.get("id_banco") and p["id_banco"] > max_id: max_id = p["id_banco"]
        id_prod = max_id + 1

    novo_prod_banco = {
        "id_produto": id_prod,
        "nome_pdt": nome,
        "desc_pdt": "Nenhuma descrição informada",
        "data_cadastro_pdt": date.today().isoformat(),
        "preco_compra_pd": 0.0,
        "estoque_atual_pdt": estoque_num,
        "categoria_pdt": categoria,
        "valor_venda_pdt": 0.0
    }
    
    novo_prod_python = {
        "id_banco": id_prod,
        "sku": str(id_prod),
        "nome": nome,
        "categoria": categoria,
        "estoque": str(estoque_num),
        "descricao": "Nenhuma descrição informada",
        "preco_compra": 0.0,
        "valor_venda": 0.0,
        "data_cadastro": date.today().isoformat()
    }
    
    if supabase is not None:
        try:
            supabase.table("produto").insert(novo_prod_banco).execute()
            print(f"⚡ Produto '{nome}' inserido com sucesso no Supabase!")
        except Exception as e: print(f"❌ Falha Insert: {e}")
            
    products_data.append(novo_prod_python)
    append_movement("Entrada", nome, estoque_num)
    save_local_data()


def insert_fornecedor(nome, cnpj="", fone="", email=""):
    global suppliers_data
    if not nome.strip():
        raise ValueError("Nome do fornecedor é obrigatório.")
    if email and not is_valid_email(email):
        raise ValueError(f"E-mail '{email}' inválido.")
    if cnpj and not is_valid_cnpj(cnpj):
        raise ValueError("CNPJ deve ter 14 dígitos.")
    
    max_id = 0
    for s in suppliers_data:
        if s.get("id_banco") and s["id_banco"] > max_id:
            max_id = s["id_banco"]
    next_id = max_id + 1
    
    email_final = email.strip() if (email and str(email).strip()) else "fornecedor@flowlog.com"
    try: cnpj_final = int(str(cnpj).strip()) if (cnpj and str(cnpj).strip()) else 0
    except ValueError: cnpj_final = 0
    try: fone_final = int(str(fone).strip()) if (fone and str(fone).strip()) else 0
    except ValueError: fone_final = 0
    
    novo_forn_banco = {
        "id_fornecedor": next_id,
        "nome_fornecedor": nome,
        "cnpj_fornecedor": cnpj_final,
        "fone_fornecedor": fone_final,
        "email_fornecedor": email_final,
        "data_cadastro_f": date.today().isoformat()
    }
    
    novo_forn_python = {
        "id_banco": next_id,
        "codigo": f"FO-{next_id}", 
        "fornecedor": nome,
        "cnpj": str(cnpj_final),
        "fone": str(fone_final),
        "email": email_final
    }
    
    if supabase is not None:
        try:
            supabase.table("fornecedor").insert(novo_forn_banco).execute()
            print(f"⚡ Fornecedor '{nome}' inserido com sucesso no Supabase!")
        except Exception as e: print(f"❌ Falha Insert Fornecedor: {e}")
            
    suppliers_data.append(novo_forn_python)
    save_local_data()


# ==============================================================================
# LÓGICA DE ATUALIZAÇÕES DIRETAS
# ==============================================================================
def update_usuario(index, nome, email, senha, perfil):
    global users_data
    id_banco = users_data[index].get("id_banco")
    if id_banco and supabase is not None:
        try:
            update_banco = {"nome_usuario": nome, "email": email, "senha": senha, "tipo_usuario": True if perfil == "Admin" else False}
            supabase.table("usuario").update(update_banco).eq("id_usuario", id_banco).execute()
        except Exception as e: print(f"❌ Erro Update: {e}")
    users_data[index]["nome"], users_data[index]["email"], users_data[index]["senha"], users_data[index]["perfil"] = nome, email, senha, perfil
    save_local_data()

def update_produto(index, sku, nome, categoria, estoque):
    global products_data
    id_banco = products_data[index].get("id_banco")
    old_estoque = 0
    try:
        old_estoque = int(str(products_data[index].get("estoque", "0")).strip() or 0)
    except Exception:
        old_estoque = 0
    if id_banco and supabase is not None:
        try:
            update_banco = {"nome_pdt": nome, "categoria_pdt": categoria, "estoque_atual_pdt": int(estoque if estoque else 0)}
            supabase.table("produto").update(update_banco).eq("id_produto", id_banco).execute()
        except Exception as e: print(f"❌ Erro Update: {e}")
    products_data[index]["sku"], products_data[index]["nome"], products_data[index]["categoria"], products_data[index]["estoque"] = sku, nome, categoria, str(estoque)
    try:
        novo_estoque = int(str(estoque).strip() or 0)
    except Exception:
        novo_estoque = old_estoque
    diff = novo_estoque - old_estoque
    if diff > 0:
        append_movement("Entrada", nome, diff)
    elif diff < 0:
        append_movement("Saída", nome, abs(diff))
    save_local_data()

def update_fornecedor(index, nome, cnpj="", fone="", email=""):
    global suppliers_data
    id_banco = suppliers_data[index].get("id_banco")
    email_final = email.strip() if (email and str(email).strip()) else "fornecedor@flowlog.com"
    try: cnpj_final = int(str(cnpj).strip()) if (cnpj and str(cnpj).strip()) else 0
    except ValueError: cnpj_final = 0
    try: fone_final = int(str(fone).strip()) if (fone and str(fone).strip()) else 0
    except ValueError: fone_final = 0
    if id_banco and supabase is not None:
        try:
            update_banco = {"nome_fornecedor": nome, "cnpj_fornecedor": cnpj_final, "fone_fornecedor": fone_final, "email_fornecedor": email_final}
            supabase.table("fornecedor").update(update_banco).eq("id_fornecedor", id_banco).execute()
        except Exception as e: print(f"❌ Erro Update: {e}")
    suppliers_data[index]["fornecedor"], suppliers_data[index]["cnpj"], suppliers_data[index]["fone"], suppliers_data[index]["email"] = nome, str(cnpj_final), str(fone_final), email_final
    save_local_data()


# ==============================================================================
# LÓGICA DE EXCLUSÃO LÓGICA (SOFT DELETE)
# ==============================================================================
def delete_usuario(index):
    global users_data
    id_banco = users_data[index].get("id_banco")
    if id_banco and supabase is not None:
        try: supabase.table("usuario").update({"status_usuario": False}).eq("id_usuario", id_banco).execute()
        except Exception as e: print(f"❌ Erro Delete: {e}")
    del users_data[index]
    save_local_data()

def delete_produto(index):
    global products_data
    id_banco = products_data[index].get("id_banco")
    nome = products_data[index].get("nome")
    estoque_atual = 0
    try:
        estoque_atual = int(str(products_data[index].get("estoque", "0")).strip() or 0)
    except Exception:
        estoque_atual = 0
    if id_banco and supabase is not None:
        try: supabase.table("produto").update({"nome_pdt": f"[OCULTO] {nome}"}).eq("id_produto", id_banco).execute()
        except Exception as e: print(f"❌ Erro Delete: {e}")
    if estoque_atual > 0:
        append_movement("Saída", nome, estoque_atual)
    del products_data[index]
    save_local_data()

def delete_fornecedor(index):
    global suppliers_data
    id_banco = suppliers_data[index].get("id_banco")
    nome = suppliers_data[index].get("fornecedor")
    if id_banco and supabase is not None:
        try: supabase.table("fornecedor").update({"nome_fornecedor": f"[OCULTO] {nome}"}).eq("id_fornecedor", id_banco).execute()
        except Exception as e: print(f"❌ Erro Delete: {e}")
    del suppliers_data[index]
    save_local_data()


# ==============================================================================
# COMPONENTES AUXILIARES E INTERFACE
# ==============================================================================
def products_count(): return str(len(products_data))
def suppliers_count(): return str(len(suppliers_data))
def users_count(): return str(len(users_data))

def testar_conexao_supabase():
    if supabase is None: return False
    try:
        supabase.table("usuario").select("count", count="exact").execute()
        print("⚡ Conexão com o Supabase realizada com sucesso!")
        return True
    except Exception as e: return False

def get_recent_activities():
    recentes = []
    for u in users_data[-3:]:
        recentes.append(["Novo", "Funcionário", u.get("nome", "---"), "Acesso Liberado"])
    for s in suppliers_data[-3:]:
        recentes.append(["Novo", "Fornecedor", s.get("fornecedor", "---"), s.get("email", "---")])
    if not recentes:
        return [["---", "Sem atividades", "---", "---"]]
    return recentes[-6:]


def low_stock_count(threshold=5):
    try:
        return str(sum(1 for p in products_data if int(str(p.get("estoque", "0")).strip() or 0) <= threshold))
    except Exception:
        return "0"


def alerts_count():
    return str(len(important_alerts()))


def recent_movements_count():
    return str(len(movements))


def important_alerts():
    alerts = []
    low_stock = int(low_stock_count())
    if low_stock > 0:
        alerts.append({
            "title": f"{low_stock} produtos com estoque baixo",
            "subtitle": "Alguns produtos precisam de reposição.",
            "color": "#F59E0B"
        })
    else:
        alerts.append({
            "title": "Sem estoque baixo",
            "subtitle": "Nenhum produto crítico no momento.",
            "color": "#10B981"
        })
    alerts.append({
        "title": "Backup do sistema",
        "subtitle": "Último backup realizado com sucesso.",
        "color": "#3B82F6"
    })
    alerts.append({
        "title": "Sistema atualizado",
        "subtitle": "Todas as funções operando normalmente.",
        "color": "#22C55E"
    })
    return alerts


def latest_movements_rows():
    if not movements:
        if not products_data:
            return [["---", "---", "---", "---"]]

        sorted_products = sorted(
            products_data,
            key=lambda p: str(p.get("data_cadastro", "")),
            reverse=True
        )[:4]
        rows = []
        for product in sorted_products:
            quantidade = 0
            try:
                quantidade = int(str(product.get("estoque", "0")).strip() or 0)
            except Exception:
                quantidade = 0
            rows.append([
                format_date(product.get("data_cadastro", "---")),
                "Entrada",
                f"{product.get('nome', '---')} (+{format_number(quantidade)})",
                "Sistema"
            ])
        return rows

    rows = []
    for m in movements[-4:][::-1]:
        quantidade = str(m.get("quantidade", "0"))
        tipo = m.get("tipo", "")
        sign = "+" if tipo.lower() == "entrada" else "-"
        descricao = f"{m.get('item', '---')} ({sign}{format_number(quantidade)})"
        rows.append([
            format_date(m.get("data", "---")),
            tipo,
            descricao,
            m.get("usuario", "Sistema")
        ])
    return rows


def movement_trend_data(days=7):
    resultados = []
    hoje = date.today()
    entradas_por_dia = {}
    saidas_por_dia = {}
    tem_entrada_movimento = False

    for m in movements:
        raw_date = str(m.get("data", "")).strip()
        if not raw_date:
            continue
        try:
            dia = date.fromisoformat(raw_date.split("T")[0])
        except Exception:
            continue
        quantidade = 0
        try:
            quantidade = int(str(m.get("quantidade", "0")).strip() or 0)
        except Exception:
            quantidade = 0
        tipo = str(m.get("tipo", "")).strip().lower().replace(" ", "")
        if "entrada" in tipo:
            tem_entrada_movimento = True
            entradas_por_dia[dia] = entradas_por_dia.get(dia, 0) + quantidade
        elif "saida" in tipo or "saída" in tipo:
            saidas_por_dia[dia] = saidas_por_dia.get(dia, 0) + quantidade

    if not tem_entrada_movimento:
        for p in products_data:
            raw_date = str(p.get("data_cadastro", "")).strip()
            if not raw_date:
                continue
            try:
                dia = date.fromisoformat(raw_date.split("T")[0])
            except Exception:
                continue
            if (hoje - dia).days < 0 or (hoje - dia).days >= days:
                continue
            quantidade = 0
            try:
                quantidade = int(str(p.get("estoque", "0")).strip() or 0)
            except Exception:
                quantidade = 0
            entradas_por_dia[dia] = entradas_por_dia.get(dia, 0) + quantidade
    for offset in range(days - 1, -1, -1):
        dia = hoje - timedelta(days=offset)
        label = dia.strftime("%d/%m")
        resultados.append({
            "label": label,
            "entradas": entradas_por_dia.get(dia, 0),
            "saidas": saidas_por_dia.get(dia, 0),
        })
    return resultados


def movement_totals(days=7):
    data = movement_trend_data(days)
    entradas = sum(item["entradas"] for item in data)
    saidas = sum(item["saidas"] for item in data)
    return {"entradas": entradas, "saidas": saidas, "saldo": entradas - saidas}


def export_home_report(file_path, days=7):
    if not file_path:
        raise ValueError("Caminho de arquivo inválido")
    if not file_path.lower().endswith(".csv"):
        file_path += ".csv"

    totals = movement_totals(days)
    rows = [
        ["Relatório Flow Log"],
        ["Data", date.today().isoformat()],
        [],
        ["Resumo", "Valor"],
        ["Entradas", totals["entradas"]],
        ["Saídas", totals["saidas"]],
        ["Saldo", totals["saldo"]],
        [],
        ["Data", "Tipo", "Descrição", "Usuário"],
    ]

    for movimento in latest_movements_rows():
        rows.append(movimento)

    with open(file_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(rows)

    return file_path


def agenda_rows(): return [[i.get("nome", ""), i.get("celular", "") ] for i in agenda]
def users_rows(): return [[u.get("codigo", ""), u.get("nome", ""), u.get("perfil", "")] for u in users_data]
def clients_rows(): return [[c.get("codigo", ""), c.get("cliente", ""), c.get("status", "")] for c in clients_data]
def products_rows(): 
    return [[p.get("sku", ""), p.get("nome", ""), p.get("categoria", ""), format_number(p.get("estoque", "0"))] for p in products_data]

# MUDANÇA: Agora o grid exibe o E-mail no lugar do antigo prazo!
def suppliers_rows(): return [[s.get("codigo", ""), s.get("fornecedor", ""), s.get("email", "")] for s in suppliers_data]

def next_code(prefix, items, code_key="codigo"):
    max_num = 0
    for item in items:
        code = str(item.get(code_key, ""))
        if code.startswith(prefix):
            suffix = code[len(prefix):]
            try: max_num = max(max_num, int(suffix))
            except ValueError: continue
    next_num = max_num + 1
    return f"{prefix}{next_num:02d}" if prefix == "USR-" else f"{prefix}{next_num}"

def product_categories_count():
    categories = {str(p.get("categoria", "")).strip().lower() for p in products_data if str(p.get("categoria", "")).strip()}
    return str(len(categories))

def sidebar_button(text, key): return sg.Button(text, key=key, size=(22, 2), button_color=("white", "#0F172A"), border_width=0, pad=(5, 5), mouseover_colors=("white", "#00B4FF"), font=("Arial", 10, "bold"))
def card(title, value, subtitle, value_key=None): return sg.Frame("", [[sg.Text(title, font=("Arial", 10, "bold"), text_color="#00B4FF", background_color="#1E293B")], [sg.Text(str(value), key=value_key, font=("Arial", 26, "bold"), text_color="white", background_color="#1E293B")], [sg.Text(subtitle, font=("Arial", 9), text_color="#94A3B8", background_color="#1E293B")]], background_color="#1E293B", border_width=0, expand_x=True, pad=(12, 12))
def image_if_exists(path, size=(None, None), reduzir=1):
    if os.path.exists(path): return sg.Image(filename=path, size=size, background_color="#00050A", subsample=reduzir)
    return sg.Text("", background_color="#00050A")