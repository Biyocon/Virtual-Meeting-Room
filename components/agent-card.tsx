"use client"

// One digital-employee "seat at the table". Presentational only — it renders the
// reduced AgentView. Visual rules from docs/design/avatar-style-spec.md:
// illustrated 2D, status states, speaker ring, waveform, role label, and an
// always-visible synthetic-voice disclosure (compliance, ADR-0004).

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Card, CardContent } from "@/components/ui/card"
import { AudioLines } from "lucide-react"
import { cn } from "@/lib/utils"
import type { AgentStatus } from "@/lib/agent/contract"

type AccentKey = "violet" | "emerald" | "sky" | "amber"

const ACCENT: Record<AccentKey, { ring: string; dot: string; badge: string }> = {
  violet: { ring: "ring-violet-400", dot: "bg-violet-400", badge: "bg-violet-500/15 text-violet-200" },
  emerald: { ring: "ring-emerald-400", dot: "bg-emerald-400", badge: "bg-emerald-500/15 text-emerald-200" },
  sky: { ring: "ring-sky-400", dot: "bg-sky-400", badge: "bg-sky-500/15 text-sky-200" },
  amber: { ring: "ring-amber-400", dot: "bg-amber-400", badge: "bg-amber-500/15 text-amber-200" },
}

const STATUS_LABEL: Record<AgentStatus, string> = {
  idle: "Inaktiv",
  listening: "Lytter",
  thinking: "Tænker",
  speaking: "Taler",
}

export type AgentCardProps = {
  name: string
  role: string
  agentLabel?: string // model/agent provenance, e.g. "Stub v0"
  avatarImage?: string
  colorAccent?: AccentKey
  status: AgentStatus
  text: string
}

function Waveform({ active, dotClass }: { active: boolean; dotClass: string }) {
  return (
    <div className="flex items-end gap-0.5 h-4" aria-hidden>
      {[0, 1, 2, 3].map((i) => (
        <span
          key={i}
          className={cn("w-0.5 rounded-full", dotClass, active ? "animate-pulse" : "opacity-30")}
          style={{ height: active ? `${6 + ((i * 5) % 11)}px` : "4px", animationDelay: `${i * 120}ms` }}
        />
      ))}
    </div>
  )
}

export function AgentCard({ name, role, agentLabel, avatarImage, colorAccent = "violet", status, text }: AgentCardProps) {
  const accent = ACCENT[colorAccent]
  const speaking = status === "speaking"
  const thinking = status === "thinking"
  const initials = name.split(" ").map((w) => w[0]).join("").slice(0, 2).toUpperCase()

  return (
    <Card className="bg-purple-800/50 border-purple-600 text-white w-72">
      <CardContent className="p-4">
        <div className="flex items-center gap-3">
          <Avatar
            className={cn(
              "h-14 w-14 ring-2 ring-offset-2 ring-offset-purple-900 transition-all",
              speaking ? cn(accent.ring, "ring-opacity-100") : "ring-transparent",
            )}
          >
            {avatarImage ? <AvatarImage src={avatarImage} alt={name} /> : null}
            <AvatarFallback className="bg-purple-700 text-white font-medium">{initials}</AvatarFallback>
          </Avatar>

          <div className="min-w-0">
            <h3 className="font-medium truncate">{name}</h3>
            <p className="text-xs opacity-80 truncate">{role}</p>
            <div className="mt-1 flex items-center gap-2">
              <span className={cn("h-1.5 w-1.5 rounded-full inline-block", accent.dot, thinking && "animate-pulse")} />
              <span className="text-xs opacity-90">{STATUS_LABEL[status]}</span>
              <Waveform active={speaking} dotClass={accent.dot} />
            </div>
          </div>
        </div>

        {/* Synthetic-voice disclosure — always visible (compliance). */}
        <div className={cn("mt-3 inline-flex items-center gap-1 rounded px-2 py-0.5 text-[10px]", accent.badge)}>
          <AudioLines className="h-3 w-3" />
          Syntetisk stemme
        </div>

        {text ? (
          <p className="mt-3 text-sm leading-relaxed text-white/90 min-h-[1.25rem]">
            {text}
            {(thinking || speaking) && <span className="inline-block w-1.5 h-4 ml-0.5 align-middle bg-white/70 animate-pulse" />}
          </p>
        ) : null}

        {agentLabel ? <div className="mt-3 text-xs opacity-60">{agentLabel}</div> : null}
      </CardContent>
    </Card>
  )
}
