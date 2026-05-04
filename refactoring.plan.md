# Light Refactoring Plan: Pygame Squares Simulation

## 1. Overview

### Current State
The `main.py` file implements a pygame simulation with moving squares that chase and flee from each other. The code is functional but has several readability and maintainability issues:
- **Code duplication**: Similar logic appears in multiple places
- **Magic numbers**: Numeric constants are scattered throughout (e.g., `2200`, `2.2`, `3.0`)
- **Methods doing too much**: Some functions handle multiple responsibilities
- **Inconsistent naming and storage**: Variables like `vx`, `vy` are stored but unused; `bounds` is a list but labeled as a Tuple

### Goals for Refactoring
The refactoring will improve **readability** and **maintainability** while preserving all original behavior:
- Reduce code duplication by extracting common patterns
- Centralize magic numbers into named constants for clarity and easy adjustment
- Simplify long methods by breaking them into smaller, focused functions
- Remove unused variables and clean up naming inconsistencies

---

## 2. Refactoring Goals

1. **Extract Common Logic**: Consolidate similar methods (`larger_square()`, `smaller_square()`, `threat()`, `prey()`) into reusable helper functions.
2. **Centralize Constants**: Move all magic numbers to module-level constants with descriptive names.
3. **Reduce Method Length**: Break `update_square()` into smaller, focused functions (e.g., `apply_steering()`, `update_position()`, `update_boost()`).
4. **Remove Dead Code**: Delete unused variables (`vx`, `vy` in `__init__`).
5. **Clarify Intent**: Rename confusing functions and variables to reflect their purpose.

---

## 3. Step-by-Step Refactoring Plan

### Step 1: Extract Magic Numbers into Named Constants

**What to do:**
At the top of the file, after existing constants (SCREEN_WIDTH, etc.), add a new group of constants for movement physics and lifecycle:

```
# Movement physics constants
INITIAL_VELOCITY_MAGNITUDE = 2200  # pixels per second
SIZE_TO_SPEED_RATIO = 1.0  # inverse scaling: smaller = faster
BOOST_MULTIPLIER_VALUE = 2.2
BOOST_DECAY_RATE = 3.0

# Lifecycle constants
SPAWN_DELAY_SECONDS = 2
MIN_SQUARE_SIZE = 20
MAX_SQUARE_SIZE = 40
MIN_LIFESPAN = 30
MAX_LIFESPAN = 60

# UI constants
FPS_TEXT_X = 20
FPS_TEXT_Y = 10
HELP_TEXT_X = 20
HELP_TEXT_Y = 40
```

**Why this helps:**
- **Readability**: `BOOST_MULTIPLIER_VALUE` is clearer than `2.2` scattered in code
- **Maintainability**: Change one constant to tune all instances (e.g., adjust game speed)
- **Testability**: Easy to verify constants match intended values
- **Beginner concept**: Shows how magic numbers hide intent and configuration

**Inline comment in final code:**
```python
# Centralized magic numbers: These constants control physics, lifecycle, and UI layout.
# Using named constants makes the code self-documenting and easier to adjust for tuning.
```

---

### Step 2: Consolidate Filtering Methods into a Helper Function

**What to do:**
Replace `larger_square()` and `smaller_square()` methods with a single, more flexible helper. Add this helper method to the `Square` class:

```python
def _filter_by_size(self, squares: List[Square], larger: bool) -> List[Square]:
    """Filter squares by size comparison.
    
    If larger=True, return all squares larger than self.
    If larger=False, return all squares smaller than self.
    This helper reduces code duplication between threat() and prey() logic.
    """
    comparison = (lambda other: other.size > self.size) if larger else (lambda other: other.size < self.size)
    return [square for square in squares if comparison(square)]
```

Then rewrite `larger_square()` and `smaller_square()` to use this helper:

```python
def larger_square(self, squares: List[Square]) -> List[Square]:
    """Return all squares that are larger than this one."""
    return self._filter_by_size(squares, larger=True)

def smaller_square(self, squares: List[Square]) -> List[Square]:
    """Return all squares that are smaller than this one."""
    return self._filter_by_size(squares, larger=False)
```

