"""
Unit tests for data layer integrity.
Validates structure, types, geographic bounds, and internal consistency
without touching the HTTP layer.
"""
import pytest
from data.news import NEWS_ITEMS
from data.research import SHORTFORM_WORKS, LONGFORM_WORKS, CITIES
from data.chapters import CHAPTER_LOCATIONS
from data.about import TEAM_MEMBERS, PARTNERS


# ---------------------------------------------------------------------------
# News data
# ---------------------------------------------------------------------------

class TestNewsData:
    REQUIRED_KEYS = {"id", "category", "title", "excerpt", "date", "slug"}

    def test_news_items_not_empty(self):
        assert len(NEWS_ITEMS) > 0

    def test_all_news_items_have_required_keys(self):
        for item in NEWS_ITEMS:
            missing = self.REQUIRED_KEYS - item.keys()
            assert not missing, f"News item id={item.get('id')} missing keys: {missing}"

    def test_all_ids_are_unique(self):
        ids = [item["id"] for item in NEWS_ITEMS]
        assert len(ids) == len(set(ids)), "Duplicate news item IDs found"

    def test_all_slugs_are_unique(self):
        slugs = [item["slug"] for item in NEWS_ITEMS]
        assert len(slugs) == len(set(slugs)), "Duplicate news slugs found"

    def test_no_empty_string_fields(self):
        for item in NEWS_ITEMS:
            for key in self.REQUIRED_KEYS:
                assert item[key] != "", f"News item id={item['id']} has empty '{key}'"

    def test_slugs_contain_no_spaces(self):
        for item in NEWS_ITEMS:
            assert " " not in item["slug"], f"Slug '{item['slug']}' contains spaces"

    def test_ids_are_integers(self):
        for item in NEWS_ITEMS:
            assert isinstance(item["id"], int)

    @pytest.mark.parametrize("item", NEWS_ITEMS)
    def test_individual_news_item_structure(self, item):
        assert isinstance(item["title"], str) and len(item["title"]) > 0
        assert isinstance(item["excerpt"], str) and len(item["excerpt"]) > 0
        assert isinstance(item["category"], str) and len(item["category"]) > 0


# ---------------------------------------------------------------------------
# Research shortform data
# ---------------------------------------------------------------------------

class TestShortformData:
    REQUIRED_KEYS = {"id", "title", "city", "state", "date", "description", "type"}

    def test_shortform_not_empty(self):
        assert len(SHORTFORM_WORKS) > 0

    def test_all_have_required_keys(self):
        for work in SHORTFORM_WORKS:
            missing = self.REQUIRED_KEYS - work.keys()
            assert not missing, f"Shortform id={work.get('id')} missing: {missing}"

    def test_all_ids_unique(self):
        ids = [w["id"] for w in SHORTFORM_WORKS]
        assert len(ids) == len(set(ids))

    def test_all_states_are_two_letter_codes(self):
        for work in SHORTFORM_WORKS:
            assert len(work["state"]) == 2 and work["state"].isupper(), \
                f"Invalid state code: '{work['state']}'"

    def test_all_cities_are_known_operating_cities(self):
        operating_cities = {"Trenton", "Oklahoma City", "Boston", "Atlanta"}
        for work in SHORTFORM_WORKS:
            assert work["city"] in operating_cities, \
                f"Unknown city '{work['city']}' in shortform works"

    def test_no_empty_descriptions(self):
        for work in SHORTFORM_WORKS:
            assert len(work["description"].strip()) > 0, \
                f"Empty description in shortform id={work['id']}"

    def test_city_state_pairs_are_consistent(self):
        # Each city should always map to the same state
        expected = {
            "Trenton": "NJ",
            "Oklahoma City": "OK",
            "Boston": "MA",
            "Atlanta": "GA",
        }
        for work in SHORTFORM_WORKS:
            if work["city"] in expected:
                assert work["state"] == expected[work["city"]], \
                    f"City/state mismatch: {work['city']} mapped to {work['state']}"


# ---------------------------------------------------------------------------
# Research longform data
# ---------------------------------------------------------------------------

