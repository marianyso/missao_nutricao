
import pygame
import sys
import random
import math

pygame.init()

LARGURA = 800
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Missão Nutrição 💚")
RELOGIO = pygame.time.Clock()


COR_SAUDAVEL = (100, 220, 100)
COR_SAUDAVEL_BORDA = (40, 180, 40)
COR_NAO_SAUDAVEL = (240, 120, 120)
COR_NAO_SAUDAVEL_BORDA = (180, 40, 40)

COR_JOGADOR = (64, 150, 230)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
COR_ROSTO = (255, 255, 200) # Amarelo claro para o rosto

FUNDO_FASE_1 = (250, 252, 255)  # Azul claro
FUNDO_FASE_2 = (255, 250, 240)  # Creme
FUNDO_FASE_3 = (255, 249, 240)  # Creme

try:
    FONTE_TITULO = pygame.font.SysFont("Segoe UI", 28, bold=True)
    FONTE_UI = pygame.font.SysFont("Segoe UI", 22)
except:
    FONTE_TITULO = pygame.font.SysFont("Arial", 28, bold=True)
    FONTE_UI = pygame.font.SysFont("Arial", 22)

PARTICULAS = []

def adicionar_particulas(x, y, cor):
    """Adiciona partículas para um efeito visual de coleta/colisão."""
    for _ in range(8):
        PARTICULAS.append({
            'x': x,
            'y': y,
            'vx': random.uniform(-2, 2),
            'vy': random.uniform(-2.5, -0.5),
            'cor': cor,
            'vida': 20
        })

def desenhar_fundo(tela, cor):
    """Preenche a tela com a cor de fundo da fase."""
    tela.fill(cor)

class Jogador:
    """Representa o personagem controlável pelo jogador."""
    def __init__(self):
        self.x = 100
        self.y = ALTURA - 120
        self.raio = 35

    def mover(self, teclas):
        """Atualiza a posição do jogador com base nas teclas pressionadas."""
        velocidade = 5
        if teclas[pygame.K_LEFT] and self.x > self.raio:
            self.x -= velocidade
        if teclas[pygame.K_RIGHT] and self.x < LARGURA - self.raio:
            self.x += velocidade
        if teclas[pygame.K_UP] and self.y > self.raio:
            self.y -= velocidade
        if teclas[pygame.K_DOWN] and self.y < ALTURA - self.raio:
            self.y += velocidade

    def desenhar(self, tela):
        """Desenha o jogador na tela com um rosto amigável."""
    
        pygame.draw.circle(tela, COR_JOGADOR, (self.x, self.y), self.raio)
        pygame.draw.circle(tela, (40, 100, 180), (self.x, self.y), self.raio, 3) # Borda do jogador
        
        olho_esq = (self.x - 10, self.y - 8)
        olho_dir = (self.x + 10, self.y - 8)
        
        pygame.draw.circle(tela, BRANCO, olho_esq, 8) # Esclera (parte branca)
        pygame.draw.circle(tela, BRANCO, olho_dir, 8) # Esclera (parte branca)
        pygame.draw.circle(tela, PRETO, olho_esq, 4) # Pupila
        pygame.draw.circle(tela, PRETO, olho_dir, 4) # Pupila
        
        # Sorriso
        pygame.draw.arc(tela, PRETO, (self.x - 15, self.y, 30, 20), 0, math.pi, 2) # Sorriso

    def get_rect(self):
        """Retorna o retângulo de colisão do jogador."""
        return pygame.Rect(self.x - self.raio, self.y - self.raio, self.raio * 2, self.raio * 2)

