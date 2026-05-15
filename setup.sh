#!/usr/bin/env bash
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "${YELLOW}>> Checking Python${NC}"
command -v python3 >/dev/null 2>&1 || {
  echo "${RED}Error: python3 not found."
  exit 1
}

echo "${YELLOW}>> Creating virtual environment${NC}"
python3 -m venv .venv

echo "${YELLOW}>> Active virtual environment${NC}"
# shellcheck disable=SC1091
source ".venv/bin/activate"

echo "${YELLOW}>> Updating pip${NC}"
pip install --upgrade pip

echo "${YELLOW}>> Installing dependencies${NC}"
pip install -r requirements.txt

echo "${YELLOW}>> Creating .env file${NC}"
cp ".env.example" ".env"

echo "${GREEN}>> Setup completed${NC}"