import PySimpleGUI as sg
import data_manager


def inicio_page():
    activities = data_manager.get_recent_activities()
    alerts = data_manager.important_alerts()
    movements = data_manager.latest_movements_rows()

    layout = [
        [
            sg.Text("Dashboard", font=("Arial", 24, "bold"), text_color="white", background_color="#111827"),
            sg.Push(background_color="#111827"),
            sg.Text("Painel do projeto", font=("Arial", 10), text_color="#AAB4C3", background_color="#111827")
        ],
        [sg.HorizontalSeparator(color="#1F2937")],

        [
            data_manager.card("Produtos", data_manager.products_count(), "Itens no estoque", "-HOME-PROD-COUNT-"),
            data_manager.card("Entradas 7 dias", data_manager.movement_totals()["entradas"], "Total entradas", "-HOME-ENTR-COUNT-"),
            data_manager.card("Saídas 7 dias", data_manager.movement_totals()["saidas"], "Total saídas", "-HOME-SAID-COUNT-"),
            data_manager.card("Saldo 7 dias", data_manager.movement_totals()["saldo"], "Fluxo líquido", "-HOME-SALDO-COUNT-"),
            data_manager.card("Movimentações", data_manager.recent_movements_count(), "Últimas ações", "-HOME-MOV-COUNT-")
        ],

        [
            sg.Column([
                [
                    sg.Frame(
                        "Movimentações (Últimos 7 dias)",
                        [
                            [sg.Text("Entradas e saídas de produtos", font=("Arial", 11), text_color="#E5E7EB", background_color="#1F2937")],
                            [sg.Text("Visualização:", font=("Arial", 9), text_color="#94A3B8", background_color="#1F2937"),
                             sg.Combo(["Linhas", "Barras", "Área"], default_value="Linhas", key="-HOME-CHART-TYPE-", readonly=True, enable_events=True, size=(12, 1), background_color="#0F172A", text_color="#FFFFFF"),
                             sg.Text("Intervalo:", font=("Arial", 9), text_color="#94A3B8", background_color="#1F2937", pad=((15, 0), 0)),
                             sg.Combo(["7 dias", "14 dias", "30 dias"], default_value="7 dias", key="-HOME-CHART-RANGE-", readonly=True, enable_events=True, size=(10, 1), background_color="#0F172A", text_color="#FFFFFF")],
                            [
                                sg.Graph(
                                    canvas_size=(560, 260),
                                    graph_bottom_left=(0, 0),
                                    graph_top_right=(560, 260),
                                    background_color="#111827",
                                    key="-HOME-CHART-",
                                    pad=(0, 0),
                                )
                            ],
                        ],
                        background_color="#1F2937",
                        relief=sg.RELIEF_FLAT,
                        pad=(0, 0),
                        border_width=0,
                        expand_x=True,
                    )
                ]
            ], background_color="#111827", expand_x=True, pad=(0, 0)),

            sg.Column([
                [
                    sg.Frame(
                        "Alertas importantes",
                        [
                            [sg.Text(alerts[0]["title"], font=("Arial", 11, "bold"), text_color=alerts[0]["color"], background_color="#111827", key="-ALERT-1-TITLE-")],
                            [sg.Text(alerts[0]["subtitle"], font=("Arial", 9), text_color="#D1D5DB", background_color="#111827", key="-ALERT-1-SUB-")],
                            [sg.HorizontalSeparator(color="#334155", pad=(0, 4))],  # ← era (0, 8)
                            [sg.Text(alerts[1]["title"], font=("Arial", 11, "bold"), text_color=alerts[1]["color"], background_color="#111827", key="-ALERT-2-TITLE-")],
                            [sg.Text(alerts[1]["subtitle"], font=("Arial", 9), text_color="#D1D5DB", background_color="#111827", key="-ALERT-2-SUB-")],
                            [sg.HorizontalSeparator(color="#334155", pad=(0, 4))],  # ← era (0, 8)
                            [sg.Text(alerts[2]["title"], font=("Arial", 11, "bold"), text_color=alerts[2]["color"], background_color="#111827", key="-ALERT-3-TITLE-")],
                            [sg.Text(alerts[2]["subtitle"], font=("Arial", 9), text_color="#D1D5DB", background_color="#111827", key="-ALERT-3-SUB-")]
                        ],
                        background_color="#111827",
                        relief=sg.RELIEF_RIDGE,
                        pad=(10, 5),   # ← era (10, 10)
                        border_width=1,
                        expand_x=True,
                    )
                ],
                [
                    sg.Frame(
                        "Relatório",
                        [
                            [sg.Text("Baixe um relatório CSV com resumo\nde movimentações e saldo.", font=("Arial", 9), text_color="#D1D5DB", background_color="#111827", size=(30, 2))],
                            [sg.Button("Download Relatório", key="-HOME-REPORT-DOWNLOAD-", button_color=("white", "#0F4C81"), border_width=0, size=(14, 1), pad=(0, 6))],
                            [sg.Text("", key="-HOME-REPORT-PATH-", font=("Arial", 8), text_color="#94A3B8", background_color="#111827", size=(28, 1))]
                        ],
                        background_color="#111827",
                        relief=sg.RELIEF_RIDGE,
                        pad=(10, 5),   # ← era (10, 0)
                        border_width=1,
                        expand_x=True,
                    )
                ]
            ], background_color="#111827", pad=(10, 0), vertical_alignment="top"),
        ],

        [
            sg.Frame(
                "Cadastros Recentes",
                [
                    [
                        sg.Table(
                            values=activities,
                            headings=["Status", "Tipo", "Nome", "Obs"],
                            auto_size_columns=True,
                            num_rows=6,
                            row_height=24,
                            background_color="#0F172A",
                            text_color="#E5E7EB",
                            header_background_color="#1F2937",
                            header_text_color="white",
                            justification="left",
                            expand_x=True,
                            border_width=0,
                            key="-TABLE-RECENTES-"
                        )
                    ]
                ],
                background_color="#1F2937",
                border_width=0,
                expand_x=True,
                pad=(0, 0)
            ),
            sg.Frame(
                "Últimas Movimentações",
                [
                    [
                        sg.Table(
                            values=movements,
                            headings=["Data/Hora", "Tipo", "Descrição", "Usuário"],
                            auto_size_columns=True,
                            num_rows=6,
                            row_height=24,
                            background_color="#0F172A",
                            text_color="#E5E7EB",
                            header_background_color="#1F2937",
                            header_text_color="white",
                            justification="left",
                            expand_x=True,
                            border_width=0,
                            key="-TABLE-MOVIMENTOS-"
                        )
                    ]
                ],
                background_color="#1F2937",
                border_width=0,
                expand_x=True,
                pad=(10, 0)
            )
        ]
    ]

    return sg.Column(layout, background_color="#111827", expand_x=True, expand_y=True, key="-PAGE-HOME-", visible=True)
