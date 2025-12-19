# """Example prompts demonstrating different patterns.
# 
# Prompts are reusable templates that help LLMs interact effectively
# with your server. They can be simple strings or structured messages.
# """
# 
# from typing import List
# from fastmcp.prompts import UserMessage, AssistantMessage
# from my_mcp_server.server import mcp
# 
# 
# # Simple string prompt
# @mcp.prompt()
# def analyze_code(code: str) -> str:
#     """Prompt for code analysis.
#     
#     Simple prompts return a string that becomes a user message.
#     
#     Args:
#         code: The code to analyze
#     
#     Returns:
#         A prompt for analyzing the code
#     """
#     return f"""Please analyze this code for:
# 1. Potential bugs or issues
# 2. Code quality and best practices
# 3. Suggestions for improvement
# 
# Code:
# ```
# {code}
# ```
# """
# 
# 
# # Structured prompt with multiple messages
# @mcp.prompt()
# def debug_error(error_message: str, context: str) -> List:
#     """Prompt for debugging errors.
#     
#     Structured prompts return a list of message objects for
#     more control over the conversation flow.
#     
#     Args:
#         error_message: The error message to debug
#         context: Additional context about when the error occurred
#     
#     Returns:
#         A structured conversation prompt
#     """
#     return [
#         UserMessage(content="I encountered an error and need help debugging it."),
#         UserMessage(content=f"Error message: {error_message}"),
#         UserMessage(content=f"Context: {context}"),
#         AssistantMessage(content="I'll help you debug this error. Let me analyze the information..."),
#     ]
# 
# 
# @mcp.prompt()
# def review_document(document_type: str, key_points: str) -> str:
#     """Prompt for document review.
#     
#     Args:
#         document_type: Type of document (e.g., "technical report", "blog post")
#         key_points: Key points to focus on during review
#     
#     Returns:
#         A prompt for document review
#     """
#     return f"""Please review this {document_type} with focus on:
# 
# Key Points to Check:
# {key_points}
# 
# Review Criteria:
# - Clarity and readability
# - Technical accuracy
# - Organization and structure
# - Grammar and style
# - Completeness
# 
# Please provide specific, actionable feedback.
# """
# 
# 
# @mcp.prompt()
# def explain_concept(concept: str, audience: str = "general") -> List:
#     """Prompt for explaining technical concepts.
#     
#     Demonstrates prompts with default parameter values.
#     
#     Args:
#         concept: The concept to explain
#         audience: Target audience level (default: "general")
#     
#     Returns:
#         A structured explanation prompt
#     """
#     audience_context = {
#         "beginner": "Explain in very simple terms with basic analogies",
#         "general": "Explain clearly with practical examples",
#         "technical": "Explain with technical depth and precision",
#         "expert": "Explain assuming advanced knowledge"
#     }
#     
#     instruction = audience_context.get(audience, audience_context["general"])
#     
#     return [
#         UserMessage(content=f"Please explain: {concept}"),
#         UserMessage(content=f"Target audience: {audience}"),
#         AssistantMessage(content=f"I'll explain {concept}. {instruction}."),
#     ]