import hashlib
from typing import List, Tuple, Any

import verifiers as vf
from datasets import Dataset
from verifiers.types import Messages, State

from aocb.task import (
    SYSTEM_PROMPT,
    compile_reward,
    correctness_reward,
    create_spec,
    create_task,
    extract_lean4_block,
    load_tasks,
    run_task,
)

DEFAULT_COMPILER_OUTPUT_CROP = 10000


class AOCBMultiTurnEnv(vf.MultiTurnEnv):
    """Multi-turn environment for AOC Bench with compiler/test feedback."""
    
    def __init__(
        self,
        compiler_output_crop: int = DEFAULT_COMPILER_OUTPUT_CROP,
        **kwargs
    ):
        """
        Initialize the multi-turn AOC Bench environment.
        
        Args:
            compiler_output_crop: Max characters per compiler output field
            **kwargs: Additional arguments for MultiTurnEnv
        """
        super().__init__(**kwargs)
        self.compiler_output_crop = compiler_output_crop
        self.cache = {}
    
    def get_results(self, completion, year, day, parser):
        """Cache task creation and execution results."""
        if isinstance(completion, list):
            completion_str = ""
            for msg in completion:
                if msg.get("role") == "assistant":
                    completion_str += msg.get("content", "")
        else:
            completion_str = completion

        key = (year, day, hashlib.md5(completion_str.encode()).hexdigest())
        if key not in self.cache:
            extracted = parser.parse_answer(completion)
            if extracted is None:
                self.cache[key] = (None, None)
            else:
                spec = create_spec(year, day)
                task_id = create_task(spec, submission=extracted)
                compile_result, run_result = run_task(task_id)
                self.cache[key] = (compile_result, run_result)
        return self.cache[key]
    
    async def is_completed(self, messages: Messages, state: State, **kwargs) -> bool:
        """
        Check if the task is completed.
        
        Returns True if:
        - Maximum turns reached (handled by super())
        - Solution succeeded (all tests passed)
        """
        if await super().is_completed(messages, state, **kwargs):
            return True
        
        return state.get("succeeded", False)
    
    async def env_response(self, messages: Messages, state: State, **kwargs) -> Tuple[Messages, State]:
        """
        Generate environment response based on model's code attempt.
        
        Compiles and runs the code, providing feedback on success or failure.
        """
        last_message = messages[-1] if messages else None
        state["attempt"] = state.get("attempt", 0) + 1
        
        if last_message and last_message.get("role") == "assistant":
            completion = [last_message]
            parsed_code = self.parser.parse_answer(completion)
            
            if parsed_code is None:
                response = [{
                    "role": "user",
                    "content": "No valid Lean4 code found in your response. Please provide code within ```lean4 ``` code blocks."
                }]
            else:
                info = state.get("info", {})
                year = info.get("year")
                day = info.get("day")
                
                compile_result, run_result = self.get_results(completion, year, day, self.parser)
                
                if compile_result is None:
                    response = [{
                        "role": "user",
                        "content": "Failed to parse or create task from your code."
                    }]
                elif compile_result.returncode != 0:
                    feedback_parts = ["Compilation failed."]
                    
                    if compile_result.stdout:
                        stdout_cropped = compile_result.stdout[:self.compiler_output_crop]
                        feedback_parts.append(f"\nStdout:\n{stdout_cropped}")
                        if len(compile_result.stdout) > self.compiler_output_crop:
                            feedback_parts.append("... (stdout truncated)")
                    
                    if compile_result.stderr:
                        stderr_cropped = compile_result.stderr[:self.compiler_output_crop]
                        feedback_parts.append(f"\nStderr:\n{stderr_cropped}")
                        if len(compile_result.stderr) > self.compiler_output_crop:
                            feedback_parts.append("... (stderr truncated)")
                    
                    response = [{
                        "role": "user",
                        "content": "\n".join(feedback_parts)
                    }]
                else:
                    correctness = correctness_reward(year, day, run_result)
                    
                    if correctness == 1.0:
                        state["succeeded"] = True
                        response = [{
                            "role": "user",
                            "content": "All tests passed! Your solution is correct."
                        }]
                    else:
                        feedback_parts = ["Compilation succeeded, but tests did not fully pass."]
                        
                        if run_result and run_result.stdout:
                            stdout_cropped = run_result.stdout[:self.compiler_output_crop]
                            feedback_parts.append(f"\nYour program output:\n{stdout_cropped}")
                            if len(run_result.stdout) > self.compiler_output_crop:
                                feedback_parts.append("... (output truncated)")
                        
                        if run_result and run_result.stderr:
                            stderr_cropped = run_result.stderr[:self.compiler_output_crop]
                            feedback_parts.append(f"\nStderr:\n{stderr_cropped}")
                            if len(run_result.stderr) > self.compiler_output_crop:
                                feedback_parts.append("... (stderr truncated)")
                        
                        feedback_parts.append(f"\nCorrectness score: {correctness:.2f}/1.00")
                        feedback_parts.append("Please fix your solution and try again.")
                        
                        response = [{
                            "role": "user",
                            "content": "\n".join(feedback_parts)
                        }]
        else:
            response = [{
                "role": "user",
                "content": "Please provide your Lean4 solution."
            }]
        
        return response, state


