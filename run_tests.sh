#!/bin/bash
# Test runner script

echo "Running unit tests..."
pytest tests/ -v --cov=dupliapp --cov-report=html --cov-report=term

echo "Generating coverage report..."
coverage html

echo "Tests completed!" 