class Alimento:
    """Representa um item de alimento que cai na tela."""
    def __init__(self, tipo, x, y):
        self.tipo = tipo  
        self.x = x
        self.y = y
        
        self.vel_y = random.uniform(1.5, 3.0) if tipo == "bom" else random.uniform(1.0, 2.5)
        self.tamanho = 60
        self.raio_borda = 15

    def mover(self):
        """Atualiza a posição do alimento, fazendo-o cair e reaparecer no topo."""
        self.y += self.vel_y
        if self.y > ALTURA + 50:
            self.y = random.randint(-100, -40)
            self.x = random.randint(50, LARGURA - 50)

    def desenhar(self, tela):
        """Desenha o alimento na tela com cores e expressões faciais diferentes."""
        x_rect, y_rect = self.x - self.tamanho // 2, self.y - self.tamanho // 2
        
        cor_principal = COR_SAUDAVEL if self.tipo == "bom" else COR_NAO_SAUDAVEL
        cor_borda = COR_SAUDAVEL_BORDA if self.tipo == "bom" else COR_NAO_SAUDAVEL_BORDA
        
        # Desenha o corpo do alimento (quadrado arredondado)
        pygame.draw.rect(tela, cor_principal, (x_rect, y_rect, self.tamanho, self.tamanho), border_radius=self.raio_borda)
        pygame.draw.rect(tela, cor_borda, (x_rect, y_rect, self.tamanho, self.tamanho), 4, border_radius=self.raio_borda)
        
        # Desenha a expressão facial
        cor_rosto = COR_ROSTO
        
        # Olhos
        olho_esq = (self.x - 10, self.y - 8)
        olho_dir = (self.x + 10, self.y - 8)
        pygame.draw.circle(tela, cor_rosto, olho_esq, 8) # Olho esquerdo
        pygame.draw.circle(tela, cor_rosto, olho_dir, 8) # Olho direito
        
        # Boca (Feliz para "bom", Triste para "ruim")
        if self.tipo == "bom":
            # Sorriso
            pygame.draw.arc(tela, cor_rosto, (self.x - 15, self.y - 3, 30, 20), 0, math.pi, 3) # Sorriso feliz
        else:
            # Triste
            pygame.draw.arc(tela, cor_rosto, (self.x - 15, self.y + 5, 30, 20), math.pi, 2 * math.pi, 3) # Sorriso triste (boca para baixo)

    def get_rect(self):
        """Retorna o retângulo de colisão do alimento."""
        # O retângulo de colisão é ligeiramente menor que o tamanho total para melhor jogabilidade
        return pygame.Rect(self.x - 30, self.y - 30, 60, 60)

def handle_collisions(jogador, alimentos, pontos, fase, LARGURA):
    """Verifica e processa colisões entre o jogador e os alimentos."""
    jogador_rect = jogador.get_rect()
    
    for alim in alimentos[:]:
        if jogador_rect.colliderect(alim.get_rect()):
            alimentos.remove(alim)
            
            if alim.tipo == "bom":
                pontos += 1
                adicionar_particulas(alim.x, alim.y, COR_SAUDAVEL)
                if fase == 1:
                    # Na fase 1, substitui o alimento coletado por um novo estático
                    alimentos.append(Alimento("bom", random.randint(80, LARGURA - 80), random.randint(50, 200)))
            else:
                pontos = max(0, pontos - 1)
                adicionar_particulas(alim.x, alim.y, COR_NAO_SAUDAVEL)
                if fase == 1:
                    # Na fase 1, substitui o alimento coletado por um novo estático
                    alimentos.append(Alimento("ruim", random.randint(80, LARGURA - 80), random.randint(50, 200)))
                    
    return pontos

def handle_phase_transition(fase, pontos, meta, alimentos, jogador, PARTICULAS, start_time):
    """Verifica e executa a transição entre as fases do jogo."""
    if fase == 1 and pontos >= meta:
        fase = 2
        pontos = 0
        alimentos = gerar_fase_2()
        meta = 10
    elif fase == 2 and pontos >= meta:
        fase = 3
        pontos = 0
        jogador = Jogador()
        alimentos = []
        PARTICULAS.clear()
        start_time = pygame.time.get_ticks()
        
    return fase, pontos, meta, alimentos, jogador, start_time

def draw_ui(tela, fase, pontos, tempo_restante, LARGURA, FONTE_UI):
    """Desenha a interface do usuário (fase, pontos e timer) na tela."""
    
    pygame.draw.rect(tela, (0, 0, 0, 180), (10, 10, 260, 36), border_radius=10)
    pygame.draw.rect(tela, BRANCO, (12, 12, 256, 32), border_radius=10)
    
    # Texto da UI
    texto = FONTE_UI.render(f"Fase {fase} • Pontos: {pontos}", True, (40, 40, 40))
    tela.blit(texto, (20, 16))

    # Timer (só fase 3)
    if fase == 3:
        # Fundo do Timer
        pygame.draw.rect(tela, (0, 0, 0, 180), (LARGURA - 150, 10, 140, 36), border_radius=10)
        pygame.draw.rect(tela, BRANCO, (LARGURA - 148, 12, 136, 32), border_radius=10)
        
        # Texto do Timer
        tempo_txt = FONTE_UI.render(f"⏳ {tempo_restante}s", True, (50, 50, 150))
        tela.blit(tempo_txt, (LARGURA - 140, 16))



