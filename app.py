import os
import PySimpleGUI as sg
import data_manager
from paginas.inicio import inicio_page
from paginas.produtos import produtos_page
from paginas.registros import registros_page
from paginas.configuracoes import configuracoes_page
from data_manager import (
    BANNER_PATH,
    image_if_exists 
)

# Configuração de Tema e Cores
meu_tema = {
    'BACKGROUND': '#020817',      
    'TEXT': '#FFFFFF',
    'INPUT': '#0F172A',
    'TEXT_INPUT': '#FFFFFF',
    'SCROLL': '#0F172A',
    'BUTTON': ('#FFFFFF', '#00B4FF'), 
    'PROGRESS': ('#00B4FF', '#0F172A'),
    'BORDER': 0, 
    'SLIDER_DEPTH': 0, 
    'PROGRESS_DEPTH': 0,
}

sg.theme_add_new('FlowLogNeon', meu_tema)
sg.theme('FlowLogNeon')

# ==============================================================================
# JANELAS POPUP MODAIS
# ==============================================================================
def abrir_popup_usuario(u=None):
    titulo = "Atualizar Funcionário" if u else "Adicionar Funcionário"
    layout = [
        [sg.Text(titulo, font=("Arial", 16, "bold"), text_color="white", pad=(0, 10))],
        [sg.Text("Nome:", size=(12, 1), font=("Arial", 10), text_color="#AAB4C3"), sg.Input(default_text=u.get("nome", "") if u else "", key="-NOME-", size=(32, 1), background_color="#0F172A", text_color="#E5E7EB", border_width=1)],
        [sg.Text("E-mail:", size=(12, 1), font=("Arial", 10), text_color="#AAB4C3"), sg.Input(default_text=u.get("email", "") if u else "", key="-EMAIL-", size=(32, 1), background_color="#0F172A", text_color="#E5E7EB", border_width=1)],
        [sg.Text("Senha:", size=(12, 1), font=("Arial", 10), text_color="#AAB4C3"), sg.Input(default_text=u.get("senha", "") if u else "", key="-PASS-", password_char="*", size=(32, 1), background_color="#0F172A", text_color="#E5E7EB", border_width=1)],
        [sg.Text("Perfil:", size=(12, 1), font=("Arial", 10), text_color="#AAB4C3"), sg.Combo(["Admin", "Usuário Comum"], default_value=u.get("perfil", "Usuário Comum") if u else "Usuário Comum", key="-PERFIL-", readonly=True, size=(30, 1), background_color="#0F172A", text_color="#E5E7EB")],
        [sg.Text("")],
        [sg.Push(), sg.Button("Salvar", key="-SALVAR-", button_color=("white", "#0F7381"), border_width=0, size=(12, 1)), sg.Button("Cancelar", key="-CANCELAR-", button_color=("white", "#6B7280"), border_width=0, size=(12, 1)), sg.Push()]
    ]
    win = sg.Window(titulo, layout, finalize=True, modal=True, element_justification="center", background_color="#020817")
    dados_retorno = None
    while True:
        ev, val = win.read()
        if ev in (sg.WIN_CLOSED, "-CANCELAR-"): break
        if ev == "-SALVAR-":
            dados_retorno = {"nome": val["-NOME-"].strip(), "email": val["-EMAIL-"].strip(), "senha": val["-PASS-"].strip(), "perfil": val["-PERFIL-"].strip()}
            break
    win.close()
    return dados_retorno

