# SPEC: hadnu.github.io — Personal Site

**Target URL:** https://had-nu.github.io/  
**Repositório:** `had-nu/had-nu.github.io`  
**Autor:** André Ataíde  
**Versão da spec:** 1.0  

---

## 1. Objectivo

Site pessoal estático que serve como ponto de entrada público para:
- Identidade profissional (IT Risk / GRC / Security Engineering)
- Portfolio de projectos open-source
- Publicações académicas
- Writing (blog)

O site deve funcionar como cartão de visita técnico: quem chega do LinkedIn, de um perfil GitHub, ou de uma referência ao whitepaper deve encontrar contexto suficiente em 30 segundos.

---

## 2. Stack técnica

**HTML/CSS/JS puro. Zero dependências externas em runtime.**

Justificação para o agente:
- GitHub Pages serve ficheiros estáticos directamente — sem pipeline de build necessário
- Zero dependências significa zero pontos de falha, zero actualizações de manutenção
- Fonts via Google Fonts CDN é a única excepção permitida
- Sem frameworks (React, Vue, Next.js), sem Jekyll, sem Hugo
- Sem npm, sem package.json, sem node_modules

### Estrutura de ficheiros

```
hadnu.github.io/
├── index.html          ← página principal (single page)
├── css/
│   └── style.css       ← todos os estilos
├── js/
│   └── main.js         ← comportamento mínimo (nav mobile, tema)
└── writing/
    └── index.html      ← lista de posts (inicialmente vazia com placeholder)
```

O blog (`/writing/`) é uma página separada, não um sistema de posts. Cada post futuro será um ficheiro HTML individual em `writing/YYYY-MM-titulo.html`. A spec do agente não precisa de gerar posts — apenas a página de índice com estado vazio.

---

## 3. Secções — `index.html`

A página principal é **single page com scroll**. Navegação ancora para cada secção.

### 3.1 Header / Nav

```
[André Ataíde]                    [about] [projects] [publications] [writing]
```

- Logo: nome em texto, tipografia display
- Links: âncoras internas (`#about`, `#projects`, `#publications`) + link externo para `/writing/`
- Sticky no topo ao scroll
- Mobile: hamburger colapsável

### 3.2 Hero

Sem imagem. Apenas texto.

```
André Ataíde

IT Risk · Security Engineering · Open Source

Portugal
```

- Nome em tipografia display grande
- Tagline em tipografia mono, tamanho médio
- Localização em tipografia corpo, small
- Links sociais em linha: [GitHub] [LinkedIn] [arXiv] — ícones SVG inline ou texto simples

**Conteúdo real a usar:**
- GitHub: `https://github.com/had-nu`
- LinkedIn: preencher com URL real (placeholder: `#`)
- arXiv: preencher quando paper for submetido (placeholder: `#`)

### 3.3 About

```html
<!-- id="about" -->
```

Parágrafo curto. Tom: directo, sem retórica de "apaixonado por".

**Texto sugerido (o agente deve usar este texto):**

> I work at the intersection of IT Risk, GRC, and security engineering. My focus is on making security decisions traceable — connecting detection output, compliance controls, and release gates into systems that produce audit evidence, not just alerts.
>
> I build open-source tooling in Go that operationalises these ideas: entropy-based secret detection, risk-driven release gates, and the supporting infrastructure between them.

### 3.4 Projects

```html
<!-- id="projects" -->
```

**Layout:** grade de cards. 3 colunas em desktop, 1 em mobile.

Cada card contém:
- Nome do projecto (link para repositório GitHub)
- Tagline de uma linha
- Stack em tags pequenas
- Badge de status (active / stable / research)

**Projectos a listar:**

| Nome | Tagline | Stack | Status | URL |
|------|---------|-------|--------|-----|
| Vexil | Shannon entropy secret detection for air-gapped environments | Go | active | https://github.com/had-nu/vexil |
| Wardex | Risk-driven release gate engine | Go | active | https://github.com/had-nu/wardex |
| lazy.go | Go project scaffolding tool | Go | stable | https://github.com/had-nu/lazy.go |
| Prana Network | Distributed reputation-based blockchain protocol | Go | research | https://github.com/had-nu/prana |

### 3.5 Publications

```html
<!-- id="publications" -->
```

**Layout:** lista vertical, uma entrada por publicação.

Cada entrada:
- Título (link para arXiv ou PDF)
- Autores
- Venue / status
- Ano
- Abstract de duas linhas (truncado)

**Publicação a listar:**

```
Beyond Entropy Thresholds: Formalising the Scope Limitation of
Entropy-Based Secret Detection and a Bifurcated Classifier Model

André Ataíde
arXiv preprint · cs.CR · 2025
[arXiv link — placeholder até submissão]

Formalises the scope boundary of Shannon entropy as a secret
discriminator, introducing a token_class / credential_class
bifurcation and a composite classifier for air-gapped environments.
```

Se não houver publicações submetidas ainda, a secção aparece com estado vazio explícito:

```
No publications yet. Preprint forthcoming.
```

### 3.6 Footer

```
© André Ataíde · hadnu.github.io · Built with HTML/CSS
[GitHub] [LinkedIn]
```

---

## 4. Identidade visual

**Tema:** minimalista escuro. Sem efeitos holográficos, sem gradientes pesados, sem glitch.

### 4.1 Paleta

