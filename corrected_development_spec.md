# Academic Apex Project - Development Specification (Corrected)

## Required Outputs
- **Codebase**: Complete React/TypeScript frontend and FastAPI backend
- **Services**: Curator service (Flask) and Ollama adapter
- **Infrastructure**: Docker + compose configuration files
- **Documentation**: README with runbook, environment variables, and troubleshooting guide
- **Testing**: Smoke tests and CI setup (GitHub Actions)
- **Design**: Design tokens and Figma-ready component specification (JSON format)
- **Final Deliverable**: `academic_apex_final.zip` artifact with absolute path output
- **Demo**: Optional video/gif demonstration of UI flows
- **Change Management**: PR with changelog after each major phase

---

## 8) Incremental Development Plan (continuation of existing build)

### Phase A (Days 0–3): Core Infrastructure + Ingestion
- Wire up FastAPI endpoints, Ollama adapter, curator service
- Implement ingestion pipeline with Tesseract fallback
- Basic frontend Upload functionality

### Phase B (Days 3–7): Planner & Obsidian Integration
- Implement planner pipeline (curator->planner)
- Generate sample plan, write to Obsidian
- Add smoke tests, CLI scripts

### Phase C (Days 7–14): UI Polish & Session Player
- Build dashboard, session player, strict mode UX
- Add animations, accessibility features
- Implement inline OCR correction modal

### Phase D (Days 14–21): Visuals & Assessment Engine
- Enable mindmaps, slide export, flashcards module
- Add auto-quiz generator and evaluation checks

### Phase E (Days 21–28): Adaptive Student Model & Analytics
- Implement mastery tracking, scheduling heuristics
- Add grade prediction dashboard
- Implement audit log and opt-in web fetcher

### Phase F (Post-30): Final Polish
- Performance optimization
- Dockerized deployment
- User testing

---

## 9) Acceptance Criteria & QA

### Performance Requirements
- **UX**: Dashboard loads in <300ms; session start latency <100ms
- **Accuracy**: OCR pipeline returns text for photos >80% average for legible notes (with manual correction flow)

### Functionality Requirements
- **End-to-End**: Smoke tests run complete flow (plan generated → Obsidian file exists → flashcards CSV produced)
- **Security**: No data sent off machine unless opt-in; all network calls logged
- **Accessibility**: Keyboard navigation and screen-reader labels present for main flows

---

## 10) Deliverables & Artifacts

### Code Components
- Frontend: React/TypeScript application
- Backend: FastAPI service
- Curator service: Flask application
- Ollama adapter service

### Infrastructure
- Docker configuration
- Docker Compose setup for curator and optional worker

### Documentation & Specifications
- Design tokens and Figma-ready component spec (JSON format)
- README with comprehensive runbook
- Environment variables documentation
- Troubleshooting guide

### Testing & CI
- Smoke tests suite
- CI setup using GitHub Actions

### Final Package
- `academic_apex_final.zip` artifact (with absolute path output upon completion)

---

## 11) Developer Instructions (Practical)

### Development Workflow
- Use feature branches with small, focused commits
- Write both unit and integration tests
- Provide manual-run checklist
- Include "staging" script to load sample models in Ollama

### Technical Decisions
- **Default Model Stack**: Local Mistral for core model selection ambiguity
- **Fallback Documentation**: Include TODO.md noting alternative models for cloud fallback

---

## 12) Non-Functional Notes & Tradeoffs

### Performance Considerations
- Heavy models require GPUs — implement graceful degradation to smaller models or lower token budget
- Avoid overusing curation model; cache curated prompts for repeat tasks

### Transparency Features
- Provide "explain decision" button that returns:
  - Exact prompt used
  - Model outputs for transparency

---

## Implementation Instructions

**Objective**: Implement the full system per this specification.

**Process**:
1. After each major phase: commit changes and open PR with changelog
2. Produce the final zip package
3. Create optional video/gif demo of UI flows
4. **Output the absolute path to the zip when complete**

---

## Required Output Format

Upon completion, provide:
```
Final deliverable location: [absolute_path_to_academic_apex_final.zip]
```