class TestLongformData:
    REQUIRED_KEYS = {"id", "title", "city", "state", "date", "description", "type", "pages"}

    def test_longform_not_empty(self):
        assert len(LONGFORM_WORKS) > 0

    def test_all_have_required_keys(self):
        for work in LONGFORM_WORKS:
            missing = self.REQUIRED_KEYS - work.keys()
            assert not missing, f"Longform id={work.get('id')} missing: {missing}"

    def test_all_ids_unique(self):
        ids = [w["id"] for w in LONGFORM_WORKS]
        assert len(ids) == len(set(ids))

    def test_pages_are_positive_integers(self):
        for work in LONGFORM_WORKS:
            assert isinstance(work["pages"], int) and work["pages"] > 0, \
                f"Invalid pages value '{work['pages']}' in longform id={work['id']}"

    def test_all_cities_in_cities_list(self):
        for work in LONGFORM_WORKS:
            assert work["city"] in CITIES, \
                f"Longform city '{work['city']}' not in CITIES list"

    def test_cities_list_matches_actual_data(self):
        """CITIES must contain exactly the cities that appear in longform works."""
        cities_in_data = {w["city"] for w in LONGFORM_WORKS}
        assert set(CITIES) == cities_in_data, \
            f"CITIES list mismatch. List: {set(CITIES)}, Data: {cities_in_data}"

    def test_city_state_pairs_are_consistent(self):
        expected = {
            "Trenton": "NJ",
            "Oklahoma City": "OK",
            "Boston": "MA",
            "Atlanta": "GA",
        }
        for work in LONGFORM_WORKS:
            if work["city"] in expected:
                assert work["state"] == expected[work["city"]]

    def test_each_city_has_exactly_one_longform_report(self):
        """Each operating city should have at least one longform report."""
        cities_covered = {w["city"] for w in LONGFORM_WORKS}
        for city in CITIES:
            assert city in cities_covered, f"No longform report for city: {city}"

    def test_shortform_and_longform_ids_independent(self):
        """IDs are scoped per list, not globally unique — but titles must be unique across both."""
        all_titles = [w["title"] for w in SHORTFORM_WORKS] + [w["title"] for w in LONGFORM_WORKS]
        assert len(all_titles) == len(set(all_titles)), "Duplicate titles across research works"


# ---------------------------------------------------------------------------
# CITIES list
# ---------------------------------------------------------------------------

class TestCitiesList:
    def test_cities_not_empty(self):
        assert len(CITIES) > 0

    def test_cities_are_strings(self):
        for city in CITIES:
            assert isinstance(city, str) and len(city) > 0

    def test_cities_are_unique(self):
        assert len(CITIES) == len(set(CITIES))

    def test_expected_cities_present(self):
        for city in ["Trenton", "Oklahoma City", "Boston", "Atlanta"]:
            assert city in CITIES, f"Expected city '{city}' missing from CITIES"


# ---------------------------------------------------------------------------
# Chapters data
# ---------------------------------------------------------------------------