```css
:root {
  --bg:           #0d0d0d;   /* fundo principal */
  --surface:      #141414;   /* cards, nav */
  --border:       #222222;   /* bordas subtis */
  --text-primary: #e8e8e8;   /* corpo de texto */
  --text-muted:   #666666;   /* labels, metadata */
  --accent:       #e8e8e8;   /* accent neutro — sem cor */
  --accent-warm:  #c8b89a;   /* detalhe quente opcional — tipografia display */
}
```

Sem azuis, sem cianos, sem magentas. O portfolio de projectos já usa esses tons — o site pessoal é deliberadamente neutro para contrastar.

### 4.2 Tipografia

```css
/* Display / headings grandes */
font-family: 'DM Serif Display', serif;

/* Corpo de texto */
font-family: 'DM Sans', sans-serif;

/* Código, tags, metadata técnica */
font-family: 'JetBrains Mono', monospace;
```

Google Fonts CDN:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500&family=JetBrains+Mono:wght@300;400&display=swap" rel="stylesheet">
```

### 4.3 Escala tipográfica

```css
--text-xs:   0.75rem;   /* tags, badges */
--text-sm:   0.875rem;  /* metadata, footer */
--text-base: 1rem;      /* corpo */
--text-lg:   1.25rem;   /* subtítulos */
--text-xl:   1.5rem;    /* títulos de secção */
--text-2xl:  2rem;      /* hero tagline */
--text-4xl:  3.5rem;    /* nome no hero */
--text-6xl:  5.5rem;    /* nome em desktop grande */
```

### 4.4 Espaçamento e layout

- Max-width do conteúdo: `760px`
- Padding horizontal mobile: `1.5rem`
- Secções separadas por `padding-top: 6rem`
- Sem bordas arredondadas excessivas — `border-radius: 2px` no máximo nos cards
- Bordas dos cards: `1px solid var(--border)` — sem sombras

### 4.5 Animações

Apenas uma: fade-in suave no load do hero.

```css
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

Sem scroll animations, sem parallax, sem hover effects elaborados. Hover nos links: `color` transition `150ms ease`.

---

## 5. SEO e meta

```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>André Ataíde — IT Risk & Security Engineering</title>
<meta name="description" content="IT Risk, GRC, and security engineering. Open-source tooling in Go: Vexil, Wardex.">
<meta name="author" content="André Ataíde">

<!-- Open Graph (LinkedIn preview) -->
<meta property="og:title" content="André Ataíde">
<meta property="og:description" content="IT Risk · Security Engineering · Open Source">
<meta property="og:url" content="https://hadnu.github.io">
<meta property="og:type" content="website">
```

Sem analytics por defeito. Se adicionar no futuro: Plausible (privacy-first) ou nada.

---

## 6. Writing — `/writing/index.html`

Página separada com a mesma navegação e estilos.

**Estado inicial (sem posts):**

```
Writing

No posts yet.
```

**Estrutura futura quando houver posts:**

```
Writing

2025

  Mar  On EPSS, CVSS, and Deployment Context
       How to read vulnerability scores without context anxiety.

  ...
```

Cada entrada: data + título (link) + subtítulo de uma linha. Sem excerpts, sem thumbnails, sem categorias.

---

## 7. Instruções para o agente

O agente deve gerar os seguintes ficheiros prontos a fazer push para o repositório `hadnu/hadnu.github.io`:

1. `index.html` — página completa com todas as secções, HTML semântico, sem inline styles
2. `css/style.css` — todos os estilos, usando as variáveis CSS definidas nesta spec
3. `js/main.js` — apenas: toggle do menu mobile + smooth scroll para âncoras
4. `writing/index.html` — página de índice de posts em estado vazio

**Validações que o agente deve verificar antes de entregar:**

- [ ] HTML passa validação W3C (sem erros de estrutura)
- [ ] Sem dependências externas além das Google Fonts
- [ ] Sem `<style>` inline nos elementos HTML
- [ ] Links placeholder marcados com `href="#"` e `data-todo="true"` para fácil localização
- [ ] Ficheiro `writing/index.html` usa o mesmo `style.css` com path relativo `../css/style.css`
- [ ] Nav mobile funciona sem JavaScript desactivado (graceful degradation: menu sempre visível em CSS quando JS falha)
- [ ] `<meta viewport>` presente
- [ ] Nenhum `console.log` no JS de produção

**O que o agente NÃO deve fazer:**

- Não adicionar Jekyll (`_config.yml`, `Gemfile`)
- Não criar `package.json` ou qualquer ficheiro de build
- Não usar Bootstrap, Tailwind, ou qualquer CSS framework
- Não adicionar animações além das especificadas
- Não inventar projectos ou publicações além dos listados
- Não adicionar secção de contacto com formulário (não há backend)

---

## 8. Deploy

O repositório `hadnu/hadnu.github.io` já existe. Após geração dos ficheiros:

```bash
git clone https://github.com/hadnu/hadnu.github.io
# copiar ficheiros gerados para a raiz
git add .
git commit -m "feat: initial site — about, projects, publications, writing"
git push origin main
```

GitHub Pages detecta automaticamente o `index.html` na raiz do branch `main` e publica em `https://hadnu.github.io` em 1–2 minutos.

Não é necessário configurar nada no repositório se Pages já estiver activado. Se não estiver: Settings → Pages → Source → "Deploy from branch" → `main` → `/ (root)`.
