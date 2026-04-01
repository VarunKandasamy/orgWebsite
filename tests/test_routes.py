"""
Integration tests for all HTTP routes.
Tests status codes, redirects, and page-level HTML content.
"""
import html
import pytest
from fastapi.testclient import TestClient
from main import app


def unescape(response_text: str) -> str:
    """Undo Jinja2 HTML auto-escaping so we can match raw strings like apostrophes."""
    return html.unescape(response_text)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def client():
    with TestClient(app, follow_redirects=False) as c:
        yield c


@pytest.fixture(scope="module")
def client_follow():
    with TestClient(app, follow_redirects=True) as c:
        yield c


# ---------------------------------------------------------------------------
# Homepage
# ---------------------------------------------------------------------------

class TestHomepage:
    def test_returns_200(self, client):
        r = client.get("/")
        assert r.status_code == 200

    def test_html_content_type(self, client):
        r = client.get("/")
        assert "text/html" in r.headers["content-type"]

    def test_hero_title_present(self, client):
        r = client.get("/")
        assert "Reinvigorating" in r.text

    def test_newsletter_form_present(self, client):
        r = client.get("/")
        assert "hero-newsletter-form" in r.text
        assert 'type="email"' in r.text

    def test_research_program_box_present(self, client):
        r = client.get("/")
        assert "Research Program" in r.text

    def test_chapters_program_box_present(self, client):
        r = client.get("/")
        assert "Chapters Program" in r.text

    def test_nav_links_present(self, client):
        r = client.get("/")
        for link_text in ["News", "Research Program", "Chapters Program", "About Us", "Contact"]:
            assert link_text in r.text, f"Nav link '{link_text}' missing from homepage"

    def test_footer_present(self, client):
        r = client.get("/")
        assert "Privacy Policy" in r.text


# ---------------------------------------------------------------------------
# News
# ---------------------------------------------------------------------------

class TestNews:
    def test_returns_200(self, client):
        assert client.get("/news").status_code == 200

    def test_all_news_items_rendered(self, client):
        from data.news import NEWS_ITEMS
        r = client.get("/news")
        for item in NEWS_ITEMS:
            assert item["title"] in r.text, f"News title '{item['title']}' not rendered"

    def test_categories_rendered(self, client):
        from data.news import NEWS_ITEMS
        r = client.get("/news")
        for item in NEWS_ITEMS:
            assert item["category"] in r.text

    def test_dates_rendered(self, client):
        from data.news import NEWS_ITEMS
        r = client.get("/news")
        for item in NEWS_ITEMS:
            assert item["date"] in r.text

    def test_card_grid_markup(self, client):
        r = client.get("/news")
        assert "cards-grid" in r.text


# ---------------------------------------------------------------------------
# Research redirects
# ---------------------------------------------------------------------------

class TestResearchRedirects:
    def test_research_root_redirects(self, client):
        r = client.get("/research")
        assert r.status_code in (301, 302, 307, 308)

    def test_research_root_redirects_to_what_we_do(self, client):
        r = client.get("/research")
        assert r.headers["location"].endswith("/research/what-we-do")

    def test_invalid_tab_redirects(self, client):
        r = client.get("/research/nonexistent-tab")
        assert r.status_code in (301, 302, 307, 308)
        assert "what-we-do" in r.headers["location"]


# ---------------------------------------------------------------------------
# Research tabs
# ---------------------------------------------------------------------------

