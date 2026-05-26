# paginas/registros.py
import PySimpleGUI as sg
from data_manager import (
    card,
    products_count,
    suppliers_count,
    suppliers_rows,
    users_count,
    users_rows,
)

def registros_page():
    layout = [
        [sg.Text("Cadastros", font=("Arial", 24, "bold"), text_color="white")],
        [sg.Text("Adicione e gerencie fornecedores e usuários com uma interface mais clara.", font=("Arial", 11), text_color="#AAB4C3")],
        [sg.HorizontalSeparator(color="#2A3546", pad=(0, 10))],

        [
            card("Produtos", products_count(), "Cadastrados", "-CAD-PROD-COUNT-"),
            card("Fornecedores", suppliers_count(), "Cadastrados", "-CAD-SUPPLIERS-COUNT-"),
            card("Funcionarios", users_count(), "Com acesso", "-CAD-USERS-COUNT-")
        ],

        [
            sg.Column([
                [sg.Frame("Fornecedores", [
                    [
                        sg.Button("Adicionar", key="-SUPPLIER-ADD-", button_color=("white", "#0F4C81"), border_width=0, size=(12, 1), pad=(0, 8)),
                        sg.Button("Atualizar", key="-SUPPLIER-UPDATE-", button_color=("white", "#0F7381"), border_width=0, size=(12, 1), pad=(0, 8)),
                        sg.Button("Remover", key="-SUPPLIER-DELETE-", button_color=("white", "#6B7280"), border_width=0, size=(12, 1))
                    ],
                    [sg.Text("", pad=(0, 8))],
                    [
                        sg.Table(
                            values=suppliers_rows(),
                            headings=["Codigo", "Fornecedor", "Email"],
                            key="-SUPPLIERS-TABLE-",
                            enable_events=True,
                            num_rows=7,
                            auto_size_columns=True,
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
            ], expand_x=True, vertical_alignment="top"),

            sg.Column([
                [sg.Frame("Funcionarios", [
                    [
                        sg.Button("Adicionar", key="-USER-ADD-", button_color=("white", "#0F4C81"), border_width=0, size=(12, 1), pad=(0, 8)),
                        sg.Button("Atualizar", key="-USER-UPDATE-", button_color=("white", "#0F7381"), border_width=0, size=(12, 1), pad=(0, 8)),
                        sg.Button("Remover", key="-USER-DELETE-", button_color=("white", "#6B7280"), border_width=0, size=(12, 1))
                    ],
                    [sg.Text("", pad=(0, 8))],
                    [
                        sg.Table(
                            values=users_rows(),
                            headings=["Codigo", "Nome", "Perfil"],
                            key="-USERS-TABLE-",
                            enable_events=True,
                            num_rows=7,
                            auto_size_columns=True,
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
            ], expand_x=True, vertical_alignment="top")
        ]
    ]

    return sg.Column(
        layout,
        background_color="#111827",
        expand_x=True,
        expand_y=True,
        key="-PAGE-CAD-",
        visible=False
    )
