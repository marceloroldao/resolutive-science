# RAMS v0.1-draft

## Resolutive Artificial Intelligence Mathematical Specification

**Status:** Experimental draft  
**Parent specification:** RSMS-1.0-rc.1  
**Scope:** Interface contracts for modular resolutive artificial-intelligence components.

---

## 1. Purpose

RAMS defines interoperable interfaces between independently testable Resolutive AI modules. It does not require a monolithic AI implementation and does not require neural networks.

The initial architecture separates five responsibilities:

1. **Sensing / edge state construction** — e.g. TRIVAX.
2. **Perceptual representation** — optional neural or non-neural encoder.
3. **Sequential inference** — e.g. resolutive-inference.
4. **Persistent knowledge and experience** — e.g. memoria.ia.
5. **Action/control integration** — domain-specific controller or agent runtime.

A module shall remain independently testable. Cross-module integration shall occur through versioned contracts rather than private internal state.

---

## 2. Core principle

RAMS distinguishes four objects that shall not be silently conflated:

\[
\mathcal O_t \neq \mathcal S_t \neq \mathcal K \neq \mathcal A_t
\]

where:

- \(\mathcal O_t\): observation/event at time \(t\);
- \(\mathcal S_t\): inferred state or belief state;
- \(\mathcal K\): persistent knowledge object;
- \(\mathcal A_t\): action intent or control request.

A trajectory is a resolvable path linking context to knowledge; it is not identical to the knowledge payload itself.

---

## 3. RAMS interface objects

### RAMS-D001 — ObservationFrame

Canonical sensory/event envelope produced by a sensing layer such as TRIVAX.

Required fields:

- `source_id`: stable source/sensor identifier;
- `timestamp`: monotonic or explicitly qualified wall-clock time;
- `sequence`: source-local monotonic sequence number;
- `values`: numeric, categorical, or structured observations;
- `quality`: optional quality/confidence indicators;
- `modality`: modality identifier such as `imu`, `temperature`, `vision-feature`, `audio-feature`, `text`, or domain-defined equivalent;
- `provenance`: producer and transformation history sufficient for audit.

An ObservationFrame shall describe observed/input state and shall not assert persistent semantic truth by itself.

### RAMS-D002 — InferenceState

Output of a sequential inference module.

Required fields:

- `state_id` or state distribution;
- `timestamp`;
- `confidence` or calibrated uncertainty representation when available;
- `source_refs`: references to the ObservationFrames used;
- `model_id` and model/version metadata;
- `anomaly` or regime-change indicators when implemented.

InferenceState is provisional state estimation. It shall not automatically overwrite persistent knowledge.

### RAMS-D003 — KnowledgeEvent

Candidate event sent to a persistent-memory module.

Required fields:

- `knowledge_id` or provisional identity;
- `payload`;
- `trajectory`;
- `modality`;
- `provenance`;
- `evidence`: support, contradiction, or neutral observation;
- `timestamp`;
- optional `confidence`.

A memory implementation may consolidate, challenge, relate, reject, or preserve this event according to its own validated lifecycle rules.

### RAMS-D004 — MemoryReference

Non-destructive reference returned by a memory module.

Required fields:

- `knowledge_id`;
- `trajectory` or route identifier;
- `active_status`;
- `confidence` or lifecycle state when defined;
- `provenance_refs`;
- optional historical state.

A MemoryReference shall distinguish shared knowledge identity from route-specific state.

### RAMS-D005 — NeuralFeature

Optional representation produced by a neural encoder.

Required fields:

- `encoder_id` and version;
- `modality`;
- `feature` or structured representation;
- `source_refs`;
- optional uncertainty/quality metadata.

A NeuralFeature is an interface object, not persistent knowledge. Neural encoders shall not be required for RAMS conformance.

### RAMS-D006 — ActionIntent

Request produced by inference/planning for a controller or actuator layer.

Required fields:

- `action_id`;
- `timestamp`;
- `target`;
- `command` or desired state;
- `confidence`/priority when applicable;
- `evidence_refs`: references to inference/memory objects supporting the action;
- `constraints`: optional safety or domain constraints.

ActionIntent is not direct hardware actuation. A physical deployment may require an independent safety/control layer.

---

## 4. Reference data flow

A minimal non-neural edge system may use:

\[
\text{Sensors} \rightarrow \text{TRIVAX} \rightarrow \mathcal O_t
\rightarrow \text{Inference} \rightarrow \mathcal S_t
\leftrightarrow \text{Memory} \rightarrow \mathcal K
\rightarrow \mathcal A_t.
\]

A multimodal system may insert an encoder:

\[
\mathcal O_t \rightarrow \text{NeuralFeature} \rightarrow \mathcal S_t.
\]

The neural stage remains optional.

---

## 5. Individual and collective memory

RAMS permits local and collective memory namespaces:

\[
M_i = M_i^{\mathrm{private}} \cup M^{\mathrm{collective}}.
\]

Promotion from private evidence to collective knowledge shall preserve provenance. A single agent or modality shall not silently rewrite collective knowledge without a declared consensus policy.

Knowledge identity and trajectory state shall remain separable:

\[
K \leftarrow \{T_1,T_2,\ldots,T_n\},
\]

where each trajectory may maintain independent confidence/lifecycle metadata.

---

## 6. Versioning and compatibility

Every implementing repository shall declare:

- RSMS compatibility target;
- RAMS contract version implemented;
- extensions or intentional departures;
- serialization/version identifiers for exchanged objects.

Initial experimental declaration format:

`RSMS compatibility: 1.0-rc.1`  
`RAMS interface compatibility: 0.1-draft`

This draft does not freeze wire serialization. JSON reference schemas and binary/embedded profiles are planned follow-up work.

---

## 7. Validation requirements

### RAMS-T001 — Round-trip identity

Serialization and deserialization shall preserve required fields and object identity semantics.

### RAMS-T002 — Provenance preservation

A chain `ObservationFrame -> InferenceState -> KnowledgeEvent -> MemoryReference` shall preserve traceable source references.

### RAMS-T003 — Module independence

Each module shall be testable without importing private internals from another module.

### RAMS-T004 — Neural ablation

When a neural encoder is introduced, experiments should compare the integrated system with a non-neural or simpler representation baseline when scientifically meaningful.

### RAMS-T005 — Failure isolation

Invalid or low-quality data from one route/source shall not silently corrupt unrelated route state or collective knowledge.

### RAMS-T006 — Embedded budget reporting

IoT/robotics benchmarks shall report, where applicable, latency, peak memory, persistent-storage cost, CPU budget, and communication overhead.

---

## 8. Planned implementation mapping

The initial experimental mapping is:

- `marceloroldao/trivax` -> ObservationFrame producer / edge sensing;
- `marceloroldao/resolutive-inference` -> InferenceState producer;
- `marceloroldao/memoria.ia` -> KnowledgeEvent consumer and MemoryReference producer;
- future `resolutive-neural` -> optional NeuralFeature producer;
- future `resolutive-ai` -> composition/integration layer.

These mappings are non-exclusive: conformance is defined by contracts and tests, not repository names.

---

## 9. Maturity

RAMS v0.1-draft is an experimental interface specification. It does not claim AGI, general intelligence, or superiority to established AI architectures. Its purpose is to make modular experiments interoperable, auditable, and falsifiable under the RSMS methodology.