def load_environment(
    max_turns: int = 4,
    years: List[int] = [2015, 2016,2017],
    days: List[int] = list(range(1, 26)),
    eval_days: List[int] = list(range(1,25)),
    use_think: bool = False,
    system_prompt: str = SYSTEM_PROMPT,
    weights: List[float] = [0.3, 0.7],
    compiler_output_crop: int = DEFAULT_COMPILER_OUTPUT_CROP,
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
        max_turns: Maximum number of turns for multi-turn interaction
        compiler_output_crop: Max characters per compiler output field
    """
    all_tasks = load_tasks(years=years, days=days)

    train_tasks = [t for t in all_tasks if t["day"] not in eval_days]
    eval_tasks = [t for t in all_tasks if t["day"] in eval_days]

    def tasks_to_dataset(tasks):
        data = [
            {
                "prompt": task["prompt"],  # Keep as string, not message list
                "info": {
                    "task_identifier": task["task_identifier"],
                    "year": task["year"],
                    "day": task["day"],
                },
            }
            for task in tasks
        ]
        
        if not data:
            import pyarrow as pa
            
            schema = pa.schema([
                ("prompt", pa.string()),
                ("info", pa.struct([
                    ("task_identifier", pa.string()),
                    ("year", pa.int64()),
                    ("day", pa.int64())
                ]))
            ])
            
            empty_table = pa.table({
                "prompt": pa.array([], type=pa.string()),
                "info": pa.array([], type=pa.struct([
                    ("task_identifier", pa.string()),
                    ("year", pa.int64()),
                    ("day", pa.int64())
                ]))
            }, schema=schema)
            
            return Dataset(empty_table)
        
        return Dataset.from_list(data)

    dataset = tasks_to_dataset(train_tasks)
    eval_dataset = tasks_to_dataset(eval_tasks)

    def extract_fn(text: str) -> str:
        result = extract_lean4_block(text)
        return result if result is not None else ""

    if use_think:
        parser = vf.ThinkParser(extract_fn=extract_fn)
    else:
        parser = vf.Parser(extract_fn=extract_fn)

    def compile_reward_func(parser, completion, info, state=None, **kwargs):
        year = info["year"]
        day = info["day"]
        
        if state and state.get("succeeded", False):
            return 1.0
        
        if isinstance(completion, list):
            completion_str = ""
            for msg in completion:
                if msg.get("role") == "assistant":
                    completion_str += msg.get("content", "")
        else:
            completion_str = completion
        
        extracted = parser.parse_answer(completion)
        if extracted is None:
            return 0.0
        
        spec = create_spec(year, day)
        task_id = create_task(spec, submission=extracted)
        compile_result, _ = run_task(task_id)
        
        return compile_reward(compile_result)

    def correctness_reward_func(parser, completion, info, state=None, **kwargs):
        year = info["year"]
        day = info["day"]
        
        if state and state.get("succeeded", False):
            return 1.0
        
        if isinstance(completion, list):
            completion_str = ""
            for msg in completion:
                if msg.get("role") == "assistant":
                    completion_str += msg.get("content", "")
        else:
            completion_str = completion
        
        extracted = parser.parse_answer(completion)
        if extracted is None:
            return 0.0
        
        spec = create_spec(year, day)
        task_id = create_task(spec, submission=extracted)
        compile_result, run_result = run_task(task_id)
        
        if compile_result.returncode != 0:
            return 0.0
        
        return correctness_reward(year, day, run_result)

    rubric = vf.Rubric(
        funcs=[compile_reward_func, correctness_reward_func],
        weights=weights,
    )

    vf_env = AOCBMultiTurnEnv(
        dataset=dataset,
        eval_dataset=eval_dataset,
        system_prompt=system_prompt,
        parser=parser,
        rubric=rubric,
        max_turns=max_turns,
        compiler_output_crop=compiler_output_crop,
    )

    return vf_env

if __name__ == "__main__":
    load_environment()
