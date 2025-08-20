"""Tests for hook interface compliance."""

import pytest
from typing import Any

from ccproxy.hooks import (
    BaseHook,
    RuleEvaluatorHook,
    ModelRouterHook,
    ForwardOAuthHook,
    rule_evaluator,
    model_router,
    forward_oauth,
)


class TestHookInterfaces:
    """Test hook interface compliance with BaseHook."""

    def test_hook_classes_inherit_from_base(self) -> None:
        """Test that all hook classes inherit from BaseHook."""
        assert issubclass(RuleEvaluatorHook, BaseHook)
        assert issubclass(ModelRouterHook, BaseHook)
        assert issubclass(ForwardOAuthHook, BaseHook)

    def test_hook_classes_are_callable(self) -> None:
        """Test that all hook classes are callable."""
        # Create instances
        rule_hook = RuleEvaluatorHook()
        model_hook = ModelRouterHook()
        oauth_hook = ForwardOAuthHook()
        
        # Check they are callable
        assert callable(rule_hook)
        assert callable(model_hook)
        assert callable(oauth_hook)

    def test_backward_compatibility_instances(self) -> None:
        """Test that backward compatibility instances work."""
        # Check that the module-level instances are callable
        assert callable(rule_evaluator)
        assert callable(model_router)
        assert callable(forward_oauth)
        
        # Check they are instances of the hook classes
        assert isinstance(rule_evaluator, RuleEvaluatorHook)
        assert isinstance(model_router, ModelRouterHook)
        assert isinstance(forward_oauth, ForwardOAuthHook)
        
        # Check they are BaseHook instances
        assert isinstance(rule_evaluator, BaseHook)
        assert isinstance(model_router, BaseHook)
        assert isinstance(forward_oauth, BaseHook)

    def test_hook_callable_signature(self) -> None:
        """Test that hooks have the correct callable signature."""
        # Create test data
        data = {"model": "test", "metadata": {}}
        user_api_key_dict = {}
        
        # Create a mock handler object
        class MockHandler:
            classifier = None
            router = None
        
        mock_handler = MockHandler()
        
        # Create hook instances
        rule_hook = RuleEvaluatorHook()
        model_hook = ModelRouterHook()
        oauth_hook = ForwardOAuthHook()
        
        # Test they can be called with the expected signature
        # (they will return the data unchanged since no classifier/router provided)
        result = rule_hook(data, user_api_key_dict, mock_handler)
        assert result == data
        
        result = model_hook(data, user_api_key_dict, mock_handler)
        assert result == data
        
        result = oauth_hook(data, user_api_key_dict, mock_handler)
        assert result == data

    def test_custom_hook_implementation(self) -> None:
        """Test that custom hooks can be created by inheriting BaseHook."""
        
        class CustomHook(BaseHook):
            """Custom test hook."""
            
            def __call__(
                self,
                data: dict[str, Any],
                user_api_key_dict: dict[str, Any],
                handler: Any,
                **kwargs: Any
            ) -> dict[str, Any]:
                """Add custom field to data."""
                data["custom_field"] = "custom_value"
                return data
        
        # Create instance and test
        custom_hook = CustomHook()
        assert isinstance(custom_hook, BaseHook)
        assert callable(custom_hook)
        
        # Test it works
        data = {}
        mock_handler = object()  # Simple mock handler
        result = custom_hook(data, {}, mock_handler)
        assert result["custom_field"] == "custom_value"

    def test_base_hook_abstract_method(self) -> None:
        """Test that BaseHook cannot be instantiated directly."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            BaseHook()  # type: ignore