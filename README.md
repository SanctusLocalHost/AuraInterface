# Aura Interface

Controle seu computador através de gestos com a mão, utilizando apenas uma webcam. Este projeto transforma seus movimentos em ações de mouse, como mover, clicar, arrastar e dar zoom, com foco em uma operação discreta e de alta performance.

---

### Funcionalidades

*   **Controle Total do Mouse:** Mover, Clicar e Arrastar com gestos intuitivos.
*   **Zoom Inteligente:** Aproxime ou afaste as duas mãos para controlar o zoom de forma fluida.
*   **Operação Discreta:** O programa roda em segundo plano. A janela da câmera é opcional e pode ser exibida ou escondida a qualquer momento através do terminal.
*   **Alta Performance:** Resposta rápida e suave do cursor, com filtros para evitar tremores e falsos positivos.

### Tecnologias Utilizadas

*   Python
*   OpenCV
*   MediaPipe
*   PyAutoGUI

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/aura-interface.git
    cd aura-interface
    ```

2.  **Instale as dependências com um único comando:**
    ```bash
    pip install opencv-python mediapipe numpy pyautogui
    ```

### Como Usar

1.  **Execute o script principal pelo terminal:**
    ```bash
    python seu_script.pyw
    ```
    O controle por gestos já estará ativo em segundo plano.

2.  **Use o terminal para controlar o programa:**
    *   `c` + `Enter`: **Mostrar / Esconder** a janela da câmera.
    *   `q` + `Enter`: **Encerrar** o programa.

### Tabela de Gestos

| Ação | Gesto | Detalhes |
| :--- | :--- | :--- |
| **Mover Cursor** | ✌️ (Indicador e Médio) | O cursor se move de forma relativa (estilo trackpad). |
| **Clicar** | 🤘 (Indicador, Médio e Mindinho) | Segure o gesto por **0.5 segundos** para confirmar. |
| **Arrastar** | 👍+✌️ (Polegar, Indicador e Médio) | Segure o gesto por **0.5 segundos** para ativar o arraste. |
| **Zoom In/Out** | ✌️ com as **duas mãos** | Aproxime ou afaste as mãos (uma esquerda e uma direita). |
