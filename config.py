"""Minimal runtime config for the SysApp UAT login test."""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://hc-uat.sysappai.net/")
TEST_USERNAME = os.getenv("TEST_USERNAME", "sanket_vspl")
TEST_PASSWORD = os.getenv("TEST_PASSWORD", "Sanket123#")
