# DocMaker AI — Task-First Capture Flow

A new, narrative-driven approach to creating GIF/video tutorials that focus on **user goals** instead of just recording clicks.

## Problem with Current GIFs

Current captures are **click-centric**:
- Too short (2-3 seconds)
- Show individual actions without context
- Missing the "why" behind each step
- User must infer the workflow from disjointed clips

## Solution: Task-First Narrative

Each capture tells a **4-beat story**:

| Beat | Purpose | Duration | User Value |
|------|---------|----------|------------|
| **1. CONTEXT** | Establish goal | 2-3s "slow" | What am I doing and why? |
| **2. CHALLENGE** | The friction point | 1-2s | Where do users get stuck? |
| **3. SOLUTION** | **THE LESSON** | 3-4s **slow** | This is the key learning moment |
| **4. RESULT** | Proof it works | 1-2s | What did I just achieve? |

**Total:** 7-10 seconds per workflow (vs 2-3s currently)

## New Capture Runner

**File:** `capture/run_task_first_captures.py`

### Key Features

1. **Narrative Phases**
   ```python
   await rec.context(page, "Schedule weekly team standup")
   await rec.challenge(page, "Find Monday 10 AM free slot")
   await rec.solution(page, "Double-click, fill in details, recurrence")
   await rec.result(page, "Event appears with recurring indicator")
   ```

2. **Variable Pacing**
   - **Slow phases:** Establish context, SOLUTION → Let user absorb
   - **Fast phases:** Mechanical navigation, routine clicks → Skip quickly

3. **Human-like Typing**
   ```python
   await page.type("[ng-model='editor.component.summary']",
                   "Weekly Team Standup", delay=120)  # 120ms per char
   ```
   Simulates real user speed, not machine gun typing

4. **Optional UI Simplification**
   ```python
   # Hide clutter (optional)
   await page.add_init_script("""
       const footer = document.querySelector('footer');
       if (footer) footer.style.display = 'none';
   """)
   ```

5. **Step Metadata**
   Captures narrative beats for potential caption generation:
   ```python
   {
       "workflow": "calendar-create-event",
       "steps": [
           {"phase": "Goal: Schedule weekly standup", "duration": 2.0},
           {"phase": "Problem: Find Monday 10 AM slot", "duration": 1.5},
           {"phase": "Do this: Double-click and create event", "duration": 3.5},
           {"phase": "Outcome: Recurring event appears", "duration": 2.0}
       ],
       "duration_s": 9.0
   }
   ```

## HTML5 Native Format

### Why Switch from GIF?

| Feature | GIF | MP4 (H.264) |
|---------|-----|-------------|
| Colors | 256 | 16.7M |
| **File Size** | Large | Small |
| **Audio** | ❌ | ✅ |
| **Scrubbing** | ❌ | ✅ |
| **Playback Speed** | ❌ Fixed | ✅ 0.5x/1x/2x |
| **Captions** | ❌ | ✅ VTT/WebVTT |
| **Browser Support** | Universal | 98% |

### Output Format Stack

**Publication Quality: MP4 (H.264 + AAC)**
```bash
python scripts/convert_to_mp4.py videos/ assets/ --formats mp4
```

**Quality Settings:**
- Codec: `libx264` (H.264)
- Preset: `medium` (speed vs quality balance)
- CRF: `23` (18-28, lower = better quality)
- Pixel Format: `yuv420p` (broad compatibility)
- Fast Start: Enabled

**Benefits:**
- 📱 Works on 98% of browsers (modern + legacy)
- 🎨 Full color (16.7M vs 256)
- ⚡ 20-50% smaller than GIF at same resolution
- 🔧 Scrubbing, playback speed control
- ♿ Caption support for accessibility

**Fallback: WebM (VP9 + Opus)**
```bash
python scripts/convert_to_mp4.py videos/ assets/ --formats webm
```

- Better compression than MP4
- Open source, royalty-free
- Modern browsers only (85% support)

**Legacy: GIF (email/PowerPoint only)**
- Use only if target platform doesn't support HTML5 video
- Keep under 200KB (current limit)

## Usage

### 1. Capture with Task-First Runner

```bash
export SOGO_URL=https://demo5.sogo.nu/SOGo/
export SOGO_USERNAME=demo
export SOGO_PASSWORD=demo

python capture/run_task_first_captures.py
```

### 2. Convert to MP4

```bash
python scripts/convert_to_mp4.py capture/videos/ site/docs/assets/ --formats mp4 --workers 4
```

### 3. Update Documentation

Use the React `<VideoFallback>` component in your markdown:

```markdown
import VideoFallback from '@site/src/components/VideoFallback';

<VideoFallback
  mp4="/assets/calendar-create-event.mp4"
  poster="/assets/calendar-create-event-poster.jpg"
  title="Scheduling a weekly team standup meeting"
>
  Our team schedules weekly standups every Monday at 10 AM.
  In SOGo 5, we use the recurrence setting to automatically repeat
  this meeting so we don't have to create it manually each week.
</VideoFallback>
```

The component automatically:
- Loads MP4 with WebM fallback
- Shows poster image before playback
- Mutes audio by default
- Provides native playback controls

## Workflow Design Checklist

Before capturing a workflow:

- [ ] **Identify User Goal:** What problem are we solving?
- [ ] **Define Pain Point:** Where do users currently get stuck?
- [ ] **Plan the 4 Beats:**
  - [ ] CONTEXT (Why this matters)
  - [ ] CHALLENGE (The friction)
  - [ ] **SOLUTION** (THE LESSON - slow down here!)
  - [ ] RESULT (Proof it worked)
- [ ] **Skip Obvious Navigation:** Don't show "click the menu" if it's routine
- [ ] **Human Typing:** Use `delay=120ms` for form fields
- [ ] **Target 7-10s:** Long enough to absorb, short enough to keep attention

## Migration Path

### Phase 1: Enable MP4 Output (Current)

1. Add `run_task_first_captures.py` to repo ✓
2. Add `convert_to_mp4.py` to repo ✓
3. Update `<VideoFallback>` component to support MP4 (todo)
4. Capture 1-2 workflows as proof-of-concept

### Phase 2: Recapture Critical Workflows

Priority by user impact:
1. Calendar workflows (highest value, most complex)
2. Email folder management ( quotidien but confusing)
3. Contacts import/export (one-time but painful)

### Phase 3: Phased GIF Deprecation

- Keep GIF format for email blasts and legacy platforms
- Default documentation to MP4
- Provide GIF fallback `<a href="...gif">` on request

## Future Enhancements

### Audio Narration
Add step 5 to story beat:
```python
async def narration(self, page: Page, script: str):
    """Add voiceover narration| await self.phase(page, 1.5, f"[NARRATION]: {script}")
```

### Auto-Captions from Story Metadata
Use step metadata to generate VTT captions:
```python
with open(f"{name}.vtt","w") as f:
    f.write(generate_captions(steps))
```

### AI-Title Suggestions
Analyze step metadata to suggest SEO titles:
```
"Scheduling weekly standups with recurrence in SOGo 5"
```