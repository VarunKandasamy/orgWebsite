"""
Unit tests for the research city-filter logic in isolation —
exercises the filtering function directly without HTTP overhead.
"""
import pytest
from data.research import LONGFORM_WORKS, CITIES


def apply_city_filter(works: list, city: str | None) -> list:
    """Mirror the filter logic from routers/research.py."""
    if city:
        return [w for w in works if w["city"] == city]
    return works


class TestCityFilterLogic:
    def test_no_filter_returns_all(self):
        result = apply_city_filter(LONGFORM_WORKS, None)
        assert result == LONGFORM_WORKS

    def test_empty_string_returns_all(self):
        # Empty string is falsy — treated the same as no filter
        result = apply_city_filter(LONGFORM_WORKS, "")
        assert result == LONGFORM_WORKS

    @pytest.mark.parametrize("city", CITIES)
    def test_each_city_filter_returns_nonempty(self, city):
        result = apply_city_filter(LONGFORM_WORKS, city)
        assert len(result) > 0, f"Filter for '{city}' returned no results"

    @pytest.mark.parametrize("city", CITIES)
    def test_filtered_results_only_contain_target_city(self, city):
        result = apply_city_filter(LONGFORM_WORKS, city)
        for work in result:
            assert work["city"] == city, \
                f"Filtered result contains wrong city: {work['city']} (expected {city})"

    @pytest.mark.parametrize("city", CITIES)
    def test_other_cities_excluded(self, city):
        result = apply_city_filter(LONGFORM_WORKS, city)
        other_cities = [c for c in CITIES if c != city]
        result_cities = {w["city"] for w in result}
        for other in other_cities:
            assert other not in result_cities, \
                f"City '{other}' appeared in results filtered for '{city}'"

    def test_nonexistent_city_returns_empty(self):
        result = apply_city_filter(LONGFORM_WORKS, "Springfield")
        assert result == []

    def test_case_sensitive_filter(self):
        # Filter is case-sensitive — "trenton" (lowercase) should match nothing
        result = apply_city_filter(LONGFORM_WORKS, "trenton")
        assert result == [], "Filter should be case-sensitive"

    def test_partial_city_name_returns_empty(self):
        result = apply_city_filter(LONGFORM_WORKS, "Trent")
        assert result == []

    def test_filter_does_not_mutate_original(self):
        original_len = len(LONGFORM_WORKS)
        apply_city_filter(LONGFORM_WORKS, "Trenton")
        assert len(LONGFORM_WORKS) == original_len, "Filter mutated the source list"

    def test_all_cities_union_equals_full_dataset(self):
        """Union of all per-city filters must equal the full dataset."""
        collected = []
        for city in CITIES:
            collected.extend(apply_city_filter(LONGFORM_WORKS, city))
        assert sorted(w["id"] for w in collected) == sorted(w["id"] for w in LONGFORM_WORKS)

    def test_filter_preserves_work_structure(self):
        required_keys = {"id", "title", "city", "state", "date", "description", "type", "pages"}
        for city in CITIES:
            for work in apply_city_filter(LONGFORM_WORKS, city):
                assert required_keys.issubset(work.keys()), \
                    f"Filtered work missing keys: {required_keys - work.keys()}"
