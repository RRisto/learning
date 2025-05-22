#!/usr/bin/env python
# coding: utf-8

import os
import chromadb
import datetime
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from chromadb.utils import embedding_functions
from mcp.server.fastmcp import FastMCP, Context
from mcp.server.fastmcp.prompts import base
from dotenv import load_dotenv

load_dotenv(override=True)

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=os.getenv("OPENAI_API_KEY"),
                model_name="text-embedding-3-small")


# Create a dataclass to hold our dependencies
@dataclass
class AppContext:
    collection: chromadb.Collection

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Set up and tear down the Chroma DB connection"""
    # Initialize Chroma client
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Get the collection
    collection = client.get_collection("obsidian_notes", embedding_function=openai_ef)
    
    try:
        yield AppContext(collection=collection)
    finally:
        # Any cleanup if needed
        pass


# Create the MCP server with our lifespan
mcp = FastMCP("ObsidianNotes", lifespan=app_lifespan)


@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    """Echo a message as a resource"""
    return f"Resource echo: {message}"


@mcp.tool()
def echo_tool(message: str) -> str:
    """Echo a message as a tool"""
    return f"Tool echo: {message}"


@mcp.prompt()
def echo_prompt(message: str) -> str:
    """Create an echo prompt"""
    return f"Please process this message: {message}"

@mcp.tool()
def get_sample_note() -> str:
    """Get a single sample note to examine its structure"""
    
    ctx = mcp.get_context()   
    collection = ctx.request_context.lifespan_context.collection
    
    # Get just one document
    results = collection.get(limit=1)
    
    if results["ids"] and len(results["ids"]) > 0:
        sample_id = results["ids"][0]
        sample_doc = results["documents"][0]
        sample_metadata = results["metadatas"][0] if "metadatas" in results and results["metadatas"] else {}
        
        # Format the output to show structure
        output = "Sample Note Structure:\n\n"
        output += f"ID: {sample_id}\n\n"
        
        output += "Metadata Fields:\n"
        for key, value in sample_metadata.items():
            output += f"- {key}: {type(value).__name__} = {value}\n"
        
        output += "\nDocument Content (first 200 chars):\n"
        output += sample_doc
        
        # If embeddings exist, show their shape
        if "embeddings" in results and results["embeddings"]:
            embedding = results["embeddings"][0]
            output += f"\n\nEmbedding: Vector of length {len(embedding)}"
        
        return output
    else:
        return "No documents found in the collection."
    
def format_search_results(vector_results):
    formatted_results = []
    for i, doc in enumerate(vector_results["documents"][0]):
        doc_id = vector_results["ids"][0][i]
        folder = vector_results["metadatas"][0][i]['folder']
        title = vector_results["metadatas"][0][i]['title']
        # Convert distance to similarity score (closer to 1 is better)
        similarity = 1.0 / (1.0 + vector_results["distances"][0][i]) if "distances" in vector_results else "N/A"

        # Add formatted result
        formatted_results.append(
            f"Note ID: {doc_id}\n"
            f"Title: {title}\n"
            f"Folder: {folder}\n"
            f"Similarity: {similarity:.4f}\n\n"
            f"{doc}\n"
            f"---")
    return "\n".join(formatted_results)


@mcp.tool()
def vector_search(query: str, n_results: int = 5, folder: str = None, ) -> str:
    """
    Search notes using both vector similarity
    
    Args:
        query: The search query
        n_results: Number of results to return
    """
    ctx = mcp.get_context()   
    collection = ctx.request_context.lifespan_context.collection
        
    where_clause = {}
    if folder:
        where_clause["folder"] = folder
    
    # 1. Vector search
    vector_results = collection.query(
        query_embeddings = openai_ef(query),
        where=where_clause if where_clause else None,
        n_results=n_results * 2  # Get more results to rerank
    )
    
    #Format the results
    if vector_results["documents"] and len(vector_results["documents"][0]) > 0:
        formatted_results = format_search_results(vector_results)
        return formatted_results
    else:
        return f"No notes found for query: '{query}'"

@mcp.tool()
def browse_notes(folder: str = None, tag: str = None, limit: int = 10, offset: int = 0) -> str:
    """
    Browse notes by category or tag
    
    Args:
        folder: Optional folder to filter by
        tag: Optional tag to filter by (will match if tag string contains this value)
        limit: Maximum number of notes to return
        offset: Number of notes to skip (for pagination)
    """
    ctx = mcp.get_context()   
    collection = ctx.request_context.lifespan_context.collection
    
    # Build where clause for filtering
    where_clause = {}
    if folder:
        where_clause["folder"] = folder
    
    # For tag filtering, we'll need to handle it manually since we want substring matching
    
    # Get all notes that match the category filter (or all notes if no category filter)
    results = collection.get(
        where=where_clause if where_clause else None,
        limit=1000  # Get a larger batch to filter manually
    )
    
    # Filter by tag if specified
    filtered_indices = []
    if tag and results["metadatas"]:
        for i, metadata in enumerate(results["metadatas"]):
            # Check if tags field exists and contains the tag substring
            if "tags" in metadata:
                tags_str = metadata["tags"]
                if isinstance(tags_str, str) and tag.lower() in tags_str.lower():
                    filtered_indices.append(i)
    else:
        # If no tag filter, use all results
        filtered_indices = list(range(len(results["documents"])))
    
    # Apply pagination
    start_idx = min(offset, len(filtered_indices))
    end_idx = min(start_idx + limit, len(filtered_indices))
    page_indices = filtered_indices[start_idx:end_idx]
    
    # Format the results
    if page_indices:
        formatted_results = []
        for idx in page_indices:
            doc = results["documents"][idx]
            doc_id = results["ids"][idx]
            metadata = results["metadatas"][idx]
            
            # Extract title and other metadata
            title = metadata.get("title", "Untitled")
            tags = metadata.get("tags", "")
            category = metadata.get("category", "Uncategorized")
            
            # Create a preview
            preview = doc[:100] + "..." if len(doc) > 100 else doc
            
            # Format the result
            formatted_results.append(
                f"## {title}\n"
                f"ID: {doc_id}\n"
                f"Category: {category}\n"
                f"Tags: {tags}\n\n"
                f"Preview: {preview}\n"
                f"---"
            )
        
        # Add pagination info
        pagination_info = f"Showing results {start_idx+1}-{end_idx} of {len(filtered_indices)}. "
        if end_idx < len(filtered_indices):
            pagination_info += f"Use offset={end_idx} to see more."
        
        return pagination_info + "\n\n" + "\n".join(formatted_results)
    else:
        return f"No notes found with the specified filters."
    
    
@mcp.resource("note://{note_id}")
def get_note(note_id: str) -> str:
    """
    Get the full content of a specific note by ID
    
    Args:
        note_id: The ID of the note to retrieve
    """
    ctx = mcp.get_context()   
    collection = ctx.request_context.lifespan_context.collection
    
    # Query for the specific note
    result = collection.get(
        ids=[note_id]
    )
    
    # Check if note was found
    if result["documents"] and len(result["documents"]) > 0:
        # Get the note content and metadata
        content = result["documents"][0]
        metadata = result["metadatas"][0] if result["metadatas"] else {}
        
        # Format with metadata if available
        title = metadata.get("title", "Untitled")
        tags = metadata.get("tags", "")
        
        return f"# {title}\n\nTags: {tags}\n\n{content}"
    else:
        return f"Note with ID '{note_id}' not found."
    
    


@mcp.prompt()
def explore_topic(topic: str) -> list[base.Message]:
    return [
        # Include system instructions in the first user message instead
        base.Message(
            role="user",
            content=f"I want to learn more about {topic}. Please act as a helpful assistant that helps me explore topics in my notes. "
                   f"Use the vector_search tool to find relevant notes and browse_notes to explore categories (which are named as folder in database). "
                   f"When showing specific notes, use the note:// resource to get full content."
        ),
        base.Message(
            role="assistant",
            content="I'd be happy to help you explore this topic. I'll search your notes to find relevant information."
        )
    ]


@mcp.tool()
def get_notes_for_summary(query: str, folder: str = None, max_notes: int = 5) -> str:
    """
    Retrieve notes related to a query for summarization
    
    Args:
        query: Search query to find relevant notes
        folder: Optional folder to filter notes by
        max_notes: Maximum number of notes to include
    """
    # Get the context
    ctx = mcp.get_context()
    
    # Access the collection from the lifespan context
    collection = ctx.request_context.lifespan_context.collection
    
    # Create where clause if folder is specified
    where_clause = {}
    if folder:
        where_clause["folder"] = folder
    
    # Search for relevant notes with optional folder filter
    results = collection.query(
        query_embeddings=openai_ef(query),
        where=where_clause if where_clause else None,
        n_results=max_notes
    )
    
    # Format notes with titles and metadata
    if results["documents"] and len(results["documents"][0]) > 0:
        
        formatted_results = format_search_results(results)        
        # Add context about the search
        header = f"Notes about '{query}'"
        if folder:
            header += f" from folder '{folder}'"
        header += f" (showing {len(formatted_results)} results):\n\n"
        
        return header + formatted_results
    else:
        if folder:
            return f"No notes found for query '{query}' in folder '{folder}'."
        else:
            return f"No notes found for query: '{query}'"
        
        
@mcp.prompt()
def summarize_topic(topic: str, folder: str = None) -> list[base.Message]:
    folder_text = f" in the folder '{folder}'" if folder else ""
    
    return [
        base.Message(
            role="user",
            content=f"I want a summary of my notes about {topic}{folder_text}. Please use the get_notes_for_summary tool to retrieve relevant notes, then create a comprehensive summary that captures the key points, concepts, and relationships. The summary should be well-structured and highlight the most important information."
        ),
        base.Message(
            role="assistant",
            content="I'll help you summarize your notes on this query. Let me retrieve the relevant information first."
        )
    ]


if __name__ == "__main__":
    mcp.run(transport="streamable-http")





