# 📄 Relatório de Acompanhamento de Projeto — Sistemas Multiagente

> Preencha com atenção. Este relatório tem o objetivo de **organizar o pensamento, identificar bloqueios e alinhar os próximos passos do seu projeto**.

---

## 🧠 1. Visão Geral do Projeto

- **Título do Projeto**:
  - SmartLux AI

- **Integrantes da Equipe**:  
  - Felipe Braz da Silva

- **Resumo em uma frase**:  
  Sistema de automação para verificação e atualização de documentos organizacionais impactados por normas regulatórias no contexto de distribuidoras de energia elétric

---

## ⚙️ 2. Arquitetura Atual

- **Quantos agentes existem no sistema atualmente?**  
  2 agentes:
 `AgenteAnalistaDocumental`
 `AgenteRedatorTecnico`

- **Função principal de cada agente:**  
  `AgenteAnalistaDocumental`: Receber documento regulatório e buscar trechos relevantes em documentos institucionais contidos em uma base vetorial.
  `AgenteRedatorTecnico`: Redigir as alterações documentais para enquadramento nas mudanças recebidas.

- **Eles interagem entre si? Como?**  
  A ideia é que o agente analista identifique os documentos impactados e repasse para o agente redator para efetuar as alterações necessárias.

- **Já existe algum ambiente de simulação/teste?**  
  Ainda a definir.

---

## ✅ 3. Avanços Concretos
- Entendimento da problemática e levantamento de tecnologias.

---

## 🧱 4. Dificuldades Enfrentadas
- Fase de discussão

---

## 🛠️ 5. Estratégias de Superação


---

## 🎯 6. Próximos Passos

- Decisão sobre as tecnologias que serão utilizadas e primeiros passos de construção do pipeline.

---

## 📢 7. Pedido de Ajuda

- Precisamos de ajuda para definir uma boa estratégia de chunking em documentos jurídicos.
- Também gostaríamos de saber se vale a pena testar outros modelos de embedding (e quais seriam gratuitos e compatíveis).

---
