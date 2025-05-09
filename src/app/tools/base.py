from abc import ABC, abstractmethod
from typing import Dict, Any, ClassVar, Type
from pydantic import BaseModel, Field


class ToolInput(BaseModel):
    """Base class for tool inputs."""
    pass


class ToolOutput(BaseModel):
    """Base class for tool outputs."""
    pass


class BaseTool(ABC):
    """Base class for all MCP tools."""
    
    name: ClassVar[str]
    description: ClassVar[str]
    input_model: ClassVar[Type[ToolInput]]
    output_model: ClassVar[Type[ToolOutput]]
    
    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the tool with the provided input.
        
        Args:
            input_data: Dictionary containing the tool input parameters
            
        Returns:
            Dictionary containing the tool output
        """
        pass
    
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the tool with validation.
        
        Args:
            input_data: Dictionary containing the tool input parameters
            
        Returns:
            Dictionary containing the tool output
        """
        # Validate input using the input model
        validated_input = self.input_model(**input_data)
        
        # Execute the tool
        result = await self.execute(validated_input.model_dump())
        
        # Validate output using the output model
        validated_output = self.output_model(**result)
        
        return validated_output.model_dump()