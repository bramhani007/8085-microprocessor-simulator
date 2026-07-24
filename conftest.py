"""
Pytest configuration file to automatically append backend to sys.path.
"""
import sys
import os

# Append the project root to sys.path so that tests can import backend modules correctly.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
