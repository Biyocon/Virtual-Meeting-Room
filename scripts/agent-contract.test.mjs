// Dependency-free contract test (run: `npm run test:contract`).
//
// Guards two things:
//  1. Drift — every type literal in lib/agent/contract.ts must be declared in
//     agent-event.schema.json (and vice-versa). This is the TS↔Python seam.
//  2. Shape — sample events validate against the schema's required payload keys;
//     known-bad samples are rejected.
//
// No test framework, no new deps (keeps the lockfile untouched — guardrail).

import { readFileSync } from "node:fs"
import { fileURLToPath } from "node:url"
import { dirname, join } from "node:path"

const here = dirname(fileURLToPath(import.meta.url))
const root = join(here, "..")

const contractTs = readFileSync(join(root, "lib/agent/contract.ts"), "utf8")
const schema = JSON.parse(readFileSync(join(root, "lib/agent/agent-event.schema.json"), "utf8"))

let failures = 0
const fail = (msg) => {
  failures++
  console.error("✗", msg)
}
const ok = (msg) => console.log("✓", msg)

// ── 1. Drift guard ───────────────────────────────────────────────────────────
// Only discriminator literals (`type: z.literal("…")`), not other literals
// such as Meeting.dataClassification.
const tsLiterals = new Set([...contractTs.matchAll(/\btype:\s*z\.literal\("([^"]+)"\)/g)].map((m) => m[1]))
const schemaTypes = new Set([...schema.eventTypes, ...schema.commandTypes])

for (const t of tsLiterals) {
  if (!schemaTypes.has(t)) fail(`type "${t}" is in contract.ts but missing from agent-event.schema.json`)
}
for (const t of schemaTypes) {
  if (!tsLiterals.has(t)) fail(`type "${t}" is in the schema but missing from contract.ts`)
}
if (failures === 0) ok(`drift guard: ${tsLiterals.size} types aligned across TS and JSON schema`)

// ── 2. Shape checks against schema.payloads ──────────────────────────────────
const envelopeRequired = schema.definitions.envelope.required.filter((k) => k !== "type" && k !== "payload")

function validateEvent(event) {
  for (const k of envelopeRequired) {
    if (event[k] === undefined || event[k] === "") return `envelope missing "${k}"`
  }
  const spec = schema.payloads[event.type]
  if (!spec) return `unknown event type "${event.type}"`
  for (const k of spec.required ?? []) {
    if (event.payload?.[k] === undefined) return `payload missing "${k}" for "${event.type}"`
  }
  return null
}

const base = { meetingId: "m1", ts: "2026-06-22T00:00:00Z", correlationId: "c1" }

const valid = [
  { ...base, type: "agent.status", payload: { status: "thinking" } },
  { ...base, type: "agent.message.delta", payload: { text: "hej" } },
  { ...base, type: "agent.message.final", payload: { text: "færdig", citations: [] } },
  { ...base, type: "audit.event", payload: { actor: "agent-1", action: "agent.respond" } },
]
const invalid = [
  { type: "agent.status", payload: { status: "thinking" } }, // missing envelope
  { ...base, type: "agent.message.delta", payload: {} }, // missing text
  { ...base, type: "nope.nope", payload: {} }, // unknown type
]

for (const e of valid) {
  const err = validateEvent(e)
  if (err) fail(`expected valid "${e.type}" but: ${err}`)
}
for (const e of invalid) {
  if (validateEvent(e) === null) fail(`expected "${e.type ?? "(no type)"}" to be rejected but it passed`)
}
if (failures === 0) ok(`shape checks: ${valid.length} valid + ${invalid.length} invalid samples behaved`)

// ── Result ───────────────────────────────────────────────────────────────────
if (failures > 0) {
  console.error(`\n${failures} contract check(s) failed.`)
  process.exit(1)
}
console.log("\nAgent Event Contract OK.")
