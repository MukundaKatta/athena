"""Tests for Athena core functionality."""

from athena.core import Skill, SkillRegistry, skill
from athena.builtin_skills import get_all_builtin_skills


class TestSkillDecorator:
    def test_creates_skill_object(self) -> None:
        @skill(name="test_skill", description="A test")
        def my_func(x: int) -> int:
            return x * 2

        assert isinstance(my_func, Skill)
        assert my_func.name == "test_skill"

    def test_defaults_to_function_name(self) -> None:
        @skill()
        def another_func() -> str:
            return "hello"

        assert another_func.name == "another_func"


class TestSkillExecution:
    def test_execute_returns_result(self) -> None:
        @skill(name="double", description="Double a number")
        def double(n: int) -> int:
            return n * 2

        assert double.execute(n=5) == 10

    def test_validate_missing_input(self) -> None:
        @skill(name="greet", description="Greet")
        def greet(name: str) -> str:
            return f"Hi {name}"

        try:
            greet.execute()
            assert False, "Should have raised ValueError"
        except ValueError:
            pass


class TestSkillRegistry:
    def test_register_and_get(self) -> None:
        registry = SkillRegistry()
        @skill(name="test", description="test skill")
        def test_fn() -> str:
            return "ok"

        registry.register(test_fn)
        assert registry.get("test") is test_fn

    def test_search(self) -> None:
        registry = SkillRegistry()
        @skill(name="summarize_text", description="Summarize long text")
        def summarize(text: str) -> str:
            return text[:10]

        registry.register(summarize)
        results = registry.search("summarize")
        assert len(results) == 1

    def test_execute_via_registry(self) -> None:
        registry = SkillRegistry()
        @skill(name="add", description="Add two numbers")
        def add(a: int, b: int) -> int:
            return a + b

        registry.register(add)
        result = registry.execute("add", {"a": 3, "b": 4})
        assert result == 7

    def test_remove(self) -> None:
        registry = SkillRegistry()
        @skill(name="temp", description="temp")
        def temp() -> None:
            pass

        registry.register(temp)
        assert registry.remove("temp") is True
        assert registry.get("temp") is None

    def test_export(self) -> None:
        registry = SkillRegistry()
        @skill(name="x", description="x skill")
        def x() -> None:
            pass

        registry.register(x)
        export = registry.export_registry()
        assert export["total"] == 1
        assert "x" in export["skills"]


class TestBuiltinSkills:
    def test_all_builtins_load(self) -> None:
        skills = get_all_builtin_skills()
        assert len(skills) == 5

    def test_summarize(self) -> None:
        skills = get_all_builtin_skills()
        summarize = skills[0]
        result = summarize.execute(text="First sentence. Second sentence. Third sentence. Fourth.")
        assert "First sentence" in result

    def test_extract_keywords(self) -> None:
        skills = get_all_builtin_skills()
        extract = skills[1]
        result = extract.execute(text="Python programming language is great for data science")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_sentiment(self) -> None:
        skills = get_all_builtin_skills()
        sentiment = skills[2]
        result = sentiment.execute(text="This is great and amazing and wonderful")
        assert result["sentiment"] == "positive"
