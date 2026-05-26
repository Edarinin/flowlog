import PySimpleGUI as sg

def configuracoes_page():
    options = [
        ["Notificações", "Ativas"],
        ["Backup automático", "Diário"],
        ["Idioma", "PT-BR"],
        ["Fuso horário", "America/Sao_Paulo"],
    ]
    
    integrations = [
        ["Email", "Conectado"],
        ["ERP", "Pendente"],
        ["Planilhas", "Conectado"],
    ]

    layout = [
        [sg.Text("Configurações", font=("Arial", 24, "bold"), text_color="white")],
        [sg.Text("Preferências do sistema e integrações", font=("Arial", 10), text_color="#AAB4C3")],
        [sg.HorizontalSeparator(color="#2A3546")],
        
        # Tabela de Perfil/Geral
        [sg.Frame("Perfil e Preferências", [
            [sg.Table(values=options, headings=["Opção", "Status"], auto_size_columns=True,
                      num_rows=4, background_color="#0F172A", text_color="#E5E7EB",
                      header_background_color="#1F2937", border_width=0, expand_x=True)]
        ], background_color="#18212E", border_width=0, expand_x=True, pad=(0, 20))],
        
        # Segurança
        [sg.Frame("Segurança", [
            [sg.Text("Senha expira em 25 dias", text_color="#B8C2CE")],
            [sg.Button("Trocar senha", button_color=("white", "#2D6CDF"), border_width=0),
             sg.Button("Sair de todos os dispositivos", button_color=("white", "#3A4656"), border_width=0)]
        ], background_color="#18212E", border_width=0, expand_x=True, pad=(0, 20))],

        # Integrações
        [sg.Frame("Integrações Externas", [
            [sg.Table(values=integrations, headings=["Serviço", "Status"], auto_size_columns=True,
                      num_rows=3, background_color="#0F172A", text_color="#E5E7EB",
                      header_background_color="#1F2937", border_width=0, expand_x=True)],
            [sg.Button("Conectar Novo", button_color=("white", "#2D6CDF"), border_width=0),
             sg.Button("Gerenciar", button_color=("white", "#3A4656"), border_width=0)]
        ], background_color="#18212E", border_width=0, expand_x=True)]
    ]
    
    return sg.Column(layout, background_color="#111827", expand_x=True, expand_y=True, 
                     key="-PAGE-SCHEDULE-", visible=False)