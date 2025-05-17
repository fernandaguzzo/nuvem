Visão Geral

Este projeto implementa uma arquitetura de microsserviços para o sistema de clínicas Vida+ Saúde, substituindo a abordagem monolítica anterior. O sistema é composto por serviços independentes que se comunicam via APIs RESTful, permitindo melhor escalabilidade e manutenibilidade. </br>
Serviços Implementados:

1. Paciente (:5001)

    Responsabilidade: Gerenciamento de cadastro de pacientes

    Endpoints:

        POST /pacientes - Cadastra um novo paciente

        GET /pacientes/<id> - Busca paciente por ID

2. Consulta (:5003)

    Responsabilidade: Agendamento e gestão de consultas médicas

    Endpoints:

        POST /consultas - Agenda nova consulta 

        GET /consultas - Lista todas as consultas

        GET /consultas/<id> - Obtém consulta específica

        GET /consultas/paciente/<id> - Lista consultas por paciente

3. Prontuário (:5002)

    Responsabilidade: Armazenamento de registros médicos

    Endpoints:

        POST /prontuarios - Cria novo prontuário 

        GET /prontuarios - Lista todos os prontuários

        GET /prontuarios/<id> - Obtém prontuário específico

        GET /prontuarios/paciente/<id> - Lista prontuários por paciente

4. Faturamento (:5004)

    Responsabilidade: Geração de faturas para consultas

    Endpoints:

        POST /faturas - Gera nova fatura 

        GET /faturas - Lista todas as faturas

        GET /faturas/<id> - Obtém fatura específica

5. Plano de Saúde (:5005)

    Responsabilidade: Simulação de sistema externo de planos de saúde

    Endpoints:

        POST /validar-procedimento - Valida cobertura de procedimento

Integrações
Integração Horizontal (entre serviços internos)

    Consulta → Paciente: Verifica existência do paciente ao agendar consulta

    Prontuário → Paciente: Obtém dados do paciente ao criar prontuário

    Faturamento → Consulta: Obtém dados da consulta para gerar fatura

Integração Vertical (com serviço externo)

    Faturamento → Plano de Saúde: Verifica cobertura de procedimentos

Tecnologias Utilizadas

    Python 3

    Flask 

    Requests 

    Docker 