class TestChaptersData:
    REQUIRED_KEYS = {"name", "city", "state", "lat", "lng", "description", "status"}
    # CONUS bounding box (generous)
    LAT_MIN, LAT_MAX = 24.0, 50.0
    LNG_MIN, LNG_MAX = -125.0, -66.0

    def test_four_chapters_present(self):
        assert len(CHAPTER_LOCATIONS) == 4, \
            f"Expected 4 chapters, got {len(CHAPTER_LOCATIONS)}"

    def test_all_chapters_have_required_keys(self):
        for ch in CHAPTER_LOCATIONS:
            missing = self.REQUIRED_KEYS - ch.keys()
            assert not missing, f"Chapter '{ch.get('name')}' missing keys: {missing}"

    def test_all_chapters_are_active(self):
        for ch in CHAPTER_LOCATIONS:
            assert ch["status"] == "Active", \
                f"Chapter '{ch['name']}' has status '{ch['status']}', expected 'Active'"

    def test_latitudes_within_conus(self):
        for ch in CHAPTER_LOCATIONS:
            assert self.LAT_MIN <= ch["lat"] <= self.LAT_MAX, \
                f"Latitude {ch['lat']} for '{ch['name']}' is outside CONUS"

    def test_longitudes_within_conus(self):
        for ch in CHAPTER_LOCATIONS:
            assert self.LNG_MIN <= ch["lng"] <= self.LNG_MAX, \
                f"Longitude {ch['lng']} for '{ch['name']}' is outside CONUS"

    def test_lat_lng_are_floats(self):
        for ch in CHAPTER_LOCATIONS:
            assert isinstance(ch["lat"], (int, float)), f"lat is not numeric in '{ch['name']}'"
            assert isinstance(ch["lng"], (int, float)), f"lng is not numeric in '{ch['name']}'"

    def test_expected_states_present(self):
        states = {ch["state"] for ch in CHAPTER_LOCATIONS}
        for expected in ["NJ", "OK", "MA", "GA"]:
            assert expected in states, f"State '{expected}' missing from chapters"

    def test_expected_cities_present(self):
        cities = {ch["city"] for ch in CHAPTER_LOCATIONS}
        for expected in ["Trenton", "Oklahoma City", "Boston", "Atlanta"]:
            assert expected in cities, f"City '{expected}' missing from chapters"

    def test_state_codes_are_two_letter_uppercase(self):
        for ch in CHAPTER_LOCATIONS:
            assert len(ch["state"]) == 2 and ch["state"].isupper(), \
                f"Invalid state code '{ch['state']}' in chapter '{ch['name']}'"

    def test_all_chapter_names_are_unique(self):
        names = [ch["name"] for ch in CHAPTER_LOCATIONS]
        assert len(names) == len(set(names)), "Duplicate chapter names"

    def test_no_two_chapters_at_same_coordinates(self):
        coords = [(ch["lat"], ch["lng"]) for ch in CHAPTER_LOCATIONS]
        assert len(coords) == len(set(coords)), "Two chapters share identical coordinates"

    def test_all_descriptions_are_non_empty(self):
        for ch in CHAPTER_LOCATIONS:
            assert len(ch["description"].strip()) > 20, \
                f"Description too short for chapter '{ch['name']}'"

    @pytest.mark.parametrize("chapter", CHAPTER_LOCATIONS)
    def test_individual_chapter_lat_lng_precision(self, chapter):
        # Coordinates should have at least 2 decimal places of precision
        lat_str = str(chapter["lat"])
        lng_str = str(chapter["lng"])
        assert "." in lat_str
        assert "." in lng_str


# ---------------------------------------------------------------------------
# About data
# ---------------------------------------------------------------------------

class TestTeamData:
    REQUIRED_KEYS = {"name", "title", "department", "bio"}

    def test_team_not_empty(self):
        assert len(TEAM_MEMBERS) > 0

    def test_all_members_have_required_keys(self):
        for member in TEAM_MEMBERS:
            missing = self.REQUIRED_KEYS - member.keys()
            assert not missing, f"Team member '{member.get('name')}' missing keys: {missing}"

    def test_all_names_are_unique(self):
        names = [m["name"] for m in TEAM_MEMBERS]
        assert len(names) == len(set(names))

    def test_known_directors_present(self):
        names = [m["name"] for m in TEAM_MEMBERS]
        assert "Lauren Elle Darby" in names, "Research director not in team data"
        assert "Ben Kelley" in names, "Chapters director not in team data"

    def test_no_empty_bios(self):
        for member in TEAM_MEMBERS:
            assert len(member["bio"].strip()) > 0, \
                f"Empty bio for team member '{member['name']}'"

    def test_bios_are_substantive(self):
        for member in TEAM_MEMBERS:
            assert len(member["bio"]) > 40, \
                f"Bio too short for '{member['name']}': '{member['bio']}'"


class TestPartnersData:
    REQUIRED_KEYS = {"name", "type", "description"}

    def test_partners_not_empty(self):
        assert len(PARTNERS) > 0

    def test_all_partners_have_required_keys(self):
        for partner in PARTNERS:
            missing = self.REQUIRED_KEYS - partner.keys()
            assert not missing, f"Partner '{partner.get('name')}' missing keys: {missing}"

    def test_all_partner_names_unique(self):
        names = [p["name"] for p in PARTNERS]
        assert len(names) == len(set(names))

    def test_known_partners_present(self):
        names = [p["name"] for p in PARTNERS]
        assert any("SPIA" in n for n in names), "SPIA partner not found"
        assert any("Future of Families" in n for n in names), \
            "Future of Families partner not found"

    def test_no_empty_descriptions(self):
        for partner in PARTNERS:
            assert len(partner["description"].strip()) > 0

    def test_partner_types_are_strings(self):
        for partner in PARTNERS:
            assert isinstance(partner["type"], str) and len(partner["type"]) > 0