def abrir_popup_produto(p=None):
    titulo = "Atualizar Produto" if p else "Adicionar Produto"
    sku_bloqueado = True if p else False
    layout = [
        [sg.Text(titulo, font=("Arial", 16, "bold"), text_color="white", pad=(0, 10))],
        [sg.Text("SKU (Número):", size=(12, 1), font=("Arial", 10), text_color="#AAB4C3"), sg.Input(default_text=p.get("sku", "") if p else "", key="-SKU-", disabled=sku_bloqueado, size=(32, 1), background_color="#0F172A", text_color="#E5E7EB", border_width=1)],
        [sg.Text("Nome:", size=(12, 1), font=("Arial", 10), text_color="#AAB4C3"), sg.Input(default_text=p.get("nome", "") if p else "", key="-NOME-", size=(32, 1), background_color="#0F172A", text_color="#E5E7EB", border_width=1)],
        [sg.Text("Categoria:", size=(12, 1), font=("Arial", 10), text_color="#AAB4C3"), sg.Combo(["Capilar", "Barba", "Capilar e Barba", "Acessório", "Corporal", "Higiene", "Manutenção", "Ferramenta"], default_value=p.get("categoria", "Capilar") if p else "Capilar", key="-CAT-", readonly=True, size=(30, 1), background_color="#0F172A", text_color="#E5E7EB")],
        [sg.Text("Qtd. Estoque:", size=(12, 1), font=("Arial", 10), text_color="#AAB4C3"), sg.Input(default_text=p.get("estoque", "") if p else "", key="-ESTOQUE-", size=(32, 1), background_color="#0F172A", text_color="#E5E7EB", border_width=1)],
        [sg.Text("")],
        [sg.Push(), sg.Button("Salvar", key="-SALVAR-", button_color=("white", "#0F7381"), border_width=0, size=(12, 1)), sg.Button("Cancelar", key="-CANCELAR-", button_color=("white", "#6B7280"), border_width=0, size=(12, 1)), sg.Push()]
    ]
    win = sg.Window(titulo, layout, finalize=True, modal=True, element_justification="center", background_color="#020817")
    dados_retorno = None
    while True:
        ev, val = win.read()
        if ev in (sg.WIN_CLOSED, "-CANCELAR-"): break
        if ev == "-SALVAR-":
            dados_retorno = {"sku": val["-SKU-"].strip(), "nome": val["-NOME-"].strip(), "categoria": val["-CAT-"].strip(), "estoque": val["-ESTOQUE-"].strip()}
            break
    win.close()
    return dados_retorno

def abrir_popup_fornecedor(s=None):
    titulo = "Atualizar Fornecedor" if s else "Adicionar Fornecedor"
    layout = [
        [sg.Text(titulo, font=("Arial", 16, "bold"), text_color="white", pad=(0, 10))],
        [sg.Text("Nome:", size=(12, 1), font=("Arial", 10), text_color="#AAB4C3"), sg.Input(default_text=s.get("fornecedor", "") if s else "", key="-NOME-", size=(32, 1), background_color="#0F172A", text_color="#E5E7EB", border_width=1)],
        [sg.Text("CNPJ:", size=(12, 1), font=("Arial", 10), text_color="#AAB4C3"), sg.Input(default_text=s.get("cnpj", "") if s else "", key="-CNPJ-", size=(32, 1), background_color="#0F172A", text_color="#E5E7EB", border_width=1)],
        [sg.Text("Telefone:", size=(12, 1), font=("Arial", 10), text_color="#AAB4C3"), sg.Input(default_text=s.get("fone", "") if s else "", key="-FONE-", size=(32, 1), background_color="#0F172A", text_color="#E5E7EB", border_width=1)],
        [sg.Text("E-mail:", size=(12, 1), font=("Arial", 10), text_color="#AAB4C3"), sg.Input(default_text=s.get("email", "") if s else "", key="-EMAIL-", size=(32, 1), background_color="#0F172A", text_color="#E5E7EB", border_width=1)],
        [sg.Text("")],
        [sg.Push(), sg.Button("Salvar", key="-SALVAR-", button_color=("white", "#0F7381"), border_width=0, size=(12, 1)), sg.Button("Cancelar", key="-CANCELAR-", button_color=("white", "#6B7280"), border_width=0, size=(12, 1)), sg.Push()]
    ]
    win = sg.Window(titulo, layout, finalize=True, modal=True, element_justification="center", background_color="#020817")
    dados_retorno = None
    while True:
        ev, val = win.read()
        if ev in (sg.WIN_CLOSED, "-CANCELAR-"): break
        if ev == "-SALVAR-":
            dados_retorno = {"fornecedor": val["-NOME-"].strip(), "cnpj": val["-CNPJ-"].strip(), "fone": val["-FONE-"].strip(), "email": val["-EMAIL-"].strip()}
            break
    win.close()
    return dados_retorno

