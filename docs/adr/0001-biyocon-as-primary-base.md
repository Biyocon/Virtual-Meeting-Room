---
status: accepted
---

# Biyocon som primær base

Vi evaluerede flere repos som produktfundament for AI Virtual Meeting Room. Efter at monorepoet (`Hassan-master`) og VSCodium blev taget ud af scope, er Biyocon den eneste Next.js/React/Tailwind/shadcn-kodebase, der allerede implementerer tabletop-mødelokalets UI og LiveKit/WebRTC-wiring. **Beslutning:** produktet bygges på **Biyocon som primær base**, fordi det er tættest på den specifikke tabletop/digitale-medarbejder-vision og sparer en genimplementering af møde-UI'et.

## Considered Options

- **Biyocon** (valgt) — nærmest visionen; eksisterende tabletop-UI + LiveKit-spor.
- **MiroTalk SFU** (fravalgt som base) — modent, men klassisk videokonference-UI og **AGPLv3 / kommerciel dual-licens**; beholdes som WebRTC/SFU-reference.
- **`Hassan-master`** (monorepo) — taget ud af scope af stakeholder.
- **Bygge fra bunden** (fravalgt) — Biyocon dækker allerede kerne-UI'et.

## Consequences

- `custom`, `odysseus` og `iqra` indtager donor-/reference-roller omkring Biyocon (afgøres i senere ADR'er).
- Biyocon har **ingen LICENSE-fil** i den vedlagte pakke → ejerskab/licens skal bekræftes før distribution.
