from app.prompt_templates import INVESTIGATE_SYSTEM_PROMPT, INVESTIGATE_USER_PROMPT, SIMILARITY_CHECK_USER_PROMPT

def create_investigate_system_prompt(case_name: str, name: str, reliability: int,memory: str, personality: str) -> str:
    return INVESTIGATE_SYSTEM_PROMPT.format(
        case_name=case_name,
        name=name,
        reliability=reliability,
        memory=memory,
        personality=personality
    )

def create_investigate_user_prompt(question: str) -> str:
    return INVESTIGATE_USER_PROMPT.format(question=question)

def create_similarity_check_user_prompt(cumulative_description: str) -> str:
    return SIMILARITY_CHECK_USER_PROMPT.format(cumulative_description=cumulative_description)