class TestResearchTabs:
    @pytest.mark.parametrize("tab", ["what-we-do", "shortform", "longform"])
    def test_valid_tabs_return_200(self, client, tab):
        assert client.get(f"/research/{tab}").status_code == 200

    def test_what_we_do_active_class(self, client):
        r = client.get("/research/what-we-do")
        # Active tab link must have the 'active' class
        html = r.text
        idx = html.find("what-we-do")
        # Find the tabs__link for what-we-do and confirm 'active' appears on it
        tab_section = html[max(0, idx - 200):idx + 100]
        assert "active" in tab_section

    def test_shortform_active_class(self, client):
        r = client.get("/research/shortform")
        html = r.text
        idx = html.find("shortform")
        tab_section = html[max(0, idx - 200):idx + 100]
        assert "active" in tab_section

    def test_what_we_do_content(self, client):
        r = client.get("/research/what-we-do")
        assert "Lauren Elle Darby" in r.text
        assert "Research Department" in r.text

    def test_shortform_renders_all_works(self, client):
        from data.research import SHORTFORM_WORKS
        r = client.get("/research/shortform")
        text = unescape(r.text)
        for work in SHORTFORM_WORKS:
            assert work["title"] in text, f"Shortform title '{work['title']}' not rendered"

    def test_longform_renders_all_works_unfiltered(self, client):
        from data.research import LONGFORM_WORKS
        r = client.get("/research/longform")
        text = unescape(r.text)
        for work in LONGFORM_WORKS:
            assert work["title"] in text, f"Longform title '{work['title']}' not rendered"

    def test_longform_city_filter_trenton(self, client):
        from data.research import LONGFORM_WORKS
        r = client.get("/research/longform?city=Trenton")
        assert r.status_code == 200
        text = unescape(r.text)
        trenton_titles = [w["title"] for w in LONGFORM_WORKS if w["city"] == "Trenton"]
        other_titles   = [w["title"] for w in LONGFORM_WORKS if w["city"] != "Trenton"]
        for title in trenton_titles:
            assert title in text
        for title in other_titles:
            assert title not in text

    def test_longform_city_filter_boston(self, client):
        from data.research import LONGFORM_WORKS
        r = client.get("/research/longform?city=Boston")
        assert r.status_code == 200
        text = unescape(r.text)
        boston_titles = [w["title"] for w in LONGFORM_WORKS if w["city"] == "Boston"]
        for title in boston_titles:
            assert title in text

    def test_longform_city_filter_nonexistent_city_returns_empty(self, client):
        r = client.get("/research/longform?city=Springfield")
        assert r.status_code == 200
        text = unescape(r.text)
        # All longform titles should be absent
        from data.research import LONGFORM_WORKS
        for work in LONGFORM_WORKS:
            assert work["title"] not in text

    def test_longform_city_filter_shows_city_filter_ui(self, client):
        r = client.get("/research/longform")
        assert "city-filter" in r.text
        from data.research import CITIES
        for city in CITIES:
            assert city in r.text

    def test_longform_active_city_filter_link(self, client):
        r = client.get("/research/longform?city=Atlanta")
        html = r.text
        # The Atlanta filter link should carry the 'active' class
        idx = html.find("city=Atlanta")
        vicinity = html[max(0, idx - 50):idx + 100]
        assert "active" in vicinity

    def test_subtab_links_all_present(self, client_follow):
        r = client_follow.get("/research/what-we-do")
        assert "/research/what-we-do" in r.text
        assert "/research/shortform" in r.text
        assert "/research/longform" in r.text


# ---------------------------------------------------------------------------
# Chapters
# ---------------------------------------------------------------------------

class TestChapters:
    def test_returns_200(self, client):
        assert client.get("/chapters").status_code == 200

    def test_map_element_present(self, client):
        r = client.get("/chapters")
        assert 'id="chapters-map"' in r.text

    def test_leaflet_css_loaded(self, client):
        r = client.get("/chapters")
        assert "leaflet" in r.text.lower()

    def test_chapter_locations_json_injected(self, client):
        r = client.get("/chapters")
        assert "CHAPTER_LOCATIONS" in r.text

    def test_all_chapter_names_in_page(self, client):
        from data.chapters import CHAPTER_LOCATIONS
        r = client.get("/chapters")
        for ch in CHAPTER_LOCATIONS:
            assert ch["name"] in r.text, f"Chapter '{ch['name']}' not in page"

    def test_all_states_in_page(self, client):
        from data.chapters import CHAPTER_LOCATIONS
        r = client.get("/chapters")
        for ch in CHAPTER_LOCATIONS:
            assert ch["state"] in r.text

    def test_lat_lng_values_in_injected_json(self, client):
        from data.chapters import CHAPTER_LOCATIONS
        r = client.get("/chapters")
        for ch in CHAPTER_LOCATIONS:
            assert str(ch["lat"]) in r.text
            assert str(ch["lng"]) in r.text

    def test_start_chapter_cta_present(self, client):
        r = client.get("/chapters")
        assert "Start a Chapter" in r.text


# ---------------------------------------------------------------------------
# About redirects
# ---------------------------------------------------------------------------

class TestAboutRedirects:
    def test_about_root_redirects(self, client):
        r = client.get("/about")
        assert r.status_code in (301, 302, 307, 308)

    def test_about_root_redirects_to_mission(self, client):
        r = client.get("/about")
        assert r.headers["location"].endswith("/about/mission")

    def test_invalid_about_tab_redirects(self, client):
        r = client.get("/about/nonexistent")
        assert r.status_code in (301, 302, 307, 308)
        assert "mission" in r.headers["location"]


