import VideoTree
import openai
import os
import json
from langchain.agents import tool
from .retrieve_video_clip_captions import retrieve_video_clip_captions
import torch

def adaptive_frame_sampling(image_dir: str, question:str, captions:list, video_filename:str):

    prompt = f"""
    Please determine the appropriate frame sampling method for this provided video-based question and the corresponding video's timestamped captions.\n 
    question: {question}\n
    captions: {captions}
    Choose **only one** of the following two options and **return only the method name**:\n

    1. **Uniform Frame Sampling**: Use this method if the question requires analyzing the entire video to answer (e.g., the answer depends on information from across the video, such as a general summary or trends over time).\n
    2. **Videotree Frame Sampling**: Use this method if the question can be answered by looking at specific parts or segments of the video (e.g., the answer is based on a particular scene or events in the video).\n

    Your answer should be either: \n
    - **Videotree Frame Sampling** \n
    - **Uniform Frame Sampling**
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")


    response = openai.chat.completions.create(
        model="gpt-4o",  
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4000,
        temperature=0.3,
    )

    
    sampling_method = response.choices[0].message.content

    if sampling_method== "Videotree Frame Sampling":

        # img_feats = VideoTree.extract_features(image_dir)                         # If extracting the features on the fly.

        img_feats = torch.load(os.path.join(os.getenv("FRAME_FEATURES_PATH"), video_filename + ".pt"))     # If loading the pre extracted features

        relevance_score, width_res = VideoTree.adaptive_breath_expansion(img_feats, video_filename)
        depth_expansion_res = VideoTree.depth_expansion(img_feats, image_dir, relevance_score, width_res)
        indices = depth_expansion_res[0]["sorted_values"]
        indices = list(dict.fromkeys(indices))
        image_paths = sorted([os.path.join(image_dir, f) for f in os.listdir(image_dir)])
        selected_frames = [image_paths[idx] for idx in indices]  
        
        return selected_frames

    elif sampling_method == "Uniform Frame Sampling":
        return None

@tool
def analyze_video_gpt4o_with_adaptive_frame_sampling(gpt_prompt:str) -> str:
    """
    Analyze video tool.

    Parameters:
    gpt_prompt (str): In the GPT prompt, You must include 5 questions based on original questions and options.
    For example, if the question asks about the purpose of the video and OptionA is “C is looking for a T-shirt” and OptionB is “C is cleaning up the room,
    OptionA is “C is looking for a T-shirt?” and OptionB is “C is tidying the room?” and so on. 
    The questions should be Yes/No questions whenever possible.
    Also, please indicate what role you would like the respondent to play in answering the questions.

    Returns:
    str: The analysis result.
    """

    from util import ask_gpt4_omni

    print ("gpt_prompt: ", gpt_prompt)

    image_dir = os.getenv("IMAGES_DIR_PATH")
    video_filename = os.getenv("VIDEO_FILE_NAME") 
    openai_api_key = os.getenv("OPENAI_API_KEY")
    qa_json_str = os.getenv("QA_JSON_STR")
    question_data = json.loads(qa_json_str)
    question = question_data['question']

    frames = image_dir + "/" + video_filename

    captions = retrieve_video_clip_captions({"video_index": video_filename, "captions_file": os.getenv("CAPTIONS_FILE"), "dataset": os.getenv("DATASET")})
    # print(captions)
    selected_frames = adaptive_frame_sampling(frames, question, captions, video_filename)
    frame_num = int(os.getenv("FRAME_NUM"))

    print ("Called the tool of analyze_video_gpt4o_with_adaptive_frame_sampling.")

    result = ask_gpt4_omni(
                openai_api_key=openai_api_key,
                prompt_text=gpt_prompt,
                image_dir=image_dir,
                vid=video_filename,
                temperature=0.7,
                frame_num=frame_num,
                use_selected_images=selected_frames
            )
    print ("result: ", result)
    return result