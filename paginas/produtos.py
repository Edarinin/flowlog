import PySimpleGUI as sg
from data_manager import (
    card,
    product_categories_count,
    products_count,
    products_rows,
    suppliers_count,
)

def produtos_page():

    layout = [
        [sg.Text("Produtos", font=("Arial", 24, "bold"), text_color="white")],
        [sg.Text("Gerencie o estoque, categorias e fornecedores com mais clareza.", font=("Arial", 11), text_color="#AAB4C3")],
        [sg.HorizontalSeparator(color="#2A3546", pad=(0, 10))],

        [
            card("Produtos", products_count(), "Cadastrados", "-PROD-COUNT-"),
            card("Categorias", product_categories_count(), "Com produtos", "-PROD-CAT-COUNT-"),
            card("Fornecedores", suppliers_count(), "Parceiros", "-PROD-SUPPLIERS-COUNT-")
        ],

        [
            sg.Column([
                [sg.Frame("Cadastro de Produtos", [
                    [sg.Text("SKU (Número)", font=("Arial", 9), text_color="#AAB4C3"), sg.Input(key="-PROD-SKU-", size=(30, 1), background_color="#0F172A", text_color="#E5E7EB", border_width=1, pad=((6, 0), 4))],
                    [sg.Text("Nome do Produto", font=("Arial", 9), text_color="#AAB4C3"), sg.Input(key="-PROD-NOME-", size=(30, 1), background_color="#0F172A", text_color="#E5E7EB", border_width=1, pad=((6, 0), 4))],
                    [sg.Text("Categoria", font=("Arial", 9), text_color="#AAB4C3"), sg.Combo([
                        "Capilar", "Barba", "Capilar e Barba", "Acessório", 
                        "Corporal", "Higiene", "Manutenção", "Ferramenta"
                    ], default_value="Capilar", key="-PROD-CAT-", readonly=True, size=(28, 1), background_color="#0F172A", text_color="#E5E7EB", pad=((6, 0), 4))],
                    [sg.Text("Qtd. Estoque", font=("Arial", 9), text_color="#AAB4C3"), sg.Input(key="-PROD-ESTOQUE-", size=(30, 1), background_color="#0F172A", text_color="#E5E7EB", border_width=1, pad=((6, 0), 4))],
                    [
                        sg.Button("Adicionar", key="-PROD-ADD-", button_color=("white", "#0F7381"), border_width=0, size=(12, 1), pad=(0, 8)),
                        sg.Button("Atualizar", key="-PROD-UPDATE-", button_color=("white", "#0F4C81"), border_width=0, size=(12, 1), pad=(0, 8)),
                        sg.Button("Excluir", key="-PROD-DELETE-", button_color=("white", "#6B7280"), border_width=0, size=(12, 1))
                    ],
                    [sg.Text("", pad=(0, 8))],
                    [
                        sg.Table(
                            values=products_rows(),
                            headings=["SKU", "Produto", "Categoria", "Estoque"],
                            key="-PROD-TABLE-",
                            enable_events=True,
                            auto_size_columns=True,
                            num_rows=8,
                            row_height=28,
                            background_color="#0F172A",
                            text_color="#E5E7EB",
                            alternating_row_color="#111827",
                            header_background_color="#1F2937",
                            header_text_color="#E5E7EB",
                            vertical_scroll_only=True,
                            pad=(0, 0),
                        )
                    ]
                ], background_color="#111827", border_width=0, pad=(0, 10), element_justification="left")]
            ], expand_x=True, expand_y=False)
        ]
    ]

    return sg.Column(
        layout,
        background_color="#111827",
        expand_x=True,
        expand_y=True,
        key="-PAGE-PRODUTO-",
        visible=False
    )
