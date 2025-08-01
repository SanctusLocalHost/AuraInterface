# Neuralis Control

Uma interface de controle neural que transforma gestos de mão em comandos precisos no seu computador, utilizando apenas uma webcam. O projeto é focado em alta performance e operação discreta, completo com um feedback visual temático e efeitos sonoros imersivos.

---

### Funcionalidades

*   **Interruptor Mestre:** Ative e desative todo o sistema com um gesto de duas mãos, garantindo que o controle só funcione quando você quiser.
*   **Controle Fino do Mouse:** Mover, Clicar (com confirmação por tempo) e Arrastar (instantâneo) com gestos distintos e feedback visual.
*   **Funções Avançadas de Duas Mãos:** Utilize a "Fenda Espacial" para Zoom e o "Dial Arcano" para rolagem vertical.
*   **Operação Discreta:** Roda silenciosamente no terminal. A janela de visualização é opcional e pode ser ativada para calibrar seus gestos.
*   **Feedback Imersivo:** Efeitos visuais "mágicos" e sons para cada ação principal, criando uma experiência de uso única.
*   **Detecção de Ambiente:** Identifica rostos humanos na cena e os destaca.
*   **Suporte a Múltiplos Monitores:** Navegue livremente por todo o seu desktop virtual sem restrições.

### Tecnologias Utilizadas

*   Python 3.10 (Recomendado)
*   OpenCV
*   MediaPipe
*   PyAutoGUI
*   Pygame (para áudio)

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/neuralis-control.git
    cd neuralis-control
    ```

2.  **Versão do Python:**
    É altamente recomendado o uso do **Python 3.10** para garantir a compatibilidade total com a biblioteca `mediapipe`.

3.  **Instale as dependências com um único comando:**
    ```bash
    pip install opencv-python mediapipe numpy pyautogui pygame
    ```

4.  **Arquivos de Áudio (Opcional):**
    Para o feedback sonoro, converta seus arquivos de som para o formato **`.ogg`** e coloque-os no diretório `G:\Meu Drive\CONTROLLER\DATA CENTER\SOM\` com os seguintes nomes:
    *   `ATIVED_NEURAL_CONTROL.ogg`
    *   `UNATIVED_NEURAL_CONTROL.ogg`
    *   `CLICK_NEURAL_CONTROL.ogg`

### Como Usar

1.  **Execute o script principal pelo terminal:**
    ```bash
    python neuralis_control.pyw
    ```
    O programa iniciará em modo discreto e **desativado**.

2.  **Ative o Sistema:**
    Faça o gesto de **Mãos Abertas** (as duas ao mesmo tempo) e segure por **1 segundo** para ativar o controle.

3.  **Use o terminal para gerenciar o programa:**
    *   `c` + `Enter`: **Mostrar / Esconder** a janela de visualização.
    *   `q` + `Enter`: **Encerrar** o programa.

### Tabela de Gestos (Sistema Ativo)

| Ação | Gesto | Detalhes |
| :--- | :--- | :--- |
| **Ativar/Desativar** | 🖐️🖐️ (Mãos Abertas) | Segure o gesto por **1 segundo** para ligar ou desligar o sistema. |
| **Mover Cursor** | ✌️ (Indicador e Médio) | O cursor se move de forma relativa (estilo trackpad). |
| **Clicar** | 🤘 (Indicador, Médio e Mindinho) | Segure o gesto por **0.5 segundos** para confirmar o clique. |
| **Arrastar** | 👍+✌️ (Polegar, Indicador e Médio) | Ação instantânea. Mude de gesto para soltar. |
| **Zoom ("Fenda Espacial")** | ✌️ com as **duas mãos** | Aproxime ou afaste as mãos (uma esquerda e uma direita). |
| **Rolar ("Dial Arcano")** | 👍+👆 (Polegar e Indicador) | Com as duas mãos, mova a mão mais alta para cima/baixo. |