# ==============================================================================
# JANELAS PRINCIPAIS E HELPERS
# ==============================================================================
def dashboard_window(usuario):
    layout = [
        [
            sg.Column([
                [image_if_exists(BANNER_PATH, reduzir=2)],
                [sg.Text('', background_color="#00050A", pad=(0, 8))],
                [data_manager.sidebar_button("  Início", "-HOME-")],
                [data_manager.sidebar_button("  Produtos", "-PRODUTO-")],
                [data_manager.sidebar_button("  Cadastros", "-CAD-")],
                [data_manager.sidebar_button("  Configurações", "-SCHEDULE-")],
                [sg.Push(background_color="#00050A")],
                [data_manager.sidebar_button("  Sair", "-LOGOUT-")],
            ], background_color="#00050A", expand_x=True, expand_y=True, size=(250, None), pad=(0,0), vertical_alignment="top", element_justification="left"),
            sg.VerticalSeparator(color="#1F2937"),
                sg.Column([
                    [sg.pin(inicio_page())], [sg.pin(produtos_page())], [sg.pin(registros_page())], [sg.pin(configuracoes_page())],
                ], expand_x=True, expand_y=True, background_color="#020817", key="-COL-CONTEUDO-", pad=(20,20), vertical_alignment="center", element_justification="center")
        ]
    ]
    window = sg.Window("Flow Log", layout, finalize=True, resizable=True)
    window.maximize()
    draw_home_graph(window)
    return window

def login_window():
    layout = [
        [sg.Text("Login Flow Log", font=("Arial", 20))],
        [sg.Text("E-mail"), sg.Input(key="-USER-", size=(20, 1))], 
        [sg.Text("Senha"), sg.Input(key="-PASS-", password_char="*", size=(20, 1))],
        [sg.Button("Entrar", key="-ENTER-", bind_return_key=True), sg.Button("Sair", key="-EXIT-")]
    ]
    return sg.Window("Login", layout, finalize=True, element_justification="center")

def update_if_exists(window, key, value=None, **kwargs):
    if window and key in window.AllKeysDict:
        if value is None: window[key].update(**kwargs)
        else: window[key].update(value, **kwargs)


def get_home_chart_days(window):
    if not window or "-HOME-CHART-RANGE-" not in window.AllKeysDict:
        return 7
    value = window["-HOME-CHART-RANGE-"].get()
    try:
        return int(str(value).split()[0])
    except Exception:
        return 7


