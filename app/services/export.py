import json
import csv
import io
from typing import Dict, Any


def export_markdown(stories_data: Dict[str, Any]) -> str:
    md = "# User Stories\n\n"
    
    for epic in stories_data.get("epics", []):
        md += f"## Epic: {epic['name']}\n\n"
        md += f"{epic['description']}\n\n"
        
        for story in epic.get("stories", []):
            md += f"### {story['id']}: {story.get('i_want', 'N/A')}\n\n"
            md += f"**As a** {story['as_a']}\n\n"
            md += f"**I want** {story['i_want']}\n\n"
            md += f"**So that** {story['so_that']}\n\n"
            
            md += "**Acceptance Criteria:**\n"
            for ac in story.get("acceptance_criteria", []):
                md += f"- {ac}\n"
            md += "\n"
            
            md += f"**Priority:** {story.get('priority', 'N/A')}\n\n"
            
            if story.get("dependencies"):
                md += f"**Dependencies:** {', '.join(story['dependencies'])}\n\n"
            
            if story.get("notes"):
                md += f"**Notes:** {story['notes']}\n\n"
            
            md += "---\n\n"
    
    if stories_data.get("nfrs"):
        md += "## Non-Functional Requirements\n\n"
        for nfr in stories_data["nfrs"]:
            md += f"- **{nfr['name']}:** {nfr['requirement']}\n"
        md += "\n"
    
    return md


def export_csv(stories_data: Dict[str, Any]) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow([
        "Issue Type",
        "Summary",
        "Description",
        "Priority",
        "Assignee",
        "Labels",
        "Epic Link",
        "Story Points"
    ])
    
    for epic in stories_data.get("epics", []):
        for story in epic.get("stories", []):
            summary = f"{story['id']}: {story.get('i_want', 'N/A')}"
            description = (
                f"As a {story['as_a']}\n"
                f"I want {story['i_want']}\n"
                f"So that {story['so_that']}\n\n"
                f"Acceptance Criteria:\n"
                + "\n".join(story.get("acceptance_criteria", []))
            )
            
            writer.writerow([
                "Story",
                summary,
                description,
                story.get("priority", "Medium"),
                "",
                epic["name"],
                epic["name"],
                ""
            ])
    
    return output.getvalue()