# ---------------------------------------------------------------------------
# About tabs
# ---------------------------------------------------------------------------

class TestAboutTabs:
    @pytest.mark.parametrize("tab", ["mission", "what-we-do", "team", "partners"])
    def test_valid_tabs_return_200(self, client, tab):
        assert client.get(f"/about/{tab}").status_code == 200

    def test_mission_content(self, client):
        r = client.get("/about/mission")
        assert "foster" in r.text.lower()
        assert "local governance" in r.text.lower()

    def test_mission_long_term_vision(self, client):
        r = client.get("/about/mission")
        assert "Long-term Vision" in r.text or "Long-Term Vision" in r.text

    def test_what_we_do_priorities(self, client):
        r = client.get("/about/what-we-do")
        for priority in ["Youth Engagement", "Community Creation", "Generational Impact"]:
            assert priority in r.text, f"Priority '{priority}' missing from what-we-do tab"

    def test_what_we_do_offers_section(self, client):
        r = client.get("/about/what-we-do")
        assert "Colleges" in r.text
        assert "Non-profits" in r.text or "Non-profit" in r.text

    def test_team_tab_renders_members(self, client):
        from data.about import TEAM_MEMBERS
        r = client.get("/about/team")
        for member in TEAM_MEMBERS:
            assert member["name"] in r.text
            assert member["title"] in r.text

    def test_partners_tab_renders_partners(self, client):
        from data.about import PARTNERS
        r = client.get("/about/partners")
        for partner in PARTNERS:
            assert partner["name"] in r.text

    def test_partners_cta_links_to_contact(self, client):
        r = client.get("/about/partners")
        assert "/contact" in r.text

    def test_active_tab_class_applied(self, client):
        for tab in ["mission", "what-we-do", "team", "partners"]:
            r = client.get(f"/about/{tab}")
            html = r.text
            # Find the tab link for this tab and confirm 'active' is nearby
            idx = html.find(f"/about/{tab}")
            assert idx != -1
            vicinity = html[max(0, idx - 100):idx + 100]
            assert "active" in vicinity, f"Tab '{tab}' missing active class"

    def test_subtab_nav_contains_all_tabs(self, client):
        r = client.get("/about/mission")
        for path in ["/about/mission", "/about/what-we-do", "/about/team", "/about/partners"]:
            assert path in r.text


# ---------------------------------------------------------------------------
# Contact
# ---------------------------------------------------------------------------

class TestContact:
    def test_get_returns_200(self, client):
        assert client.get("/contact").status_code == 200

    def test_both_forms_present(self, client):
        r = client.get("/contact")
        assert "Partnership Inquiries" in r.text
        assert "General Inquiries" in r.text

    def test_partnership_form_action(self, client):
        r = client.get("/contact")
        assert 'action="/contact/partnership"' in r.text

    def test_general_form_action(self, client):
        r = client.get("/contact")
        assert 'action="/contact/general"' in r.text

    def test_no_success_banner_by_default(self, client):
        r = client.get("/contact")
        assert "success-banner" not in r.text

    def test_submitted_partnership_shows_banner(self, client_follow):
        r = client_follow.get("/contact?submitted=partnership")
        assert "success-banner" in r.text
        assert "partnership" in r.text.lower()

    def test_submitted_general_shows_banner(self, client_follow):
        r = client_follow.get("/contact?submitted=general")
        assert "success-banner" in r.text

    def test_partnership_post_valid_data_redirects(self, client):
        r = client.post("/contact/partnership", data={
            "name": "Jane Smith",
            "organization": "Civic Partners Inc.",
            "email": "jane@civicpartners.org",
            "message": "We would love to collaborate.",
        })
        assert r.status_code == 303
        assert "submitted=partnership" in r.headers["location"]

    def test_general_post_valid_data_redirects(self, client):
        r = client.post("/contact/general", data={
            "name": "John Doe",
            "email": "john@example.com",
            "subject": "Question about chapters",
            "message": "How do I start a chapter at my university?",
        })
        assert r.status_code == 303
        assert "submitted=general" in r.headers["location"]

    def test_partnership_post_missing_name_returns_422(self, client):
        r = client.post("/contact/partnership", data={
            "organization": "Some Org",
            "email": "test@test.com",
            "message": "Hello",
            # name is missing
        })
        assert r.status_code == 422

    def test_partnership_post_missing_email_returns_422(self, client):
        r = client.post("/contact/partnership", data={
            "name": "Jane",
            "organization": "Some Org",
            "message": "Hello",
            # email is missing
        })
        assert r.status_code == 422

    def test_partnership_post_missing_message_returns_422(self, client):
        r = client.post("/contact/partnership", data={
            "name": "Jane",
            "organization": "Some Org",
            "email": "jane@example.com",
            # message is missing
        })
        assert r.status_code == 422

    def test_general_post_missing_subject_returns_422(self, client):
        r = client.post("/contact/general", data={
            "name": "John",
            "email": "john@example.com",
            "message": "Hello",
            # subject is missing
        })
        assert r.status_code == 422

    def test_general_post_all_fields_missing_returns_422(self, client):
        r = client.post("/contact/general", data={})
        assert r.status_code == 422

    def test_contact_page_encourages_ideas(self, client):
        r = client.get("/contact")
        # The brief says: "say something like we would love to hear anything from you, including ideas"
        text = r.text.lower()
        assert "ideas" in text or "hear from you" in text


