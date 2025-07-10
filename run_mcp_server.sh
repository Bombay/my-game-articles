#!/bin/bash

# 프로젝트 디렉토리로 이동
cd "/Users/hyuntkim/workspace/my-game-articles"

# 환경변수 설정
export PYTHONPATH="/Users/hyuntkim/workspace/my-game-articles"
export PYTHONIOENCODING=utf-8

# 가상환경의 Python으로 표준 MCP 서버 실행
exec "/Users/hyuntkim/workspace/my-game-articles/.venv/bin/python" "src/working_mcp_server.py" 