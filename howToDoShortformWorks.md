# How to Restore Shortform Works

## 1. Re-add the data — `data/research.py`

Add back the `SHORTFORM_WORKS` list above `LONGFORM_WORKS`:

```python
SHORTFORM_WORKS = [
    {
        "id": 1,
        "title": "Local Government Engagement: A 2025 Overview",
        "city": "Trenton",
        "state": "NJ",
        "date": "March 2026",
        "description": "A concise analysis of civic participation rates and engagement opportunities in Trenton, NJ's local government landscape.",
        "type": "Policy Brief",
    },
    {
        "id": 2,
        "title": "Youth Voter Turnout in Oklahoma City Municipal Elections",
        "city": "Oklahoma City",
        "state": "OK",
        "date": "February 2026",
        "description": "Short-form research on trends in youth voter participation in Oklahoma City's most recent local election cycle.",
        "type": "Research Note",
    },
    {
        "id": 3,
        "title": "Community Organizing in Greater Boston",
        "city": "Boston",
        "state": "MA",
        "date": "January 2026",
        "description": "An examination of existing civic organizations in Boston and opportunities for expanded civic participation.",
        "type": "Policy Brief",
    },
    {
        "id": 4,
        "title": "Atlanta's Civic Infrastructure: Strengths and Gaps",
        "city": "Atlanta",
        "state": "GA",
        "date": "December 2025",
        "description": "A snapshot analysis of Atlanta's civic ecosystem, identifying key partners and under-served communities.",
        "type": "Research Note",
    },
]
```

## 2. Re-add the import — `routers/research.py`

Update the import line to include `SHORTFORM_WORKS`:

```python
from data.research import SHORTFORM_WORKS, LONGFORM_WORKS, CITIES
```

And pass it into the template response:

```python
return templates.TemplateResponse(
    request,
    "research/index.html",
    {
        "active_tab": tab,
        "shortform_works": SHORTFORM_WORKS,
        "longform_works": filtered_longform,
        "cities": CITIES,
        "selected_city": city,
    },
)
```

Also add `"shortform"` back to the `TABS` list:

```python
TABS = ["what-we-do", "shortform", "longform"]
```

## 3. Re-add the tab link — `templates/research/index.html`

Add the Shortform Works tab back into the `<nav class="tabs">` block:

```html
<nav class="tabs" aria-label="Research subtabs">
  <a href="/research/what-we-do" class="tabs__link {% if active_tab == 'what-we-do' %}active{% endif %}">What We Do</a>
  <a href="/research/shortform"  class="tabs__link {% if active_tab == 'shortform'  %}active{% endif %}">Shortform Works</a>
  <a href="/research/longform"   class="tabs__link {% if active_tab == 'longform'   %}active{% endif %}">Longform Works</a>
</nav>
```

And re-add the shortform tab content block between the `what-we-do` and `longform` blocks:

```html
<!-- ---- SHORTFORM ---- -->
{% elif active_tab == 'shortform' %}
<div class="tab-content">
  <div class="page-header" style="margin-bottom:2rem;">
    <p class="section-body">Policy briefs, research notes, and shorter analyses from our team across all four operating states.</p>
  </div>
  <div class="cards-grid">
    {% for work in shortform_works %}
    <article class="card">
      <div class="card__body">
        <div class="card__category">{{ work.state }} &bull; {{ work.type }}</div>
        <h2 class="card__title">{{ work.title }}</h2>
        <p class="card__excerpt">{{ work.description }}</p>
        <div class="card__meta">
          <span class="card__date">{{ work.date }}</span>
          <a href="#" class="btn btn-outline-gold" style="font-size:0.75rem; padding:0.35rem 1rem;">Read</a>
        </div>
      </div>
    </article>
    {% endfor %}
  </div>
</div>
```
