# Architecture Documentation

## Scope
This document describes the architecture implemented in `main.py` for the square simulation.
All relationships below are based on concrete code in the repository.

## 1) Module Dependency Graph

```mermaid
flowchart TD
    subgraph "Repository"
        M["main.py"]
    end

    subgraph "Standard Library"
        R["random"]
        T["time"]
        TY["typing (List, Tuple)"]
    end

    subgraph "Third-Party"
        PG["pygame"]
        V2["pygame.math.Vector2"]
    end

    M --> R
    M --> T
    M --> TY
    M --> PG
    M --> V2
```

Notes:
- `main.py` is the execution and behavior module.
- No internal package split is present yet; simulation logic is centralized in one file.

## 2) High-Level Runtime Flow

```mermaid
flowchart TD
    A["Program Start"] --> B["run()"]
    B --> C["Initialize pygame, window, clock, font"]
    C --> D["create_squares()"]
    D --> E["Enter Main Loop"]

    E --> F["Compute dt from clock.tick(FPS)"]
    F --> G["handle_event()"]
    G --> H{"Continue Running?"}

    H -->|"No"| I["Exit Loop"]
    H -->|"Yes"| J["update_world(squares, bounds, dt)"]

    J --> K["draw_world(screen, squares)"]
    K --> L["draw_text(FPS) and draw_text(exit hint)"]
    L --> M["pygame.display.flip()"]
    M --> E

    I --> N["pygame.quit()"]
    N --> O["Program End"]
```

Notes:
- The frame loop is time-step driven (`dt`) and runs until close event or `Q` key.
- Rendering always follows world update in each active frame.

## 3) Function-Level Call Graph

```mermaid
flowchart TD
    ENTRY["__main__ guard"] --> RUN["run()"]

    RUN --> CS["create_squares()"]
    RUN --> HE["handle_event()"]
    RUN --> UW["update_world(squares, bounds, dt)"]
    RUN --> DW["draw_world(screen, squares)"]
    RUN --> DT["draw_text(...)"]

    UW --> AL["alive(squares)"]
    UW --> RB["reborn(squares)"]
    UW --> US["update_square(square, squares, bounds, dt)"]

    US --> CFB["Square.check_for_bounds(bounds)"]
    US --> RN["Square.running(squares, dt)"]
    US --> CH["Square.chasing(squares, dt)"]
    US --> CL["Square.clamp_speed()"]

    RN --> TH["Square.threat(squares)"]
    TH --> LG["Square.larger_square(squares)"]

    CH --> PR["Square.prey(squares)"]
    PR --> SM["Square.smaller_square(squares)"]

    DW --> PDR["pygame.draw.rect(...)"]
    HE --> PEG["pygame.event.get()"]
    AL --> TT1["time.time()"]
    RB --> RNG["random.choice()/random.randint()"]
    CS --> TT2["time.time()"]
```

Notes:
- `update_world` is the per-frame orchestration point.
- `update_square` encapsulates movement, steering, bounce, and boost decay.

## 4) Primary Execution Sequence

```mermaid
sequenceDiagram
    participant U as "User"
    participant PY as "Python Runtime"
    participant GL as "Game Loop (run)"
    participant EV as "Event Handler"
    participant W as "World Updater"
    participant S as "Square Updater"
    participant RD as "Renderer"

    U->>PY: "Launch program"
    PY->>GL: "run()"
    GL->>GL: "pygame init, window, clock, font"
    GL->>W: "create_squares()"

    loop "While running is True"
        GL->>GL: "dt = clock.tick(FPS) / 1000.0"
        GL->>EV: "handle_event()"
        EV-->>GL: "continue flag"

        alt "Quit event or key Q"
            GL->>GL: "running = False"
        else "Continue frame"
            GL->>W: "update_world(squares, bounds, dt)"
            W->>W: "alive(squares)"
            W->>W: "reborn(squares)"

            loop "For each square"
                W->>S: "update_square(square, squares, bounds, dt)"
                S->>S: "check_for_bounds(bounds)"

                alt "Bounce occurred"
                    S->>S: "reflect velocity and set boost"
                else "No bounce"
                    S->>S: "running(squares, dt)"
                    S->>S: "chasing(squares, dt)"
                end

                S->>S: "clamp speed if needed"
                S->>S: "integrate position, decay boost, update center"
            end

            GL->>RD: "draw_world(screen, squares)"
            GL->>RD: "draw_text(FPS and exit hint)"
            GL->>RD: "pygame.display.flip()"
        end
    end

    GL->>RD: "pygame.quit()"
```

## Assumptions
- Architecture is documented from `main.py`, which is the active simulation implementation.
- `example.py` appears to be a variant/skeleton and is not the runtime entry path used by default.