def draw_home_graph(window):
    if not window or "-HOME-CHART-" not in window.AllKeysDict:
        return
    graph = window["-HOME-CHART-"]
    graph.erase()
    chart_type = "Linhas"
    if "-HOME-CHART-TYPE-" in window.AllKeysDict:
        chart_type = window["-HOME-CHART-TYPE-"].get()
    days = get_home_chart_days(window)
    data = data_manager.movement_trend_data(days=days)
    if not data:
        return

    width, height = 560, 260
    left, bottom, right, top = 40, 35, width - 20, height - 35
    graph.draw_text(f"Últimos {days} dias", (left + 80, top - 10), color="#94A3B8", font=("Arial", 8))
    graph.draw_line((left, bottom), (left, top), color="#334155")
    graph.draw_line((left, bottom), (right, bottom), color="#334155")

    max_value = max(max(item["entradas"] for item in data), max(item["saidas"] for item in data), 1)
    step = (right - left) / max(len(data) - 1, 1)
    entries_points = []
    exits_points = []
    bar_width = step * 0.18

    # Eixos e grade vertical
    for tick in range(5):
        y = bottom + (top - bottom) * tick / 4
        graph.draw_line((left - 4, y), (left, y), color="#334155")
        value = int(max_value * tick / 4)
        graph.draw_text(str(value), (left - 10, y), color="#94A3B8", font=("Arial", 8), text_location="right")
        if tick > 0:
            graph.draw_line((left, y), (right, y), color="#1F2937")

    label_step = max(1, len(data) // 8)

    for idx, item in enumerate(data):
        x = left + idx * step
        y_entry = bottom + (top - bottom) * item["entradas"] / max_value
        y_exit = bottom + (top - bottom) * item["saidas"] / max_value
        entries_points.append((x, y_entry))
        exits_points.append((x, y_exit))
        if idx % label_step == 0 or idx == len(data) - 1:
            graph.draw_text(item["label"], (x, bottom - 12), color="#94A3B8", font=("Arial", 8), text_location="center")

    def draw_bar(x_center, value, color):
        top_y = bottom + (top - bottom) * value / max_value
        graph.draw_rectangle((x_center - bar_width, bottom), (x_center + bar_width, top_y), fill_color=color, line_color=color)

    if chart_type == "Barras":
        for idx, item in enumerate(data):
            x = left + idx * step
            draw_bar(x - bar_width * 1.5, item["entradas"], "#3B82F6")
            draw_bar(x + bar_width * 1.5, item["saidas"], "#EF4444")
            graph.draw_text(str(item["entradas"]), (x - bar_width * 1.5, bottom + (top - bottom) * item["entradas"] / max_value + 14), color="#3B82F6", font=("Arial", 8))
            graph.draw_text(str(item["saidas"]), (x + bar_width * 1.5, bottom + (top - bottom) * item["saidas"] / max_value + 14), color="#EF4444", font=("Arial", 8))
    else:
        if len(entries_points) > 1:
            for i in range(len(entries_points) - 1):
                graph.draw_line(entries_points[i], entries_points[i + 1], color="#3B82F6", width=2)
        if len(exits_points) > 1:
            for i in range(len(exits_points) - 1):
                graph.draw_line(exits_points[i], exits_points[i + 1], color="#EF4444", width=2)
        if chart_type == "Área" and len(entries_points) > 1:
            area_points = [(entries_points[0][0], bottom)] + entries_points + [(entries_points[-1][0], bottom)]
            graph.draw_polygon(area_points, fill_color="#3B82F644", line_color="#3B82F6")
            area_points = [(exits_points[0][0], bottom)] + exits_points + [(exits_points[-1][0], bottom)]
            graph.draw_polygon(area_points, fill_color="#EF444444", line_color="#EF4444")

    for idx, point in enumerate(entries_points):
        graph.draw_circle(point, 4, fill_color="#3B82F6", line_color="#3B82F6")
        if chart_type != "Barras":
            graph.draw_text(str(data[idx]["entradas"]), (point[0], point[1] + 10), color="#3B82F6", font=("Arial", 8), text_location="center")
    for idx, point in enumerate(exits_points):
        graph.draw_circle(point, 4, fill_color="#EF4444", line_color="#EF4444")
        if chart_type != "Barras":
            graph.draw_text(str(data[idx]["saidas"]), (point[0], point[1] + 10), color="#EF4444", font=("Arial", 8), text_location="center")

    graph.draw_text("Entradas", (right - 80, top - 10), color="#3B82F6", font=("Arial", 8))
    graph.draw_text("Saídas", (right - 80, top - 22), color="#EF4444", font=("Arial", 8))


def refresh_json_views(window):
    if not window: return
    update_if_exists(window, "-PROD-TABLE-", values=data_manager.products_rows())
    update_if_exists(window, "-SUPPLIERS-TABLE-", values=data_manager.suppliers_rows())
    update_if_exists(window, "-USERS-TABLE-", values=data_manager.users_rows())
    chart_days = get_home_chart_days(window)
    totals = data_manager.movement_totals(chart_days)
    update_if_exists(window, "-HOME-PROD-COUNT-", data_manager.products_count())
    update_if_exists(window, "-HOME-ENTR-COUNT-", totals["entradas"])
    update_if_exists(window, "-HOME-SAID-COUNT-", totals["saidas"])
    update_if_exists(window, "-HOME-SALDO-COUNT-", totals["saldo"])
    update_if_exists(window, "-HOME-ALERT-COUNT-", data_manager.alerts_count())
    update_if_exists(window, "-HOME-MOV-COUNT-", data_manager.recent_movements_count())
    update_if_exists(window, "-TABLE-RECENTES-", values=data_manager.get_recent_activities())
    update_if_exists(window, "-TABLE-MOVIMENTOS-", values=data_manager.latest_movements_rows())

    for index, alert in enumerate(data_manager.important_alerts(), start=1):
        update_if_exists(window, f"-ALERT-{index}-TITLE-", alert["title"])
        update_if_exists(window, f"-ALERT-{index}-SUB-", alert["subtitle"])

    draw_home_graph(window)

def clear_product_fields(window):
    for k in ["-PROD-SKU-", "-PROD-NOME-", "-PROD-CAT-", "-PROD-ESTOQUE-"]:
        if k in window.AllKeysDict: window[k].update(value="Capilar") if k == "-PROD-CAT-" else window[k].update("")

def clear_supplier_fields(window):
    # MUDANÇA: Remoção do campo de prazo na rotina de limpeza
    for k in ["-SUPPLIER-NOME-", "-SUPPLIER-CNPJ-", "-SUPPLIER-FONE-", "-SUPPLIER-EMAIL-"]:
        if k in window.AllKeysDict: window[k].update("")

def clear_user_fields(window):
    for k in ["-USER-COD-", "-USER-NOME-", "-USER-PERFIL-", "-USER-PASS-", "-USER-EMAIL-"]:
        if k in window.AllKeysDict: window[k].update(value="Usuário Comum") if k == "-USER-PERFIL-" else window[k].update("")

# ==============================================================================
# MAIN LOOP
# ==============================================================================
def main():
    data_manager.load_local_data()
    data_manager.testar_conexao_supabase()
    win_login = login_window()
    win_dash = None
    selected_product = None
    selected_supplier = None
    selected_user = None
    page_map = {"-HOME-": "-PAGE-HOME-", "-PRODUTO-": "-PAGE-PRODUTO-", "-CAD-": "-PAGE-CAD-", "-SCHEDULE-": "-PAGE-SCHEDULE-"}

    while True:
        window, event, values = sg.read_all_windows()
        if event == sg.WIN_CLOSED or event == "-EXIT-": break

        if window == win_login and event == "-ENTER-":
            email_digitado = str(values["-USER-"]).strip().lower()
            senha_digitada = str(values["-PASS-"]).strip()
            usuario_autenticado = None
            for user in data_manager.users_data:
                if str(user.get("email", "")).strip().lower() == email_digitado and str(user.get("senha", "")) == senha_digitada:
                    usuario_autenticado = user.get("nome")
                    break
            if not usuario_autenticado and email_digitado == "admin@flowlog.com" and senha_digitada == "123":
                usuario_autenticado = "Administrador"
            if usuario_autenticado:
                win_login.close()
                win_dash = dashboard_window(usuario_autenticado)
                refresh_json_views(win_dash)
            else:
                sg.popup("E-mail ou Senha Incorretos", title="Erro", button_color="red")

        elif win_dash and window == win_dash:
            if event == "-LOGOUT-":
                win_dash.close()
                win_dash = None
                win_login = login_window()
            elif event in page_map:
                if event == "-HOME-":
                    refresh_json_views(win_dash)
                    window["-TABLE-RECENTES-"].update(values=data_manager.get_recent_activities())
                for key in page_map.values(): win_dash[key].update(visible=False)
                win_dash[page_map[event]].update(visible=True)

            elif event == "-HOME-CHART-TYPE-" or event == "-HOME-CHART-RANGE-":
                refresh_json_views(win_dash)
            elif event == "-HOME-REPORT-DOWNLOAD-":
                save_path = sg.popup_get_file(
                    "Salvar relatório como",
                    save_as=True,
                    no_window=True,
                    default_path=os.path.join(os.getcwd(), "relatorio_movimentacoes.csv"),
                    file_types=(("CSV Files", "*.csv"),),
                    default_extension=".csv",
                )
                if save_path:
                    try:
                        saved = data_manager.export_home_report(save_path)
                        sg.popup(f"Relatório salvo em:\n{saved}", title="Sucesso", button_color=("white", "#0F4C81"))
                        if "-HOME-REPORT-PATH-" in win_dash.AllKeysDict:
                            win_dash["-HOME-REPORT-PATH-"].update(saved)
                    except Exception as e:
                        sg.popup(f"Erro ao salvar relatório:\n{e}", title="Erro", button_color=("white", "#E53E3E"))

            # --- CRUD Funcionários ---
            elif event == "-USERS-TABLE-":
                selected = values["-USERS-TABLE-"]
                if selected: selected_user = selected[0]
            elif event == "-USER-ADD-":
                dados = abrir_popup_usuario()
                if dados:
                    if not dados["nome"] or not dados["senha"] or not dados["email"]:
                        sg.popup("Nome, E-mail e Senha são obrigatórios.", title="Aviso")
                        continue
                    data_manager.insert_usuario(dados["nome"], dados["email"], dados["senha"], dados["perfil"])
                    refresh_json_views(win_dash)
                    selected_user = None
            elif event == "-USER-UPDATE-":
                if selected_user is None:
                    sg.popup("Por favor, selecione um funcionário na tabela antes de atualizar.", title="Aviso")
                    continue
                dados = abrir_popup_usuario(data_manager.users_data[selected_user])
                if dados:
                    if not dados["nome"] or not dados["senha"] or not dados["email"]:
                        sg.popup("Nome, E-mail e Senha são obrigatórios.", title="Aviso")
                        continue
                    data_manager.update_usuario(selected_user, dados["nome"], dados["email"], dados["senha"], dados["perfil"])
                    refresh_json_views(win_dash)
                    selected_user = None
            elif event == "-USER-DELETE-":
                if selected_user is None:
                    sg.popup("Selecione um funcionário na tabela antes de ocultar.", title="Aviso")
                    continue
                data_manager.delete_usuario(selected_user)
                refresh_json_views(win_dash)
                selected_user = None

            # --- CRUD Fornecedores ---
            elif event == "-SUPPLIERS-TABLE-":
                selected = values["-SUPPLIERS-TABLE-"]
                if selected: selected_supplier = selected[0]
            elif event == "-SUPPLIER-ADD-":
                dados = abrir_popup_fornecedor()
                if dados:
                    try:
                        data_manager.insert_fornecedor(dados["fornecedor"], dados["cnpj"], dados["fone"], dados["email"])
                        refresh_json_views(win_dash)
                        sg.popup(f"Fornecedor '{dados['fornecedor']}' adicionado com sucesso!", title="Sucesso")
                        selected_supplier = None
                    except ValueError as e:
                        sg.popup(f"Erro: {str(e)}", title="Aviso")
            elif event == "-SUPPLIER-UPDATE-":
                if selected_supplier is None:
                    sg.popup("Selecione um fornecedor na tabela antes de atualizar.", title="Aviso")
                    continue
                dados = abrir_popup_fornecedor(data_manager.suppliers_data[selected_supplier])
                if dados:
                    if not dados["fornecedor"]:
                        sg.popup("O nome do fornecedor é obrigatório.", title="Aviso")
                        continue
                    # Chamada ao data_manager atualizada sem o parâmetro de prazo!
                    data_manager.update_fornecedor(selected_supplier, dados["fornecedor"], dados["cnpj"], dados["fone"], dados["email"])
                    refresh_json_views(win_dash)
                    sg.popup("Cadastro do fornecedor atualizado com sucesso!", title="Sucesso")
                    selected_supplier = None
            elif event == "-SUPPLIER-DELETE-":
                if selected_supplier is None:
                    sg.popup("Selecione um fornecedor na tabela antes de ocultar.", title="Aviso")
                    continue
                data_manager.delete_fornecedor(selected_supplier)
                refresh_json_views(win_dash)
                selected_supplier = None

            # --- CRUD Produtos ---
            elif event == "-PROD-TABLE-":
                selected = values["-PROD-TABLE-"]
                if selected:
                    selected_product = selected[0]
                    produto = data_manager.products_data[selected_product]
                    win_dash["-PROD-SKU-"].update(produto.get("sku", ""))
                    win_dash["-PROD-NOME-"].update(produto.get("nome", ""))
                    win_dash["-PROD-CAT-"].update(produto.get("categoria", ""))
                    win_dash["-PROD-ESTOQUE-"].update(produto.get("estoque", ""))
            elif event == "-PROD-ADD-":
                sku, nome, categoria, estoque = values["-PROD-SKU-"].strip(), values["-PROD-NOME-"].strip(), values["-PROD-CAT-"].strip(), values["-PROD-ESTOQUE-"].strip()
                try:
                    data_manager.insert_produto(sku, nome, categoria, estoque)
                    refresh_json_views(win_dash)
                    clear_product_fields(win_dash)
                    sg.popup(f"Produto '{nome}' adicionado com sucesso!", title="Sucesso")
                    selected_product = None
                except ValueError as e:
                    sg.popup(f"Erro: {str(e)}", title="Aviso")
            elif event == "-PROD-UPDATE-":
                if selected_product is None:
                    sg.popup("Selecione um produto na tabela antes de atualizar.", title="Aviso")
                    continue
                sku, nome, categoria, estoque = values["-PROD-SKU-"].strip(), values["-PROD-NOME-"].strip(), values["-PROD-CAT-"].strip(), values["-PROD-ESTOQUE-"].strip()
                if not sku or not nome:
                    sg.popup("SKU e Nome do produto são obrigatórios.", title="Aviso")
                    continue
                data_manager.update_produto(selected_product, sku, nome, categoria, estoque)
                refresh_json_views(win_dash)
                sg.popup("Estoque do produto atualizado com sucesso!", title="Sucesso")
                clear_product_fields(win_dash)
                selected_product = None
            elif event == "-PROD-DELETE-":
                if selected_product is None:
                    sg.popup("Selecione um produto na tabela antes de ocultar.", title="Aviso")
                    continue
                data_manager.delete_produto(selected_product)
                refresh_json_views(win_dash)
                clear_product_fields(win_dash)
                selected_product = None

    for open_window in sg.get_open_windows(): open_window.close()

if __name__ == "__main__": main()