**Why this helps:**
- **DRY Principle (Don't Repeat Yourself)**: Filter logic appears in one place
- **Beginner concept**: Higher-order functions and lambda expressions
- **Easier maintenance**: If filter logic changes, update one function

**Inline comment in final code:**
```python
# Helper method _filter_by_size() consolidates the filtering logic used by both threat() and prey().
# This reduces duplication and makes the logic easier to maintain and test.
```

---

### Step 3: Consolidate Nearest-Neighbor Lookup Logic

**What to do:**
Notice that `threat()` and `prey()` both:
1. Filter squares by size
2. Compute distances to all filtered squares
3. Find the minimum distance
4. Return the nearest square or self

Extract this into a helper method:

```python
def _find_nearest(self, squares: List[Square], find_threat: bool):
    """Find the nearest threat (larger square) or prey (smaller square).
    
    If find_threat=True, return nearest larger square; else nearest smaller square.
    Returns self if no candidates exist.
    This consolidates duplicate logic from threat() and prey() methods.
    """
    candidates = self.larger_square(squares) if find_threat else self.smaller_square(squares)
    if not candidates:
        return self
    
    # Calculate distances to all candidates and find minimum
    distances = [(square, self.center.distance_squared_to(square.center)) for square in candidates]
    nearest_square, _ = min(distances, key=lambda x: x[1])
    return nearest_square
```

Then simplify `threat()` and `prey()`:

```python
def threat(self, squares: List[Square]):
    """Return nearest larger square, or self if no threat exists."""
    return self._find_nearest(squares, find_threat=True)

def prey(self, squares: List[Square]):
    """Return nearest smaller square, or self if no prey exists."""
    return self._find_nearest(squares, find_threat=False)
```

**Why this helps:**
- **Reduces method length**: `threat()` and `prey()` now are one-liners
- **Beginner concept**: Refactoring to eliminate duplication
- **Easier testing**: Test the complex logic once in `_find_nearest()`

**Inline comment in final code:**
```python
# The _find_nearest() helper consolidates the nearest-neighbor lookup logic,
# eliminating duplicate distance calculations and min() calls between threat() and prey().
```

---

### Step 4: Break Down `update_square()` into Focused Functions

**What to do:**
`update_square()` currently handles:
1. Checking if the square is alive
2. Boundary checking and bouncing
3. Applying steering forces
4. Speed clamping
5. Position integration
6. Boost decay
7. Updating center

Extract these into helper functions:

```python
def _apply_steering(self, squares: List[Square], dt: float):
    """Apply flee and chase steering forces to the moving vector.
    
    This consolidates steering logic, making update_square() more readable.
    Separating concerns: steering forces are computed here, independent of physics.
    """
    flee_force = self.running(squares, dt)
    chase_force = self.chasing(squares, dt)
    self.moving_vector += flee_force + chase_force

def _update_position_and_boost(self, dt: float):
    """Update position based on velocity and decay the boost multiplier.
    
    This consolidates position integration and boost management.
    Separating the physics step (position) from the lifecycle step (boost decay).
    """
    # Apply boost multiplier to velocity before integration
    velocity = self.moving_vector * self.boost_multiplier
    self.x += velocity.x * dt
    self.y += velocity.y * dt
    
    # Decay boost multiplier back to 1.0 over time
    if self.boost_multiplier > 1.0:
        self.boost_multiplier = max(1.0, self.boost_multiplier - self.boost_decay * dt)
```

Then rewrite `update_square()`:

```python
def update_square(square: Square, squares: List[Square], bounds: Tuple[int, int], dt: float):
    """Advance one square by one frame using dt-based movement."""
    if not square.alive:
        # Check if spawn delay has elapsed
        if time.time() - square.birth_time > SPAWN_DELAY_SECONDS:
            square.alive = True
    else:
        # Step 1: Enforce boundaries
        square.x, square.y, square.moving_vector, bounce = square.check_for_bounds(bounds)
        
        # Step 2: Apply steering only if not bouncing
        if not bounce:
            square._apply_steering(squares, dt)
        
        # Step 3: Clamp speed to maximum
        if square.moving_vector.length_squared() > square.max_speed ** 2:
            square.moving_vector = square.clamp_speed()
        
        # Step 4: Integrate position and decay boost
        square._update_position_and_boost(dt)
        
        # Step 5: Refresh center position for next frame's steering calculations
        square.center = Vector2(square.x + square.size / 2, square.y + square.size / 2)
```

**Why this helps:**
- **Readability**: Each step is labeled and clear
- **Testability**: Can test steering, position, and boost separately
- **Beginner concept**: Separation of Concerns — each function has one responsibility
- **Maintainability**: Easier to debug or modify one step without affecting others

**Inline comment in final code:**
```python
# update_square() is now a high-level orchestrator that calls focused helper methods.
# Each step (steering, position, boost) is isolated, making the logic flow clear and testable.
```

---

### Step 5: Reduce Duplication in Square Initialization

**What to do:**
`create_squares()` and `reborn()` both create squares with identical initialization logic. Extract into a helper function:

```python
def _create_random_square(alive: bool = True) -> Square:
    """Create a square with random properties.
    
    This consolidates square creation logic used by both create_squares() and reborn().
    Reduces duplication and makes it easy to adjust square generation in one place.
    """
    size = random.randint(MIN_SQUARE_SIZE, MAX_SQUARE_SIZE)
    x = random.randint(0, SCREEN_WIDTH - size)
    y = random.randint(0, SCREEN_HEIGHT - size)
    
    # Speed is inversely proportional to size: smaller squares move faster
    velocity_scale = INITIAL_VELOCITY_MAGNITUDE * SIZE_TO_SPEED_RATIO / size
    vx = random.choice([-1, 1]) * velocity_scale
    vy = random.choice([-1, 1]) * velocity_scale
    max_speed = INITIAL_VELOCITY_MAGNITUDE / size
    
    color = random.choice(SQUARE_COLOR)
    birth_time = time.time()
    lifespan = random.randint(MIN_LIFESPAN, MAX_LIFESPAN)
    
    return Square(color, size, x, y, vx, vy, max_speed, birth_time, lifespan, alive)
```

Then simplify `create_squares()` and `reborn()`:

```python
def create_squares() -> List[Square]:
    """Create the initial set of random squares."""
    # Use the helper to create SQUARE_COUNT squares, all initially alive
    return [_create_random_square(alive=True) for _ in range(SQUARE_COUNT)]

def reborn(squares: List[Square]) -> List[Square]:
    """Respawn squares until the world reaches SQUARE_COUNT."""
    # Add new squares (initially inactive) until population is full
    while len(squares) < SQUARE_COUNT:
        squares.append(_create_random_square(alive=False))
    return squares
```

**Why this helps:**
- **DRY Principle**: Square creation logic is in one place
- **Beginner concept**: List comprehensions vs. explicit loops
- **Maintainability**: Adjust square generation once, everywhere benefits

**Inline comment in final code:**
```python
# The _create_random_square() helper consolidates square generation.
# Using this function in both create_squares() and reborn() eliminates duplication
# and makes it easy to adjust how squares are initialized.
```

---

### Step 6: Remove Unused Variables

**What to do:**
In `Square.__init__()`, the `vx` and `vy` parameters are stored as instance variables but never directly accessed. The code uses `moving_vector` instead. Remove these unused attributes:

**Before:**
```python
def __init__(self, color, size: int, x: float, y: float, vx: float, vy: float, max_speed: float, birth_time, life_span, alive):
    """Initialize a square with movement and lifecycle properties."""
    self.color = color
    self.size = size
    self.x = x 
    self.y = y
    self.center = Vector2(self.x + self.size / 2, self.y + self.size / 2)
    self.vx = vx              # <-- Unused
    self.vy = vy              # <-- Unused
    self.max_speed = max_speed
    self.moving_vector = Vector2(vx, vy)
    # ...
```

**After:**
```python
def __init__(self, color, size: int, x: float, y: float, vx: float, vy: float, max_speed: float, birth_time, life_span, alive):
    """Initialize a square with movement and lifecycle properties."""
    # Removed: self.vx and self.vy are redundant since moving_vector stores the velocity.
    # Using moving_vector directly is clearer and reduces memory overhead.
    self.color = color
    self.size = size
    self.x = x 
    self.y = y
    self.center = Vector2(self.x + self.size / 2, self.y + self.size / 2)
    self.max_speed = max_speed
    self.moving_vector = Vector2(vx, vy)  # Single source of truth for velocity
    # ...
```

**Why this helps:**
- **Memory efficiency**: One fewer attribute per square instance
- **Clarity**: `moving_vector` is the single source of truth for velocity
- **Beginner concept**: Avoiding redundant data representation

**Inline comment in final code:**
```python
# Removed self.vx and self.vy: moving_vector is the single source of truth for velocity.
# This reduces redundancy and potential for inconsistency (e.g., vx != moving_vector.x).
```

---

### Step 7: Simplify Bounds Handling in Main Loop

**What to do:**
In `run()`, `bounds` is created as a list `[SCREEN_WIDTH, SCREEN_HEIGHT]` but the type hint in `update_square()` says `Tuple[int, int]`. Change to a tuple for consistency:

**Before:**
```python
bounds = [SCREEN_WIDTH, SCREEN_HEIGHT]
```

**After:**
```python
bounds = (SCREEN_WIDTH, SCREEN_HEIGHT)  # Use tuple for consistency with type hints
```

**Why this helps:**
- **Type Safety**: Matches the type hints
- **Immutability**: Tuples signal intent: bounds shouldn't change
- **Beginner concept**: Understanding tuples vs. lists and type hints

**Inline comment in final code:**
```python
# Changed bounds from list to tuple for consistency with type hints.
# Tuples signal immutability: bounds are fixed configuration, not modifiable state.
```

---

## 4. Final Output Requirements (Mandatory)

When this plan is executed, the final refactored code **must include inline comments** that:

1. **Explain what changed**: "Added helper method `_filter_by_size()` to consolidate filtering logic"
2. **Explain why it improves the code**: "Reduces code duplication and makes the logic easier to test"
3. **Highlight concepts**: "This demonstrates the DRY Principle (Don't Repeat Yourself)"

The refactored code must:
- ✅ Preserve all original behavior (no bugs introduced)
- ✅ Maintain readability for first-year students
- ✅ Include concise, beginner-friendly comments
- ✅ Use the same coding style and conventions as the original
- ✅ Not introduce advanced patterns (e.g., metaclasses, decorators)

---

## 5. Key Concepts for Students

This refactoring illustrates important programming principles:

### **DRY Principle (Don't Repeat Yourself)**
When the same logic appears in multiple places, extract it into a reusable function. Example: `_find_nearest()` consolidates the nearest-neighbor search used by both `threat()` and `prey()`.

### **Separation of Concerns**
Each function should have one clear responsibility. Example: Breaking `update_square()` into `_apply_steering()`, `_update_position_and_boost()` makes each step's purpose clear.

### **Named Constants**
Replace magic numbers with descriptive variable names. Example: `BOOST_MULTIPLIER_VALUE` is clearer than `2.2` scattered throughout the code, and makes tuning easier.

### **Single Source of Truth**
Store information in one place, not multiple locations. Example: Use `moving_vector` for velocity, not both `vx`, `vy`, and `moving_vector`.

### **Type Consistency**
Honor type hints. If a function expects a `Tuple`, don't pass a `List`. Example: Using `(SCREEN_WIDTH, SCREEN_HEIGHT)` instead of `[SCREEN_WIDTH, SCREEN_HEIGHT]`.

---

## 6. Safety Notes

### Testing & Verification
- **Run the simulation after each refactoring step** to verify behavior hasn't changed
- **Visual inspection**: Squares should still chase, flee, bounce, and respawn as before
- **No changes to constants**: Behavior should be identical to the original

### Incremental Approach
- Apply one step at a time, testing between steps
- If a step introduces a bug, revert and investigate before proceeding

### Preserving Behavior
- Do NOT modify the algorithm logic (steering forces, speed clamping, lifespan)
- Do NOT change how squares interact or spawn
- Only improve readability and reduce duplication

### Common Pitfalls to Avoid
1. **Accidentally changing constants**: Ensure refactored code uses the same values as the original
2. **Breaking list/tuple conversions**: Be careful with bounds passed to functions
3. **Forgetting to update `center`**: The `center` must be recalculated after position changes
4. **Off-by-one errors in size ranges**: MIN_SQUARE_SIZE, MAX_SQUARE_SIZE should match `random.randint(20, 40)` behavior

---

## Conclusion

This light refactoring improves **readability** and **maintainability** while preserving all original behavior. By following this plan step-by-step, you'll learn practical refactoring techniques and solidify understanding of core programming principles like DRY, Separation of Concerns, and type safety.
