"""
Tests for the main FastAPI application.

This module contains tests for the basic FastAPI app setup and health endpoint.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

# Create test client
client = TestClient(app)


class TestHealthEndpoint:
    """Test cases for the /health endpoint."""
    
    def test_health_endpoint_returns_200(self):
        """Test that the health endpoint returns a 200 status code."""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_endpoint_returns_correct_response(self):
        """Test that the health endpoint returns the expected response structure."""
        response = client.get("/health")
        data = response.json()
        
        assert "status" in data
        assert "message" in data
        assert "version" in data
        assert data["status"] == "healthy"
        assert data["version"] == "0.1.0"
        assert "Personal Finance Tracker API is running" in data["message"]
    
    def test_health_endpoint_response_content_type(self):
        """Test that the health endpoint returns JSON content type."""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"


class TestFastAPIApp:
    """Test cases for the FastAPI application configuration."""
    
    def test_app_has_correct_metadata(self):
        """Test that the FastAPI app has the correct metadata."""
        assert app.title == "Personal Finance Tracker API"
        assert app.version == "0.1.0"
        assert app.description == "Backend API for personal finance tracking and management"
    
    def test_cors_middleware_configured(self):
        """Test that CORS middleware is properly configured."""
        # Check that CORS middleware is added
        middleware_types = [type(middleware).__name__ for middleware in app.user_middleware]
        assert "Middleware" in middleware_types  # FastAPI wraps middleware in a Middleware class
    
    def test_openapi_docs_available(self):
        """Test that OpenAPI documentation is available."""
        response = client.get("/docs")
        assert response.status_code == 200
        
        response = client.get("/openapi.json")
        assert response.status_code == 200
    
    def test_openapi_spec_contains_metadata(self):
        """Test that the OpenAPI spec contains the app metadata."""
        response = client.get("/openapi.json")
        openapi_spec = response.json()
        
        assert openapi_spec["info"]["title"] == "Personal Finance Tracker API"
        assert openapi_spec["info"]["version"] == "0.1.0"
        assert openapi_spec["info"]["description"] == "Backend API for personal finance tracking and management"
    
    def test_health_endpoint_in_openapi_spec(self):
        """Test that the health endpoint is documented in the OpenAPI spec."""
        response = client.get("/openapi.json")
        openapi_spec = response.json()
        
        assert "/health" in openapi_spec["paths"]
        assert "get" in openapi_spec["paths"]["/health"]


class TestCORSHeaders:
    """Test cases for CORS headers."""
    
    def test_cors_headers_present_with_origin(self):
        """Test that CORS headers are present when Origin header is sent."""
        # CORS headers are only added when there's an Origin header in the request
        response = client.get("/health", headers={"Origin": "http://localhost:3000"})
        
        # Check for basic CORS headers that are always added
        assert "access-control-allow-origin" in response.headers
        assert "access-control-allow-credentials" in response.headers
    
    def test_cors_allow_origin_wildcard(self):
        """Test that CORS allows all origins (development configuration)."""
        response = client.get("/health", headers={"Origin": "http://localhost:3000"})
        assert response.headers["access-control-allow-origin"] == "*"
    
    def test_cors_allow_credentials(self):
        """Test that CORS allows credentials."""
        response = client.get("/health", headers={"Origin": "http://localhost:3000"})
        assert response.headers["access-control-allow-credentials"] == "true"
    
    def test_cors_preflight_request(self):
        """Test CORS preflight request handling."""
        response = client.options(
            "/health",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "Content-Type"
            }
        )
        assert response.status_code == 200
        # For preflight requests, the origin is echoed back, not wildcard
        assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
        assert "access-control-allow-methods" in response.headers
        assert "access-control-allow-headers" in response.headers


class TestAppStartup:
    """Test cases for application startup and basic functionality."""
    
    def test_app_starts_without_errors(self):
        """Test that the app can be instantiated without errors."""
        # This test passes if the app can be imported and instantiated
        from app.main import app
        assert app is not None
    
    def test_app_has_health_route(self):
        """Test that the app has the health route registered."""
        routes = [route.path for route in app.routes]
        assert "/health" in routes
