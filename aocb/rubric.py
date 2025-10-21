import asyncio
import inspect
import logging
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from typing import Optional

from verifiers.parsers.parser import Parser
from verifiers import Rubric
from verifiers.types import (
    Info,
    Messages,
    RewardFunc,
    RolloutScore,
    RolloutScores,
    State,
)


def _sync_reward_func_wrapper(
    func: RewardFunc,
    prompt: Messages,
    completion: Messages,
    answer: str,
    state: State,
    task: str,
    info: Info,
    example_id: Optional[int],
    class_objects: dict,
    **kwargs
) -> float:
    """
    Synchronous wrapper for reward functions to be used in multiprocessing.
    This runs in a separate process.
    """
    sig = inspect.signature(func)
    
    common = dict(
        prompt=prompt,
        completion=completion,
        answer=answer,
        state=state,
        task=task,
        info=info,
        example_id=example_id,
    )
    common.update(class_objects)
    merged = {**common, **kwargs}
    
    try:
        if any(p.kind == p.VAR_KEYWORD for p in sig.parameters.values()):
            # If func is async, we need to run it in an event loop
            if asyncio.iscoroutinefunction(func):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    result = loop.run_until_complete(func(**merged))
                finally:
                    loop.close()
            else:
                result = func(**merged)
        else:
            allowed = {k: v for k, v in merged.items() if k in sig.parameters}
            if asyncio.iscoroutinefunction(func):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    result = loop.run_until_complete(func(**allowed))
                finally:
                    loop.close()
            else:
                result = func(**allowed)
        return float(result) #type:ignore
    except Exception as e:
        logging.error(f"Error calling reward function {func.__name__}: {e}")
        return 0.0

def _process_single_reward(
    rollout_idx: int,
    func_name: str,
    func: RewardFunc,
    prompt: Messages,
    completion: Messages,
    answer: str,
    state: State,
    task: str,
    info: Info,
    example_id: Optional[int],
    class_objects: dict,
    kwargs: dict
) -> tuple[int, str, float]:
    """Helper function to process a single reward in a separate process."""
    score = _sync_reward_func_wrapper(
        func, prompt, completion, answer, state, task, info, 
        example_id, class_objects, **kwargs
    )
    return (rollout_idx, func_name, score)



class BatchMultiprocessedRubric(Rubric):
    """
    A Rubric that processes entire batches using multiprocessing.
    More efficient for large batches as it reduces overhead.
    """
    
    def __init__(
        self,
        funcs: list[RewardFunc] | None = None,
        weights: list[float] | None = None,
        parser: Parser | None = None,
        parallelize_scoring: bool = True,
        max_workers: Optional[int] = None,
        chunk_size: int = 1,
        **kwargs,
    ):
        super().__init__(
            funcs=funcs,
            weights=weights,
            parser=parser,
            parallelize_scoring=parallelize_scoring,
            **kwargs
        )
        self.max_workers = max_workers
        self.chunk_size = chunk_size
    
    async def score_rollouts(
        self,
        prompts: list[Messages],
        completions: list[Messages],
        answers: list[str],
        states: list[State],
        tasks: list[str],
        infos: list[Info],
        example_ids: list[int] | None = None,
        max_concurrent: int = -1,  # Ignored in this implementation
        use_tqdm: bool = True,
        **kwargs,
    ) -> RolloutScores:
        """
        Compute reward scores for a group of rollouts using multiprocessing.
        """
        example_ids = example_ids or list(range(len(prompts)))
        
        # First run any group scoring
        await self.score_group(
            states,
            prompts=prompts,
            completions=completions,
            answers=answers,
            tasks=tasks,
            infos=infos,
            example_ids=example_ids,
            **kwargs,
        )
        
        if self.parallelize_scoring:
            loop = asyncio.get_event_loop()
            
            # Prepare work items
            work_items = []
            for i, (p, c, a, s, t, inf, eid) in enumerate(zip(
                prompts, completions, answers, states, tasks, infos, example_ids
            )):
                for func in self.get_reward_funcs():
                    work_items.append((
                        i, func.__name__, func, p, c, a, s, t, inf, eid, 
                        self.class_objects, kwargs
                    ))
            
            # Process in parallel using process pool
            with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
                if use_tqdm:
                    from tqdm import tqdm
                    
                    # Submit all tasks
                    futures = [ loop.run_in_executor( executor, partial(_process_single_reward, *item)) for item in work_items ]
                    
                    # Wait with progress bar
                    results = []
                    for future in tqdm(
                        asyncio.as_completed(futures),
                        total=len(futures),
                        desc=f"Evaluating {len(prompts)} rollouts x {len(self.get_reward_funcs())} functions"
                    ):
                        results.append(await future)
                else:
                    futures = [
                        loop.run_in_executor(
                            executor,
                            partial(_process_single_reward, *item)
                        )
                        for item in work_items
                    ]
                    results = await asyncio.gather(*futures)
            
            # Reorganize results
            rewards_by_rollout = {}
            for rollout_idx, func_name, score in results:
                if rollout_idx not in rewards_by_rollout:
                    rewards_by_rollout[rollout_idx] = {}
                rewards_by_rollout[rollout_idx][func_name] = score
            
            # Build final results
            rewards = []
            for i in range(len(prompts)):
                rollout_metrics = rewards_by_rollout[i]
                reward_sum = sum(
                    rollout_metrics[func.__name__] * weight
                    for func, weight in zip(self.get_reward_funcs(), self.get_reward_weights())
                )
                rewards.append(RolloutScore(
                    metrics=rollout_metrics,
                    reward=reward_sum
                ))
        else:
            # Fall back to original implementation
            return await super().score_rollouts(
                prompts, completions, answers, states, tasks, infos,
                example_ids, max_concurrent, use_tqdm, **kwargs
            )
        
        if not rewards:
            reward_func_names = self.get_reward_func_names()
            return RolloutScores(
                reward=[],
                metrics={name: [] for name in reward_func_names},
            )
        
        return RolloutScores(
            reward=[reward.reward for reward in rewards],
            metrics={
                k: [item.metrics[k] for item in rewards] for k in rewards[0].metrics
            },
        )
