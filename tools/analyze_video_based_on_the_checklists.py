import os
import sys
import json
from langchain.agents import tool

from util import ask_gpt4_omni


@tool
def analyze_video_based_on_the_checklist(question_and_options:str, agent_role:str) -> str:
    """
    Analyze video based on the checklists.

    Parameters:
    question_and_options (str): A string containing the main question and its possible answer options, 
                                 as provided in the dataset. This input will be used to generate a checklist 
                                 for analysis for detailed evaluation. 
    agent_role (str): The role or perspective the agent should adopt (e.g., "social psychologist," "behavioral analyst") 
                      when creating the checklist and conducting the video analysis.

    Returns:
    str: The analysis result generated by GPT-4, which includes observations and insights based on the checklist and video content.
    """

    openai_api_key  = os.getenv("OPENAI_API_KEY")
    video_file_name = os.getenv("VIDEO_FILE_NAME")
    frame_num       = int(os.getenv("FRAME_NUM"))
    image_dir       = os.getenv("IMAGES_DIR_PATH")

    print ("Called the tool of analyze_video_based_on_the_checklist")
    
    # The prompt to create a checklist for the video analysis based on the agent's role. 
    gpt_prompt = f"""
    You are assigned the role of a {agent_role}. Based on this role, create a detailed checklist consisting of 20 specific questions tailored to the responsibilities and objectives associated with this role. 
    Ensure that each question is relevant, actionable, and helps to clarify or achieve the role's tasks effectively.
    The checklist should focus on analyzing the given text information and also be adaptable for use with video content analysis in later stages. 
    The goal is to create a checklist that serves as a foundation for understanding interactions, behaviors, or contextual patterns, regardless of the input format.
    Here is the question text: {question_and_options}
    """
    
    # Create the checklist for the video analysis that based on the agent's role.
    checklist = ask_gpt4_omni(
                openai_api_key=openai_api_key,
                prompt_text=gpt_prompt,
                temperature=0.7,
             )
    # print ("checklist: ", checklist)
    
    gpt_prompt = f"""
    Please answer the following 20 questions. For each item, provide a detailed answer and explain the reason behind your answer.

    [Checklists]
    {checklist}

    For each response, structure your answer like this:
    - Answer: [Your answer here]
    - Reason: [Explain why this is your answer]
    """

    result = ask_gpt4_omni(
                openai_api_key=openai_api_key,
                prompt_text=gpt_prompt,
                image_dir=image_dir,
                vid=video_file_name,
                temperature=0.7,
                frame_num=frame_num 
            )
    # print ("result: ", result)
    return result