def gerar_fase_1():
    """Gera a lista inicial de alimentos para a Fase 1 (itens estáticos)."""
    return [
        Alimento("bom", 200, 100),
        Alimento("bom", 400, 150),
        Alimento("bom", 600, 200),
        Alimento("bom", 300, 250),
        Alimento("ruim", 500, 120),
    ]

def gerar_fase_2():
    """Gera a lista inicial de alimentos para a Fase 2 (itens caindo)."""
    lista = []
    # 12 alimentos saudáveis (verdes)
    for _ in range(12):
        lista.append(Alimento("bom", random.randint(60, LARGURA - 60), random.randint(-300, -50)))
    # 3 alimentos ruins (vermelhos)
    for _ in range(6):
        lista.append(Alimento("ruim", random.randint(60, LARGURA - 60), random.randint(-400, -100)))
    return lista

fase = 1
pontos = 0
meta = 6
tempo_fase3 = 25
start_time = pygame.time.get_ticks()

jogador = Jogador()
alimentos = gerar_fase_1()

rodando = True
while rodando:
    tempo_atual = pygame.time.get_ticks()
    teclas = pygame.key.get_pressed()

    # --- 5.1. Tratamento de Eventos ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # --- 5.2. Atualização de Estado ---
    jogador.mover(teclas)

    if fase >= 2:
        for alim in alimentos:
            alim.mover()

    # Colisões
    pontos = handle_collisions(jogador, alimentos, pontos, fase, LARGURA)

    
    fase, pontos, meta, alimentos, jogador, start_time = handle_phase_transition(fase, pontos, meta, alimentos, jogador, PARTICULAS, start_time)

    # Lógica da Fase 3 (Modo Sobrevivência/Tempo)
    tempo_restante = tempo_fase3
    if fase == 3:
        if random.randint(1, 20) == 1:
            tipo = "bom" if random.random() < 0.75 else "ruim"
            alimentos.append(Alimento(tipo, random.randint(60, LARGURA - 60), -40))
        
        for alim in alimentos[:]:
            if alim.y > ALTURA + 50:
                alimentos.remove(alim)

        tempo_passado = (tempo_atual - start_time) // 1000
        tempo_restante = max(0, tempo_fase3 - tempo_passado)

        # Condições de Fim de Jogo
        if pontos >= 20:
            desenhar_fundo(TELA, (200, 255, 200)) # Fundo verde de vitória
            msg = FONTE_TITULO.render("VOCÊ VENCEU! Alimentação SAUDÁVEL! ", True, (0, 120, 0))
            TELA.blit(msg, (LARGURA // 2 - msg.get_width() // 2, ALTURA // 2 - 20))
            pygame.display.flip()
            pygame.time.delay(3000)
            rodando = False
        elif tempo_restante <= 0:
            desenhar_fundo(TELA, (255, 220, 220)) # Fundo vermelho de derrota
            msg = FONTE_TITULO.render(" Tempo esgotado! Tente novamente.", True, (180, 0, 0))
            TELA.blit(msg, (LARGURA // 2 - msg.get_width() // 2, ALTURA // 2 - 20))
            pygame.display.flip()
            pygame.time.delay(3000)
            rodando = False


    # Desenhar fundo por fase
    if fase == 1:
        desenhar_fundo(TELA, FUNDO_FASE_1)
    elif fase == 2:
        desenhar_fundo(TELA, FUNDO_FASE_2)
    else:
        desenhar_fundo(TELA, FUNDO_FASE_3)

    # Partículas
    for part in PARTICULAS[:]:
        part['x'] += part['vx']
        part['y'] += part['vy']
        part['vida'] -= 1
        
        if part['vida'] > 0:
            raio_particula = max(1, part['vida'] // 4) # Partículas diminuem de tamanho
            pygame.draw.circle(TELA, part['cor'], (int(part['x']), int(part['y'])), raio_particula)
        else:
            PARTICULAS.remove(part)

    # Alimentos e jogador
    for alim in alimentos:
        alim.desenhar(TELA)
    jogador.desenhar(TELA)

    # Interface de fase e pontos (UI)
    draw_ui(TELA, fase, pontos, tempo_restante, LARGURA, FONTE_UI)

    # Atualiza a tela
    pygame.display.flip()
    
    # Limita o FPS
    RELOGIO.tick(60)

pygame.quit()
sys.exit()
