from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from mcp.types import TextContent
import logging


class BaseGameHandler(ABC):
    def __init__(self, game_name: str):
        self.game_name = game_name
        self.logger = logging.getLogger(f"{__name__}.{game_name}")
    
    @abstractmethod
    async def get_announcements(self) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    async def get_announcement_detail(self, url: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def get_events(self) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    async def get_event_detail(self, url: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def get_updates(self) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    async def get_update_detail(self, url: str) -> Dict[str, Any]:
        pass
    
    def format_response(self, data: Any) -> List[TextContent]:
        try:
            if isinstance(data, dict):
                formatted_text = self._format_dict(data)
            elif isinstance(data, list):
                formatted_text = self._format_list(data)
            else:
                formatted_text = str(data)
            
            return [TextContent(type="text", text=formatted_text)]
        except Exception as e:
            self.logger.error(f"Error formatting response: {str(e)}")
            return [TextContent(type="text", text=f"Error formatting response: {str(e)}")]
    
    def _format_dict(self, data: Dict[str, Any]) -> str:
        lines = []
        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f"{key}:")
                for sub_key, sub_value in value.items():
                    lines.append(f"  {sub_key}: {sub_value}")
            elif isinstance(value, list):
                lines.append(f"{key}: {', '.join(str(item) for item in value)}")
            else:
                lines.append(f"{key}: {value}")
        return "\n".join(lines)
    
    def _format_list(self, data: List[Any]) -> str:
        if not data:
            return "데이터가 없습니다."
        
        lines = []
        for i, item in enumerate(data, 1):
            if isinstance(item, dict):
                lines.append(f"{i}. {self._format_dict(item)}")
            else:
                lines.append(f"{i}. {item}")
            lines.append("")  # 빈 줄 추가
        
        return "\n".join(lines)
    
    async def handle_error(self, error: Exception, operation: str) -> List[TextContent]:
        error_message = f"[{self.game_name}] {operation} 중 오류 발생: {str(error)}"
        self.logger.error(error_message)
        
        return [TextContent(
            type="text",
            text=error_message
        )]