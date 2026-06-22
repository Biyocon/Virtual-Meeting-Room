# AI Virtual Meeting Room

Et virtuelt mødelokale set oppefra, hvor menneskelige deltagere og digitale medarbejdere
deltager i samme møde. På sigt en app/plugin til Microsoft Teams.

## Language

**Digital medarbejder**:
En AI-agent, der deltager i et møde som en plads ved bordet — med persona, rolle, avatar, stemme, skills og videnadgang.
_Avoid_: chatbot, bot, assistant (i sidepanel-forstand)

**Menneskelig deltager**:
En rigtig person i mødet.
_Avoid_: bruger (tvetydigt)

**Tabletop-rum**:
Mødelokalet renderet top-down, med deltagere (menneskelige + digitale) placeret rundt om et fælles bord.
_Avoid_: stage, gallery, grid view

**Primær base**:
Den ene kodebase, produktet bygges oven på.
_Avoid_: foundation (overloaded), framework

**Komponent-donor**:
Et repo, vi høster specifikke moduler/mønstre fra, men ikke bygger oven på.
_Avoid_: dependency, library

**Reference**:
Et repo, vi studerer for design/arkitektur, men hverken bygger på eller kopierer kode fra.
_Avoid_: eksempel

**Egen brain**:
En enkelt agents private hukommelse, scoped til netop den agent.
_Avoid_: state, context (overloaded)

**Fælles brain**:
Hukommelse delt på tværs af et projekts eller mødes agenter/deltagere.
_Avoid_: global memory

**Videnscope**:
Det sæt af filer/mapper/data, en agent må tilgå i et givent møde.
_Avoid_: knowledge base (for bredt), data source
