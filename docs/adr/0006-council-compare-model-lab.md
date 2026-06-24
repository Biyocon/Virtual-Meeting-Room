---
status: accepted
---

# Council & Compare som "Model Lab" på sidecar'en

Vi skulle afgøre, hvordan LLM Council (3-fase modelråd med peer-review + chairman) og Compare (blind side-by-side + vote/scoreboard) bygges ind i Virtual Meeting Room. **Beslutning:** begge bygges som **capabilities i Python-sidecar'en** (`council.run`, `compare.run`) bag den eksisterende **Agent Event Contract** — ikke som kopieret kode i Next.js-UI'et. De eksponeres på tre niveauer: en **Model Lab-side**, et **møde-sidepanel**, og som **agent-capabilities** (`llm.council`, `llm.compare`). **Council implementeres før Compare**, og arbejdet placeres **efter M2** (sidecar'en).

## Considered Options

- **(A) Model Lab på sidecar, native reimplementering** (valgt) — konsistent med ADR-0005 (intelligens i sidecar, ikke i Next.js); ét fælles `model_router`; genbruger kontrakt, audit og owner-scoping.
- **(B) Hermes Agents tilgang: kopier native council-kode direkte ind i VMR's Next.js** (fravalgt) — bryder ADR-0005 (LLM-kald i `app/api/council` + `app/council/page.tsx` uden om sidecar/kontrakt), duplikerer model-kald, og Hermes-loggen viser fejlede/uverificerede file-mutations (bash-quoting-EOF, "files NOT modified"). Hermes' VMR-council-kode **må ikke merges til `main`**; den kan bevares i en separat `experiment/model-lab-nextjs-spike`-branch som reference, men produktionssporet implementeres native i sidecar efter M2.
- **(C) Wholesale-kopi af Odysseus Compare- eller LLM Council-kode** (fravalgt) — licens, se nedenfor.

## Licens (verificeret)

- **karpathy/llm-council: INGEN licens** → all rights reserved; koden må **ikke** kopieres ind i et kommercielt produkt. Kun **mønsteret** (anonymiseret peer-review + chairman-synthese) genbruges.
- **pewdiepie-archdaemon/odysseus: AGPL-3.0-or-later** → kopiering ind i et lukket produkt udløser copyleft. Kun **mønstre** (blind mode, side-by-side streaming, vote, reveal, scoreboard).
- Begge → **native reimplementering** efter egen kontrakt, ikke kodekopi.

> **Bemærk:** Dette er en teknisk licensrisikovurdering baseret på repo-metadata og offentlige filer, ikke juridisk rådgivning. Før kommerciel distribution bør licensstatus verificeres juridisk.

## Consequences

- **Fælles `sidecar/runtime/model_router.py`** (+ provider-adapters: Ollama/OpenRouter/OpenAI-compatible/Azure) deles af Council + Compare. Uden dette duplikeres model-kald.
- **Eventtyper udvides på den EKSISTERENDE `AgentEvent`-kontrakt** (`council.phase.started`, `council.phase1.answer`, `council.phase2.review`, `council.phase3.final`, `compare.response.delta/final`, `compare.vote.recorded`, `compare.scoreboard.updated`, `model.run.failed`) — ikke et parallelt streaming-system.
- **Datamodel** (i `lib/model-lab/contract.ts` + spejlet i sidecar): `ModelRef`, `ModelRun` (mode, blind, `meetingId?` optional → standalone + møde-integreret), `CouncilResult` (phase1/2/3), `CompareResult` (responses/votes/scoreboard), `ModelScore`.
- **Sikkerhed:** anonymisering (Council) + blind mode sker **server-side** i sidecar'en — browseren modtager ikke `modelId` før reveal (ellers er blind mode kosmetik). Council/Compare-adgang til mødedata går gennem `KnowledgeScope`/`FileAccessGrant`. **Mødeintegration er human-approved i MVP** (en agent må foreslå "Kør Council?", men ikke automatisk sende følsomt mødeindhold til eksterne modeller). Alle runs audit-logges. Kun testdata i MVP.
- **Rækkefølge:** M2 sidecar → `model_router` → Council v0 (non-streaming) → Compare v0 (streaming + vote/scoreboard) → mødeintegration. Council først, fordi det giver direkte produktværdi ("bedste svar fra flere modeller"); Compare er et evalueringsværktøj og kræver vote/scoreboard-state.