# ---------------------------------------------------------------------------
# Newsletter
# ---------------------------------------------------------------------------

class TestNewsletter:
    def test_valid_subscribe_returns_200(self, client):
        r = client.post(
            "/newsletter/subscribe",
            json={"email": "subscriber@example.com"},
        )
        assert r.status_code == 200

    def test_valid_subscribe_returns_json(self, client):
        r = client.post(
            "/newsletter/subscribe",
            json={"email": "subscriber@example.com"},
        )
        assert r.headers["content-type"].startswith("application/json")

    def test_valid_subscribe_status_field(self, client):
        r = client.post(
            "/newsletter/subscribe",
            json={"email": "subscriber@example.com"},
        )
        assert r.json() == {"status": "subscribed"}

    def test_missing_email_returns_422(self, client):
        r = client.post("/newsletter/subscribe", json={})
        assert r.status_code == 422

    def test_non_json_body_returns_422(self, client):
        r = client.post(
            "/newsletter/subscribe",
            data="not-json",
            headers={"Content-Type": "text/plain"},
        )
        assert r.status_code == 422

    def test_multiple_subscribes_all_succeed(self, client):
        emails = [
            "a@example.com",
            "b@example.com",
            "c@example.com",
        ]
        for email in emails:
            r = client.post("/newsletter/subscribe", json={"email": email})
            assert r.json()["status"] == "subscribed", f"Failed for {email}"


# ---------------------------------------------------------------------------
# Static assets
# ---------------------------------------------------------------------------

class TestStaticAssets:
    @pytest.mark.parametrize("path", [
        "/static/css/main.css",
        "/static/css/nav.css",
        "/static/css/hero.css",
        "/static/css/cards.css",
        "/static/css/tabs.css",
        "/static/css/map.css",
        "/static/css/contact.css",
        "/static/css/footer.css",
        "/static/js/main.js",
        "/static/js/map.js",
        "/static/js/newsletter.js",
    ])
    def test_static_file_exists_and_returns_200(self, client, path):
        r = client.get(path)
        assert r.status_code == 200, f"Static file missing: {path}"

    def test_css_contains_design_tokens(self, client):
        r = client.get("/static/css/main.css")
        assert "--color-navy" in r.text
        assert "--color-gold" in r.text
        assert "--font-display" in r.text
        assert "--font-body" in r.text

    def test_map_js_initializes_leaflet(self, client):
        r = client.get("/static/js/map.js")
        assert "L.map" in r.text
        assert "CHAPTER_LOCATIONS" in r.text

    def test_newsletter_js_posts_to_correct_endpoint(self, client):
        r = client.get("/static/js/newsletter.js")
        assert "/newsletter/subscribe" in r.text
        assert "fetch(" in r.text

    def test_main_js_sets_active_nav_link(self, client):
        r = client.get("/static/js/main.js")
        assert "active" in r.text
        assert "nav__link" in r.text


# ---------------------------------------------------------------------------
# 404 handling
# ---------------------------------------------------------------------------

class TestNotFound:
    def test_nonexistent_route_returns_404(self, client):
        assert client.get("/does-not-exist").status_code == 404

    def test_nonexistent_static_file_returns_404(self, client):
        assert client.get("/static/css/nonexistent.css").status_code == 404
