# Dataset — Gerador de Cartazes para Festas da Terrinha

Dataset de anotações usado no desenvolvimento do [Gerador de Cartazes para
Festas da Terrinha](https://github.com/estevaoabreu/terrinha-posters-generator),
projeto desenvolvido para a unidade curricular de Criatividade Computacional
para Design (Mestrado em Design e Multimédia, FCTUC, 2025/2026).

Este dataset consiste em **56 cartazes reais** de festas e arraiais
populares portugueses, anotados manualmente com [Label Studio](https://labelstud.io/),
identificando a posição e dimensão dos elementos visuais recorrentes em
cada cartaz. Foi usado para gerar um *heatmap* de posições típicas (ver
`heatmap.js` / Processing no repositório principal), que informa o
algoritmo de geração de layout do sistema.

## Estrutura

```
.
├── dataset_cartazes.json   # Export do Label Studio (anotações)
├── images/                 # Imagens originais dos cartazes (Frame_1.png ... Frame_56.png)
├── load_dataset.py         # Script de inspeção/validação do dataset
└── README.md
```

## Categorias anotadas

Cada cartaz foi anotado com retângulos (`rectanglelabels`) identificando
as seguintes regiões:

| Label                         | Descrição                                          |
|--------------------------------|-----------------------------------------------------|
| `Sant@ (Figura)`               | Imagem/escultura do santo padroeiro                |
| `Nome da Terrinha / Santo`     | Título do cartaz (nome da festa/santo)             |
| `Data do Evento`               | Datas da festividade                               |
| `Local`                        | Localidade/freguesia                               |
| `Programação/Horários`         | Bloco(s) de texto com o programa                   |
| `Artista (Imagem)`             | Fotografias de artistas/bandas                     |
| `Patrocínios`                  | Logótipos de patrocinadores                        |

> **Nota técnica:** algumas labels foram exportadas pelo Label Studio com
> caracteres invisíveis (`U+2060`, WORD JOINER) misturados no texto — por
> exemplo, `"⁠⁠⁠Patrocínios"` em vez de `"Patrocínios"`. Isto é um
> artefacto da ferramenta, não um erro de anotação. O script
> `load_dataset.py` inclui uma função `normalize_label()` que remove estes
> caracteres antes de qualquer comparação ou filtragem.

## Formato

O ficheiro `dataset_cartazes.json` segue o formato de export padrão do
Label Studio (lista de *tasks*, cada uma com `data.image`, `annotations`,
e `file_upload`). As coordenadas de cada região (`x`, `y`, `width`,
`height`) estão em **percentagem** relativa às dimensões originais da
imagem (`original_width`, `original_height`), não em pixels absolutos.

## Imagens

As imagens correspondem aos cartazes reais recolhidos via
[Festas & Arraiais](https://festasearraiais.pt/), usados como referência
visual e fonte dos dados de posicionamento. Os nomes de ficheiro seguem o
padrão `Frame_N.png`, com o hash de upload do Label Studio removido (ex:
`2f3f8fcb-Frame_1.png` → `Frame_1.png`).

## Uso

```bash
python3 load_dataset.py
```

Isto imprime um resumo do dataset (número de tasks, contagem de regiões
por categoria) e verifica se todas as imagens referenciadas no JSON estão
presentes em `images/`.

## Autores

- Estêvão Abreu — 2021220591
- João Luiz Castanheira — 2022212582

Criatividade Computacional para Design, MDM @ FCTUC, 2025/2026.
