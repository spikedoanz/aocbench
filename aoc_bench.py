import hashlib
import uuid
from typing import List

import verifiers as vf
from datasets import Dataset

from aocb.task import (
    SYSTEM_PROMPT,
    compile_reward,
    correctness_reward,
    create_task,
    extract_lean4_block,
    load_tasks,
    run_task,
)


def load_environment(
    years: List[int] = [2015],
    days: List[int] = list(range(1, 26)),
    eval_days: List[int] = list(range(1,25)),
    use_think: bool = False,
    system_prompt: str = SYSTEM_PROMPT,
    weights: List[float] = [0.3, 0.7],
):
    """
    Load Advent of Code environment for verifiers.

    Args:
        years: List of years to include in the dataset
        days: List of days to include in the dataset
        eval_days: Days to use for evaluation (others used for training)
        use_think: Whether to use ThinkParser or regular Parser
        system_prompt: System prompt for the environment
        weights: [compile_weight, correctness_weight] for reward weighting
    """
    # Load all tasks
    all_tasks = load_tasks(years=years, days=days)

    # Split into train and eval based on eval_days
    train_tasks = [t for t in all_tasks if t["day"] not in eval_days]
    eval_tasks = [t for t in all_tasks if t["day"] in eval_days]

    # Convert to Dataset format expected by verifiers
    def tasks_to_dataset(tasks):
        data = [
            {
                "question": task["prompt"],  # Changed from "prompt" to "question"
                "info": {
                    "year": task["year"],
                    "day": task["day"],
                },
            }
            for task in tasks
        ]
        return Dataset.from_list(data)

    dataset = tasks_to_dataset(train_tasks)
    eval_dataset = tasks_to_dataset(eval_tasks)

    # Create parser with lean4 extraction
    # Wrapper to convert str|None to str for type compatibility
    def extract_fn(text: str) -> str:
        result = extract_lean4_block(text)
        return result if result is not None else ""

    if use_think:
        parser = vf.ThinkParser(extract_fn=extract_fn)
    else:
        parser = vf.Parser(extract_fn=extract_fn)

    # Create reward functions with caching to avoid duplicate task runs
    cache = {}

    def get_results(completion, year, day, parser):
        """Cache task creation and execution results."""
        # Convert completion to string for hashing (handles both str and list[dict])
        if isinstance(completion, list):
            # For chat format, get the last assistant message
            completion_str = ""
            for msg in completion:
                if msg.get("role") == "assistant":
                    completion_str += msg.get("content", "")
        else:
            completion_str = completion

        key = (year, day, hashlib.md5(completion_str.encode()).hexdigest())
        if key not in cache:
            extracted = parser.parse_answer(completion)
            if extracted is None:
                cache[key] = (None, None)
            else:
                task_id = f"{year}_{day:02d}_{uuid.uuid4()}"
                create_task(
                    task_identifier=task_id,
                    submission=extracted,
                    year=year,
                    day=day
                )
                compile_result, run_result = run_task(task_id)
                cache[key] = (compile_result, run_result)
        return cache[key]

    def compile_reward_func(parser, completion, info, **kwargs):
        year = info["year"]
        day = info["day"]
        compile_result, _ = get_results(completion, year, day, parser)
        if compile_result is None:
            return 0.0
        return compile_reward(compile_result)

    def correctness_reward_func(parser, completion, info, **kwargs):
        year = info["year"]
        day = info["day"]
        _, run_result = get_results(completion, year, day, parser)
        if run_result is None:
            return 0.0
        return correctness_reward(year, day, run_result)

    # Create rubric with compile and correctness rewards
    rubric = vf.Rubric(
        parser=parser,
        funcs=[compile_reward_func, correctness_reward_func],
        weights=weights,
    )

    # Create environment
    vf_env = vf.SingleTurnEnv(
        dataset=dataset,
        eval_dataset=eval_dataset,
        system_prompt=system_prompt,
        parser=parser,
        rubric=rubric,
    )

    return vf_env

if __name__ == "__main__":
    load_environment()
