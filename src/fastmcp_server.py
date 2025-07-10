#!/usr/bin/env python3

from fastmcp import FastMCP

# FastMCP 서버 생성
mcp = FastMCP(name="Game News Tools", port=8000)


@mcp.tool()
def get_game_announcements(game: str) -> str:
    """
    지정된 게임의 최신 공지사항 목록을 가져옵니다.
    
    Args:
        game: 게임 이름 (lordnine, epic_seven, lost_ark)
    
    Returns:
        공지사항 목록
    """
    return f"✅ {game} 공지사항 목록 (FastMCP)"


@mcp.tool()
def get_announcement_detail(game: str, announcement_id: str) -> str:
    """
    특정 공지사항의 상세 정보를 가져옵니다.
    
    Args:
        game: 게임 이름 (lordnine, epic_seven, lost_ark)
        announcement_id: 공지사항 ID
    
    Returns:
        공지사항 상세 정보
    """
    return f"✅ {game} 공지사항 상세: {announcement_id} (FastMCP)"


@mcp.tool()
def get_game_events(game: str) -> str:
    """
    지정된 게임의 최신 이벤트 목록을 가져옵니다.
    
    Args:
        game: 게임 이름 (lordnine, epic_seven, lost_ark)
    
    Returns:
        이벤트 목록
    """
    return f"✅ {game} 이벤트 목록 (FastMCP)"


@mcp.tool()
def get_event_detail(game: str, event_id: str) -> str:
    """
    특정 이벤트의 상세 정보를 가져옵니다.
    
    Args:
        game: 게임 이름 (lordnine, epic_seven, lost_ark)
        event_id: 이벤트 ID
    
    Returns:
        이벤트 상세 정보
    """
    return f"✅ {game} 이벤트 상세: {event_id} (FastMCP)"


@mcp.tool()
def get_game_updates(game: str) -> str:
    """
    지정된 게임의 최신 업데이트 목록을 가져옵니다.
    
    Args:
        game: 게임 이름 (lordnine, epic_seven, lost_ark)
    
    Returns:
        업데이트 목록
    """
    return f"✅ {game} 업데이트 목록 (FastMCP)"


@mcp.tool()
def get_update_detail(game: str, update_id: str) -> str:
    """
    특정 업데이트의 상세 정보를 가져옵니다.
    
    Args:
        game: 게임 이름 (lordnine, epic_seven, lost_ark)
        update_id: 업데이트 ID
    
    Returns:
        업데이트 상세 정보
    """
    return f"✅ {game} 업데이트 상세: {update_id} (FastMCP)"


if __name__ == "__main__":
    mcp.run(
        transport="sse",
        host="127.0.0.1"
    ) 